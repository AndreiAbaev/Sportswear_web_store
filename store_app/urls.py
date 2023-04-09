from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('category/<int:category_id>/', product_category, name='category'),
    path('product/<int:product_id>/', show_product, name='product'),
    path('cart/', product_cart, name='product_cart'),
    path('cart/add/<int:product_id>', cart_add, name='cart_add'),
    path('order/<int:user_id>/', order, name='order'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('account/<int:user_id>', account_user, name='account'),
]
