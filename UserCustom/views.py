import random
import string

from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from rest_framework.status import HTTP_400_BAD_REQUEST

from UserCustom.serializer import UserSerializer, GroupSerializer

from django.shortcuts import render
from django.contrib.auth.models import Group

from rest_framework import generics,mixins
from django.contrib.auth import authenticate, logout
from datetime import datetime, timezone
import json
from django.core import serializers
from rest_framework import response,request
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from  rest_framework.decorators import api_view,permission_classes
from django.core.mail import EmailMessage
from  store.serializers import *
from  store.models import *
# Create your views here.
from UserCustom.models import Users, Verification
from UserCustom.utils import verification_utils
from  order.models import *
from  order.serializer import *
from notifications import email_service
import random
from django.views.decorators.csrf import csrf_exempt


def generate_password():
    """ Generates a digit based default password """
    list = [random.choice(range(0, 9)) for i in range(0, 10)]
    code = ''.join(str(i) for i in list)
    return code



def _generate_code():
    key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    return key






@api_view(['PATCH', 'POST', 'PUT'])
#@permission_classes([IsAuthenticated])
def update_profile(request):
    try:
        user = Users.objects.filter(id=request.user.id).update(**request.data)

        if user:
            user = user[0]
            serializer = UserSerializer(user)
            return Response(serializer.data, status=200)
        return Response({"detail": "Something went wrong"}, status=400)
    except Exception as e:
        return Response({"detail": str(e)}, status=400)


@api_view(['POST'])
def manager_register(request):
    user_group = request.data.get('group', request.data.get('groups'))
    manager = Group.objects.filter(name='Manager').last()
#    request.data['is_active'] = False
    password = request.data.get('password', generate_password())
    email = request.data.get('email')
    name = request.data.get('name')
    phone_number = request.data.get('phone_number')

    user = Users.objects.filter(phone_number=phone_number) | Users.objects.filter(email=email)

    if len(user) > 0:
        user = user[0]
    else:
        user = None


    if user:
        from UserCustom.utils import verification_utils
        verification_utils.send_verification_code(user)
        return Response(
            {"detail": "User with this phone number / email aleady exists. Sign in or verify your account."},
            status=409)

    if not str(phone_number).startswith("+"):
        return Response({"detail": "Invalid phone number. Phone number must start with +"}, status=400)

    if name is None or email is None or password is None or phone_number is None:
        return Response({"detail": "Bad request"}, status=400)

    user = Users(
        name=name,
        email=email,
        is_active=True,
        phone_number=phone_number
    )

    user.save()
    user.groups.add(manager)

    user.set_password(password)

    user.save()

    verification = Verification.objects.filter(
        user=user,
        category='Activation',
        is_used=False
    ).first()

    if not verification:
        verification = Verification(
            user=user,
            category='Activation',
            is_used=False
        )
        verification.save()



    response = {
        "id": user.id,
        "phone_number": phone_number,
        "email": email,
        "name": name,
        "group": manager.name,

        "message": "Your account has been created successfully. However, verify your phone number to activate your account."
    }

    try:
        email_service.send_email(
            subject='Welcome to Omeal!',
            message='Your account has been created successfully. However, verify your phone number to activate your account.',
            user=user,
            email=None
        )
    except:
        pass
    return Response(response, status=201)


@api_view(['POST'])
@permission_classes([AllowAny])
def buyer_register(request):
    buyer = Group.objects.filter(name='Buyer').last()
   # request.data['is_active'] = False
    name = request.data.get('name')
    email = request.data.get('email')
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')



    users = Users.objects.filter(phone_number=phone_number) | Users.objects.filter(email=email)
    user = users[0] if len(users) > 0 else None

    if user:
        #verification_utils.send_verification_code(user)
        return Response({"detail":"User with this phone number / email aleady exists. Sign in or verify your account."}, status=409)

    if not str(phone_number).startswith("+"):
        return Response({"detail": "Invalid phone number. Phone number must start with +250"}, status=400)


    if name == None or email == None or password == None or phone_number == None:
        return Response({"detail": "Bad request"}, status=400)

    user = Users(
        name=name,
        email=email,
        phone_number=phone_number,
        is_active=False,
    )

    user.save()
    user.groups.add(buyer)

    user.set_password(password)
    user.save()


    response = {
        "id":str(user.id),
        "phone_number":phone_number,
        "email":email,
        "name":name,
        "groups":[
            {
                "name":buyer.name
            }
        ],
        "message":"Your account has been created successfully. However, verify your phone number to activate your account."
    }



    return Response(response,status=200)




@api_view(['POST'])
def activate_account(request):
    phone_number = request.data.get('phone_number', None)
    email = request.data.get('email', None)
    code = request.data.get('code')

    if phone_number is None and email is None:
        return Response({"detail": "Bad request"}, status=400)

    if phone_number is not None:
        if not str(phone_number).startswith("+"):
            return Response({"detail": "Invalid phone number. Phone number must start with +"}, status=400)

    user = Users.objects.filter(email=email).first()

    if not user:
        user = Users.objects.filter(phone_number=phone_number).first()

    if user is None:
        return Response({"detail": "User with this phone number does not exist. Register first."}, status=400)

    verification = Verification.objects.filter(code=code, user=user, category='Activation').last()

    if not verification:
        return Response({"detail": "Verification code is incorrect."}, status=400)

    now_time = datetime.now(timezone.utc)

    time_diff = now_time - verification.time_created

    if time_diff.total_seconds() >= 3600:
        verification.code = _generate_code()
        verification.save()

        verification_utils.send_verification_code(user)

        return Response({"detail": "Verification code expired. Sent another one"}, status=400)

    user.is_active = True
    user.save()

    serializer = UserSerializer(user, context={'request': request})
    serialized_data = serializer.data
    serialized_data['message'] = 'You account has been verified and activated successfully.'

    return Response(serialized_data, status=200)

