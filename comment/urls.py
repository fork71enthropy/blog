from django.urls import path
from . import views

urlpatterns = [
    path('post/<int:post_pk>/add/', views.add_comment, name='add_comment'),
    path('<int:comment_pk>/like/', views.toggle_comment_like, name='toggle_comment_like'),
]