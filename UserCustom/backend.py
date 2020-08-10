"""
Backend that allows authentication using email and phone_number
"""
from UserCustom.models import Users

class Backend(object):

    def authenticate(self, request=None, **kwargs):
        """
        Returns a user with the given credentials
        :param request: Request object passed to the backend
        :param kwargs: Contains credentials to find user
        :return: User if credentials are found
        """
        username = kwargs.get('username')  # Contains email or phone_number
        password = kwargs.get('password')

        # Trying email
        user = Users.objects.filter(email=username).first()

        # Trying phone_number
        if not user:
            user = Users.objects.filter(phone_number=username).first()

        if user:
            if user.check_password(password) and user.is_active:
                return user

        return None

    def get_user(self, user_id):
        """
        Returns instance of the user, when given the user_id
        :param user_id: User id, the current primary key
        :return: User if found and None otherwise
        """
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None
