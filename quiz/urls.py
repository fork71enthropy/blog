from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_quizzes, name='all_quizzes'),
    path('<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('<int:quiz_id>/success/', views.quiz_success, name='quiz_success'),
]