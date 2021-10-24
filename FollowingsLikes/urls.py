from django.urls import path
from .views import *

app_name = 'FollowingsLikes'

urlpatterns = [
    path('images/', FollowersImagesListView.as_view(), name='followers_images'),
    path('list/', FollowersListView.as_view(), name='list_followers'),
    path('ajax/load-more-followers/', DynamicFollowingsLoad.as_view(), name='load-more-followers'),
    path('ajax/count-likes/<int:pk>/', DynamicLikes.as_view(), name='count-likes'),
    path('ajax/followings/<int:pk>/', DynamicFollowings.as_view(), name='followings')
]
