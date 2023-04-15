from django.urls import path
from .views import *
#----------------------------------------------------------------

app_name='main'

urlpatterns = [
    path('',index,name='index'),
    path('about_us',about_us,name='about_us'),
    path('contact_us',contact_us,name='contact_us'),
    
    
]
