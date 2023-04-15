from django.urls import path
from .views import *
#----------------------------------------------------------------

app_name='csws'

urlpatterns = [
    path('create_comment/<slug:slug>/',CommentView.as_view(),name='create_comment'),
    path('add_score/',add_score,name='add_score'),
    path('add_favorite/',add_favorite,name='add_favorite'),
    path('user_favorite/',UserFavoriteView.as_view(),name='user_favorite'),
]



