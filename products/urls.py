from django.urls import path,include
from . import views


urlpatterns = [
   
     
    path('<int:id>/<slug:slug>/', views.product_detail,
        name='product_detail'),

    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/',
        views.cart_add,
        name='cart_add'),
    path('remove/<int:product_id>/',
        views.cart_remove,
        name='cart_remove'),
    path('<slug:category_slug>/', views.home,
        name='product_list_by_category'),
    path('',views.home,name=('product_list') ),
    path('accounts/update/', views.profileupdate, name='profileupdate'),
    path('accounts/profile/', views.profiles, name='profile'),
    path('accounts/apply/', views.applytobeaseller, name='apply'),
    path('accounts/myproducts/', views.myproducts, name='myproducts'),
     path('accounts/deleteproduct/<int:id>/', views.deleteproduct, name='deleteproduct'),
     path('accounts/editproduct/<int:id>/', views.editproduct, name='editproduct'),
      path('accounts/Addproduct/', views.addproduct, name='addproduct'),
    ]