@api_view(['POST','PATCH'])
#@permission_classes([IsAuthenticated])
def update_groups(request):
    user = request.user
    if user.is_superuser or user.is_staff:
        user = Users.objects.filter(user_id=request.data.get('id')).last()
        if user:
            user.groups.clear()
            group = Group.objects.filter(name=request.data.get('groups')).last()
            user.groups.add(group)
            return Response({"detail":"Groups updated successfully"}, status=200)
        return Response({"detail": "Something went wrong"}, status=400)

    return Response({"detail": "You are not allowed to update user group "}, status=403)




@api_view(['POST'])
@permission_classes((AllowAny, ))
def verify(request):
    phone_number = request.data.get('phone_number')
    code = request.data.get('code')

    if not str(phone_number).startswith("+"):
         return Response({"detail":"Invalid phone number. Phone number must start with +"}, status=400)

    user = Users.objects.filter(phone_number=phone_number).last()

    if user is None:
        return Response({"detail":"User with this phone number does not exist. Register first."}, status=400)

    verification = Verification.objects.filter(code=code, user=user, category='Activation', is_used=False).last()

    if verification is None:
        return Response({"detail":"Verification code is incorrect."}, status=400)

    user.is_active = True
    user.save()
    verification.is_used = True
    verification.save()

    serializer = UserSerializer(user)

    return Response(serializer.data, status=200)




@api_view(['POST'])
def resend_verification(request):
    phone_number = request.data.get('phone_number')
    category = request.data.get('category', 'Activation')

    if not str(phone_number).startswith("+"):
         return Response({"detail":"Ivalid phone number. Phone number must start with +"}, status=400)

    user = Users.objects.filter(phone_number=phone_number).last()

    if user is None:
        return Response({"detail":"User with this phone number does not exist. Register first."}, status=400)

    verification_utils.send_verification_code(user)

    return Response({"detail":"Verification code has been sent to {}".format(phone_number)}, status=200)


@api_view(['POST'])
def send_reset_code(request):
    phone_number = request.data.get('phone_number')

    if not phone_number:
        return Response({"detail": "Phone number must be sent"}, status=400)
    user = Users.objects.filter(phone_number=phone_number).first()

    if not user:
        return Response({"detail": "User with {} phone number is not found".format(phone_number)}, status=400)

    verification = Verification.objects.filter(
        user=user,
        category='Reset',
        is_used=False
    ).first()

    if not verification:
        verification = Verification(
                user=user,
                category='Reset',
                is_used=False
            )
        verification.save()

    verification_utils.send_verification_code(user)
    email_service.send_email(
        subject="Omeal password reset code",
        message="{} is your omeal account password reset code.".format(verification.code),
        user=user
    )

    return Response({"detail": "Reset code has been sent to your email and phone number. If not received, try again."}, status=200)


@api_view(['PATCH', 'POST', 'PUT'])
def reset_password(request):
    code = request.data.get('code')
    password = request.data.get('password')
    if not code:
        return Response({"detail": "Reset code is required."}, status=400)

    verification = Verification.objects.filter(code=code, category='Reset', is_used=False).first()

    if not verification:
        return Response({"detail": "Reset code is invalid."}, status=400)
    if not password:
        return Response({"detail": "Invalid password. password is required."}, status=400)
    user = verification.user

    user.set_password(password)
    user.save()
    verification.is_used = True
    verification.save()
    Token.objects.filter(user=user).delete()

    return Response({"detail": "Password has been changed successfully."}, status=200)

@api_view(['POST'])
def login(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')
    user = authenticate(request=request, username=phone_number, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        response = UserSerializer(user).data
        response['token'] = token.key
        return Response(response, status=200)
    return Response({"detail": "Invalid credentials"}, status=400)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def forgot_password(request):
    phone_number = request.data.get('phone_number')


    if phone_number:
        user = Users.objects.filter(phone_number=phone_number).last()

        if not user:
            return Response({'detail': 'User not found'}, status=404)

        verification = Verification(
            user=user,
            category='Reset',
        )
        verification.save()

       # verification_utils.send_verification_code(user)

        return Response({'detail': 'Reset code sent to your phone number via SMS'}, status=200)

    return Response({'detail': 'Bad request'}, status=400)

#Login
class UserList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    queryset = Users.objects.none()
    serializer_class = UserSerializer


    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Users.objects.all()

        user_group = user.groups.first()
        if user_group.name == 'Manager'or  user_group.name == 'Administrator':
            return User.objects.all()

        if user_group.name == 'Buyer':
            return User.objects.filter(user=user)

        return User.objects.none()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserDetail(mixins.
                 RetrieveModelMixin, mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Users.objects.none()
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Users.objects.all()

        user_group = user.groups.first()
        if user_group.name == 'Manager':
            return Users.objects.all()

        if user_group.name == 'Buyer':
            return Users.objects.filter(user=user)

        return User.objects.none()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            user_group = Group.objects.filter(name=request.data.get('groups')).first()
            user = self.get_object()

            if user_group and user:
                user.groups.clear()
                user.groups.add(user_group)
            return self.partial_update(request, *args, **kwargs)
        return Response({"detail": "You are not allowed to perform such operation"}, status=403)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return self.destroy(request, *args, **kwargs)

        return Response({"detail": "You are not allowed to perform such action."}, status=403)



