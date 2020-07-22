from django.urls import path
from . import views

urlpatterns = [
    path('createuser/', views.UserCreate.as_view(), name='create-user'),
    path('loginuser/', views.UserLogin.as_view(), name='login-user'),
]