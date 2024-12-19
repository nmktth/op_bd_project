# op_bd_project/urls.py
from django.urls import path
from django.shortcuts import redirect
from products import views  # Импортируем представления из приложения products

urlpatterns = [
    # Редирект с корневого пути на страницу добавления товара
    path('', lambda x: redirect('products')),  # Перенаправление на '/add-product/', если корневая страница запрашивается

    # Путь для страницы добавления товара
    path('products/', views.products, name='products'),
    path('get-all/', views.get_all, name='get-all'),
    path('get/', views.get, name='get'),
    
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete')
]
