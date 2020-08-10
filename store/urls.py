from django.urls import path, re_path
from store.views import *


urlpatterns = [
    path('stores', StoresList.as_view(), name='stores_list'),
    path('stores/<slug:pk>', StoreDetails.as_view(), name='store_details'),
    path('change-store-icon-banner', change_store_icon_banner, name='change_store_icon'),

    # Endpoint used by administrator to verify a store
    path('verify-store', verifying_store, name='verify_store'),

    # Endpoint used by administrator to activate a store
    path('activate-store', activate_store, name='activate_store'),
    path('stores-reviews', StoresReviewsList.as_view(), name='stores_reviews_list'),

]
