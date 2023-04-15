from django.urls import path
from .views import *
# #------------------------------------------------------------------------------


app_name='orders'

urlpatterns = [
    path('',shopCartView.as_view(),name='ordersmain'),
    path('show_shop_cart/',show_shop_cart,name='show_shop_cart'),
    path('add_to_shop_cart/',add_to_shop_cart,name='add_to_shop_cart'),
    path('delete_from_shop_cart/',delete_from_shop_cart,name='delete_from_shop_cart'),
    path('update_shop_cart/',update_shop_cart,name='update_shop_cart'),
    path('status_of_shop_cart/',status_of_shop_cart,name='status_of_shop_cart'),
    path('create_ordere/',CreateOrderView.as_view(),name='createorder'),
    path('checkout/<int:order_id>/',CheckoutOrderView.as_view(),name='checkout_order'),
    path('apply_coupon/<int:order_id>/',ApplyCoupon.as_view(),name='apply_coupon'),
]







