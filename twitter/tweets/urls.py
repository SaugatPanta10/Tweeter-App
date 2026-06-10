from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('register/', views.register_view, name = 'register'),
    path('login/', views.login_view, name = 'login'),
    path('logout', views.logout_view, name = 'logout'),
    path ('create/', views.tweet_create, name = 'tweet_create'),
    
] 
