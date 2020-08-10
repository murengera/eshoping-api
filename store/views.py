from django.contrib.auth.models import Group
from django.core.files import File
from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response





from store.models import Stock,StockRating
from store.serializers import StoreSerializer,StoreReviewSerializer
from UserCustom.models import Users

from UserCustom.serializer import UserSerializer



class StoresList(generics.GenericAPIView,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """
    View to list all stores, and create new ones
    """
    serializer_class = StoreSerializer

    filter_fields = ('id', 'store_code', 'name', 'is_verified', 'is_deleted', 'workers', 'activated_by', 'is_active')
    ordering_fields = ('store_code', 'name', 'is_verified', 'is_deleted', 'time_created', 'is_active')
    search_fields = ('store_code', 'name', 'time_created', 'description', 'followers', 'is_verified')

    def get_queryset(self):
        queryset = Stock.objects.filter(is_deleted=False, is_active=True)

        user = self.request.user
        user_grp = user.groups.first()
        admin_grp = Group.objects.filter(name='Administrator').first()

        if user:
            if user_grp == admin_grp:
                queryset = Stock.objects.filter(is_deleted=False)

        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user

        st = Stock.objects.filter(workers=user).first()
        if st:
            return Response({'detail': 'The user already has a store'}, status=409)

        name = request.data.get('name')
        description = request.data.get('description')
        icon = request.data.get('icon')
        banner = request.data.get('banner', None)

        if not name or not description or not icon:
            return Response({'detail': 'Bad Request'}, status=400)

        store = Stock.objects.create(
            name=name,
            description=description,
            icon=icon,
            banner=banner
        )
        store.workers.add(user)
        response_data = StoreSerializer(store, context={'request': request}).data
        response_data['message'] = "Store created successfully. Please wait while it\'s being activated"

        return Response(response_data, status=201)

class StoreDetails(generics.GenericAPIView,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin):
    """
    View to deal with a particular store
    """
    queryset = Stock.objects.filter(is_deleted=False)
    serializer_class = StoreSerializer




    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        user = request.user
        store = self.get_object()

        if request.data.get('is_verified') is not None or request.data.get('is_deleted') is not None:
            return Response({"detail": "You are trying to do a fraudulent action, please stop!"}, status=403)

        user_store = Stock.objects.filter(workers=user).first()

        if user_store is not None and user_store == store:
            return self.partial_update(request, *args, **kwargs)

        return Response({"detail": "You are not allowed to perform such operation"}, status=403)




# Change store icon
@api_view(['PATCH'])
@permission_classes((IsAuthenticated, ))
def change_store_icon_banner(request):
    user = request.user
    user_grp = user.groups.first()
    store_manager_grp = Group.objects.filter(name="Administrator").first()

    if user_grp == store_manager_grp:
        icon = request.data.get('icon', None)
        banner = request.data.get('banner', None)

        store = Stock.objects.filter(workers=user).first()

        if not store:
            return Response({'detail': 'Store not found'}, status=404)

        if not icon and not banner:
            return Response({'detail': 'Bad request (icon and banner fields are empty)'}, status=400)

        if icon:
            store.icon = icon
            store.save()

        if banner:
            store.banner = banner
            store.save()

        response_data = StoreSerializer(store, context={'request': request}).data

        return Response(response_data, status=200)

    return Response({"detail": "You are not allowed to perform such operation"}, status=403)



# Verifying a store
@api_view(['PATCH'])
@permission_classes((IsAuthenticated, ))
def verifying_store(request):
    user = request.user
    user_grp = user.groups.first()
    admin_grp = Group.objects.filter(name='Administrator').first()
    status='True'


    if user_grp == admin_grp:

        store = Stock.objects.filter(workers=user).first()

        print(store)

        if store:
            store.is_verified =status
            store.save()
            store = StoreSerializer(store, context={'request': request}).data

        return Response(store, status=200)

    return Response({"detail": "You are trying to do a fraudulent action, please stop!"}, status=403)





# Verifying a store
@api_view(['PATCH'])
@permission_classes((IsAuthenticated, ))
def activate_store(request):
    user = request.user
    user_grp = user.groups.first()
    admin_grp = Group.objects.filter(name='Administrator').first()
    status='True'


    if user_grp == admin_grp:
        store = Stock.objects.filter(workers=user).first()

        store.is_active = status
        store.activated_by = user
        store.save()

        store = StoreSerializer(store, context={'request': request})

        return Response(store.data, status=200)

    return Response({"detail": "You are trying to do a fraudulent action, please stop!"}, status=403)


class StoresReviewsList(generics.GenericAPIView,mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    queryset = StockRating.objects.all()
    serializer_class = StoreReviewSerializer
    def get(self,request,*args,**kwargs):
        return  self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        user= self.request.user
        #request.data['reviewer']= str(user.id)
        return  self.create(request,*args,**kwargs)

