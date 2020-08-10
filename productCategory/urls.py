from django.urls import path, re_path
from productCategory.views import *

urlpatterns = [
    path('products-categories/', ProductsCategoriesList.as_view()),
    path('products-brands/', ProductsBrandsList.as_view())
]
