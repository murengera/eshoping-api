from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import mixins, generics
from rest_framework.response import Response

from productCategory.serializer import ProductCategorySerializer,ProductBrandSerializer

from productCategory.models import ProductCategory,Brand
from  rest_framework import  serializers

"""
 ProductCategory  Views
 """
class ProductsCategoriesList(generics.GenericAPIView,
                             mixins.ListModelMixin,
                             mixins.CreateModelMixin):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user
        title = request.data.get('title')
        title_lower = title.strip().lower()
        titles = []

        if not title:
            return Response({'detail': 'Bad request. The category title is required'}, status=400)
        categories = ProductCategory.objects.all()
        for category in categories:
            titles.append(category.title.strip().lower())
        for t in titles:
            if t == title_lower:
                return Response({"detail": "Category or sub category already exists"}, status=409)

        product_categories = ProductCategory.objects.create(
            title=title,
            created_by=user
        )

        response_data = ProductCategorySerializer(product_categories, context={'request': request}).data
        return Response(response_data, status=201)




class ProductsBrandsList(generics.GenericAPIView,
                             mixins.ListModelMixin,
                             mixins.CreateModelMixin):

        queryset = Brand.objects.all()
        serializer_class = ProductBrandSerializer

        def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)

        def post(self, request, *args, **kwargs):
            user = request.user
            title = request.data.get('title')
            title_lower = title.strip().lower()
            image = request.data.get('image')
            titles = []

            if not title or not image:
                return Response({'detail': 'Bad request. Some required fields are missing'}, status=400)

            brands = Brand.objects.all()
            for br in brands:
                titles.append(br.title.strip().lower())

            for t in titles:
                if t == title_lower:
                    return Response({"detail": "Brand already exists"}, status=409)

            product_brand = Brand.objects.create(
                title=title,
                image=image,
                created_by=user
            )

            response_data = ProductBrandSerializer(product_brand, context={'request': request}).data
            return Response(response_data, status=201)









