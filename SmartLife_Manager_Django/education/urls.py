# SmartLife_Manager_Django/education/urls.py
from django.urls import path
from . import views

app_name = 'education'

urlpatterns = [
    path('tentang-aplikasi/', views.about_app_view, name='about_app'),
]