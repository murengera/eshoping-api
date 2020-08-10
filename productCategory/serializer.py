from rest_framework import serializers
from productCategory.models import ProductCategory,Brand


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductCategory
        fields='__all__'

class ProductBrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'

