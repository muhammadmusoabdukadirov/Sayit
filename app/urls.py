from django.contrib import admin
from django.urls import path
from .views import index, create_order, clients

urlpatterns = [
    path('', index, name='index'),
    path('create_order/', create_order, name='create_order'),
    path('clients/', clients, name='clients'),
]