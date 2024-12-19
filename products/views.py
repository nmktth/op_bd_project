# products/views.py
import json
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .classes.parser import Parser
from .classes.db import DB
from decimal import Decimal  # Для преобразования цены в Decimal
from .models import Product  # Импортируем модель

parser = Parser()
db = DB()

@csrf_exempt
def update(request):
    if request.method == "POST":
        url = request.POST.get("url")
        price = request.POST.get("price")
        
        if url and price:
            price = float(price.replace(",", "."))
            db.update_price(url, price)
    return JsonResponse({'result': True})



def get_all(request):
    products = db.get_all()
    # Преобразуем каждый объект Product в словарь
    products_list = [product.to_dict() for product in products]
    return JsonResponse({'data': products_list})

def get(request):
    if request.method != "GET": return
    
    url = request.GET.get("url")
    if url is None: return
    
    product = db.get(url)
    if product is None: return
    return JsonResponse({'data': product.to_dict()})

def delete(request):
    if request.method != "GET": return
    
    url = request.GET.get("url")
    if url is None: return
    
    db.delete(url)
    return JsonResponse({'result': True})


def products(request):
    # Сначала получаем все продукты из базы данных
    all_products = db.get_all()

    if request.method == 'POST':
        method = request.POST.get("_method", "").upper()
        if method == "POST":
            url = request.POST.get('ozon')

            if url:
                resp = parser.url(url)

                if isinstance(resp, Exception):
                    return JsonResponse({'error': f"Ошибка при парсинге данных: {str(resp)}"})
            
                price, name = resp  # Распаковываем ответ парсера
                db.create(name, price, url)
                return redirect("products")
        if method == "UPDATE":
            percent = request.POST.get('procent')
            url = request.POST.get('url')

            if url and percent:
                
                db.update_percent(url, int(percent.replace("%", "")))
                return redirect("products")
        elif method == 'DELETE':
            url = request.POST.get('url')
            if url:
                db.delete(url)
                return redirect("products")



    # Если POST-запрос не был отправлен, просто отобразим все товары
    return render(request, 'products.html', {'all_products': all_products})
