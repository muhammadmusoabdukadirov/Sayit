from django.contrib import admin
from django.urls import path
from .views import index, create_order, clients, sozlamalar,update_order_status,delete_order,boshqaruv_view,profile_view

urlpatterns = [
    path('', index, name='index'),
    path('create_order/', create_order, name='create_order'),
    path('clients/', clients, name='clients'),
    path('sozlamalar/', sozlamalar, name='sozlamalar'),
    path('boshqaruv/', boshqaruv_view, name='boshqaruv'),
    path('order/<int:order_id>/update-status/',update_order_status, name='update_order_status'),
    path('profile/', profile_view, name='profile'),

    # 🔥 Delete order URL
    path('order/<int:order_id>/delete/', delete_order, name='delete_order'),

]