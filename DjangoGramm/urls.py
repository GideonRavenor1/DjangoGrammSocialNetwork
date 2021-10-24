from django.urls import path
from .views import *


app_name = 'DjangoGramm'


urlpatterns = [
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/password/change/', DjangoPasswordChangeView.as_view(), name='password_change'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/logout/', DjangoLogoutView.as_view(), name='logout'),
    path('accounts/profile/delete/<int:pk>/', ProfileImageDeleteView.as_view(), name='profile_image_delete'),
    path('accounts/profile/add/', ProfileImageAddView.as_view(), name='profile_image_add'),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('accounts/login/', DjangoLoginView.as_view(), name='login'),
    path('<str:page>/', other_page, name='other'),
    path('by_user/<int:pk>/', UserPageView.as_view(), name='by_user'),
    path('', IndexView.as_view(), name='index'),
    path('ajax/load-more-user-images/', DynamicUserImageLoad.as_view(), name='load-more-user-images'),
]
