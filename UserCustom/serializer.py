from UserCustom.models import Users
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from UserCustom.models import DeliveryInfo

from django.contrib.auth.models import Group
from rest_framework import serializers
from UserCustom.models import Users




class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id','name')



class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = Users
        fields = ['phone_number', 'email', 'name', 'groups', 'id', 'is_staff', 'is_superuser', 'is_active']
    def to_representation(self, obj):
        serialized_data = super(UserSerializer, self).to_representation(obj)
        user = None
        request = self.context.get("request")

        if not request and not hasattr(request, "user"):
            serialized_data.pop('groups')
        return serialized_data


class SellerSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='seller.name')
    address = serializers.CharField(source='seller.drivers')

    class Meta:
        model = Users
        fields = ('email', 'password', 'name', 'drivers')


class DeliveryInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryInfo
        fields = ('name', 'drivers', 'phone')


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=127)
