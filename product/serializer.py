from rest_framework import serializers

from productCategory.serializer import *
from product.models import *
from store.models import *
from store.serializers import *



class ItemConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConditionItems
        fields = ('__all__')

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountOffer
        fields = ('__all__')



"""
product serializer
"""
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producte


        exclude = ['is_deleted']

    def to_representation(self, instance):
            serialized_data = super(ProductSerializer, self).to_representation(instance)
            serialized_data['item_condition'] = ItemConditionSerializer(instance.item_condition,context=self.context).data
            serialized_data['category'] = ProductCategorySerializer(instance.category, context=self.context).data
            serialized_data['brand'] = ProductBrandSerializer(instance.brand, context=self.context).data
            serialized_data['discount'] =  DiscountSerializer(instance.brand, context=self.context).data
            serialized_data['stock'] = StoreMiniSerializer(instance.stock, context=self.context).data
            return serialized_data


class ProductReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductReviewers
        fields = '__all__'
