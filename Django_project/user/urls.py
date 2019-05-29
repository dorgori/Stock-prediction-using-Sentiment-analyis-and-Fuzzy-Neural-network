from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='user-home'),
    path('base/', views.base, name='user-base'),
    path('about/', views.about, name='user-about'),
]