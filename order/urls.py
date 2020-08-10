from django.urls import path

from order.views import *
from .import views

urlpatterns = [


    path('orders/', OrderList.as_view(), name='orders_list'),
    path('orders/<slug:pk>', OrderDetails.as_view(), name='order_details'),
    path('get-active-order/',views.get_active_order),
    path('finish-order/', views.finish_order),
    path('get_finished_order/', views.getFinishedOrder),
    path('activate_order/', views.activate_order),




]
