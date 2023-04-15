from django.urls import path
from .views import *

app_name='article'

urlpatterns=[
    path('',ArticleView.as_view(),name='blog'),
    path('<str:slug>/',ArtcileDetailView.as_view(),name='blog_detail'),
    path('last_article/<str:slug>',last_article,name='last_article'),

]