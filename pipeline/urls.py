from django.urls import path
from . import views

urlpatterns = [
    path('createuser/', views.UserCreate.as_view(), name='create-user'),
    path('loginuser/', views.UserLogin.as_view(), name='login-user'),
    path('pipelines/', views.Pipelines.as_view(), name='pipelines'),
    path('pipelines/pipeline/', views.ViewPipeline.as_view(), name='pipeline'),
    path('boards/', views.Boards.as_view(), name='boards'),
]