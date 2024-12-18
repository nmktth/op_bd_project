# op_bd_project/urls.py
from django.urls import path
from django.shortcuts import redirect
from products import views  # Импортируем представления из приложения products

urlpatterns = [
    # Редирект с корневого пути на страницу добавления товара
    path('', lambda x: redirect('add_product')),  # Перенаправление на '/add-product/', если корневая страница запрашивается

    # Путь для страницы добавления товара
    path('add-product/', views.add_product, name='add_product'),
]
