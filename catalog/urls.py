from django.urls import path
from . import views

# Без app_name
urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
]