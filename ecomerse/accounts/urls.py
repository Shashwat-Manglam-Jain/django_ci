from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.Login, name ='login'),
    path('logout/', views.logout_view, name ='logout'),
    path('register/', views.register, name ='register'),
    path('forget_password/', views.forget_Password, name ='forget_Password'),
    path('reset_password/<str:code>/', views.reset_password, name ='reset_password'),
    path('home/', views.home_view, name ='home'),
]