from rest_framework import *
from order.models import *
from product.models import *
from  store.models import *
from  store.serializers import *
from  UserCustom.models import*
from UserCustom.serializer import *
from product.serializer import *
from django.contrib.auth.models import *
from rest_framework import serializers
from UserCustom.models import *




class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'

    def to_representation(self, instance):
         serialized_data=super(OrderSerializer,self).to_representation(instance)
         serialized_data['buyer'] = UserSerializer(instance.buyer, context=self.context).data
         serialized_data['product'] = ProductSerializer(instance.product, context=self.context).data

         serialized_data['price'] = float(serialized_data['price'])
#         serialized_data['quantity'] = float(serialized_data['quantity'])
         serialized_data['total_price'] = float(serialized_data['total_price'])


         return serialized_data
