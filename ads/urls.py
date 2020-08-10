from django.urls import path, re_path
from ads.views import *

urlpatterns = [
    path('carousel-ads', CarouselAdsList.as_view(), name='carousel_ads_list'),
    path('carousel-ads/<slug:pk>', CarouselAdDetails.as_view(), name='carousel_ad_details'),


]