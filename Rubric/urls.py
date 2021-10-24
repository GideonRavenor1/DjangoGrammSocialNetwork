from django.urls import path
from .views import ByRubricView


app_name = 'Rubric'

urlpatterns = [
    path('by/<int:rubric_id>/', ByRubricView.as_view(), name='by_rubric'),
    ]
