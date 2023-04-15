from django.urls import path
from .views import *

app_name='products'

urlpatterns = [
    path('product_detail/<slug:slug>/',ProductDetailView.as_view(),name='product_detail'),
    path('cheapest_products/',cheapest_products,name='cheapest_products'),
    path('brands/',get_brand,name='brands'),
    path('newest_products/',th_newest_products,name='newest_products'),
    path('popular_groups/',popular_groups,name='popular_groups'),
    path('related_product/<slug:slug>/',related_products,name='related_product'),
    path('products_ech_group/<slug:slug>/',products_ech_groups.as_view(),name='products_ech_group'),
    path('ajax_admin/',get_filter_value_for_feature,name='filter_value_for_feature'),
    path('filter_get_product_groups/',filter_get_product_groups,name='filter_get_product_groups'),
    path('filter_get_product_brands/<slug:slug>/',filter_get_product_brands,name='filter_get_product_brands'),
    path('filter_get_product_features/<slug:slug>/',filter_get_product_features,name='filter_get_product_features'),
]
