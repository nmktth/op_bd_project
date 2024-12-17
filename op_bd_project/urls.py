from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    # Редирект с корневого пути на страницу добавления товара
    path('', lambda request: redirect('add_product')),  # Перенаправление на '/add-product/'
    
    # Путь для страницы добавления товара
    path('add-product/', views.add_product, name='add_product'),
]
