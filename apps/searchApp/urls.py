from django.urls import path
from .views import *
#------------------------------------------------------------------------------

app_name='search_app'
urlpatterns = [
    path('',Search.as_view(),name='search_view')
]




