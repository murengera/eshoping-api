from django.template.context_processors import static

from eShoping import settings
from product.views import *
from django.urls import path

urlpatterns = [

    path('item-conditions', ItemConditionsList.as_view(), name='item_conditions_list'),
    path('item-conditions/<slug:pk>', ItemConditionDetails.as_view(), name='item_condition_details'),
    path('product/', ProductList.as_view()),
    path('product/<slug:pk>', ProductDetail.as_view(), name='products_detail'),
    path('store-products', get_store_products, name='get_store_products'),

    path('discounts/', DiscountList.as_view(), name='discounts_list'),
    path('products-reviews', ProductReviewsList.as_view(), name='products_reviews_list'),
    path('get_store_products', get_store_products, name='products_reviews_list')


]
