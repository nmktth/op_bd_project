# products/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .classes.parser import Parser
from decimal import Decimal  # Для преобразования цены в Decimal
from .models import Product  # Импортируем модель

parser = Parser()

def add_product(request):
    # Сначала получаем все продукты из базы данных
    all_products = Product.objects.all()

    if request.method == 'POST':
        url = request.POST.get('ozon')

        if url:
            resp = parser.url(url)

            if isinstance(resp, Exception):
                return JsonResponse({'error': f"Ошибка при парсинге данных: {str(resp)}"})
        
            price, name = resp  # Распаковываем ответ парсера
            
            product, created = Product.objects.get_or_create(url=url)  # Получаем или создаем продукт по URL
            product.name = name  # Обновляем название товара
            product.price = Decimal(price)  # Обновляем цену в формате Decimal
            product.save()  # Сохраняем изменения в базе данных

            # Передаем информацию в шаблон, включая все товары
            return render(request, 'add_product.html', {'price': price, 'product': product, 'all_products': all_products})


    # Если POST-запрос не был отправлен, просто отобразим все товары
    return render(request, 'add_product.html', {'all_products': all_products})
