from django.urls import path
from .views import CommentPageAddView


app_name = 'Comments'

urlpatterns = [
    path('image/<int:pk>/', CommentPageAddView.as_view(), name='comment_page'),
]
