from rest_framework import serializers
from ads.models import Carousel_ad
from store.models import Stock
from store.serializers import StoreSerializer, StoreMiniSerializer
from UserCustom.models import Users
from UserCustom.serializer import UserSerializer


class CarouselAdSerializer(serializers.ModelSerializer):

    class Meta:
        model=Carousel_ad
        fields = ['id', 'title', 'description', 'is_active',
                  'expire_date', 'action_name', 'action', 'image', 'store', 'created_by']

        def to_representation(self, instance):
            serialized_data = super(CarouselAdSerializer, self).to_representation(instance)

            serialized_data['store'] = StoreMiniSerializer(instance.store, context=self.context).data
            serialized_data['created_by'] = UserSerializer(instance.created_by, context=self.context).data

            return serialized_data
