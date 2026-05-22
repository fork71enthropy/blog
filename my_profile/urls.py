from django.urls import path
from . import views

urlpatterns = [
    path('',views.my_profile_presentation,name='my_profile'),
    path('books',views.allbooks,name='allbooks'),
    path('projects',views.allprojects,name='allprojects'),
    
]





































