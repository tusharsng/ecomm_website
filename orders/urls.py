from django.urls import path
from . import views

urlpatterns = [
    
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('create/', views.order_create, name='order_create'),
    path('my_order/', views.my_order, name='my_order'),
    path('sucess/', views.sucess, name='sucess'),
    ]