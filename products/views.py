# products/views.py
from django.shortcuts import render
from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
from decimal import Decimal  # Для преобразования цены в Decimal
from .models import Product  # Импортируем модель

def add_product(request):
    # Сначала получаем все продукты из базы данных
    all_products = Product.objects.all()

    if request.method == 'POST':
        url = request.POST.get('ozon')

        if url:
            # Настроим Selenium
            options = Options()
            options.headless = True  # Запуск браузера без окна

            # Укажи путь к Chrome, если он не добавлен в системный путь
            options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'  # Укажи свой путь

            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(url)

            # Подождем несколько секунд, чтобы страница полностью загрузилась
            driver.implicitly_wait(10)

            try:
                # Находим кнопку для перезагрузки страницы или проверки (reload)
                reload_button = driver.find_element(By.ID, 'reload-button')
                reload_button.click()  # Кликаем по кнопке

                # Подождем некоторое время, чтобы страница обновилась
                time.sleep(3)  # Пауза 3 секунды для обновления

                # Ищем элемент с ценой
                price_element = driver.find_element(By.CLASS_NAME, 'v6l_27')  # Убедись, что это правильный класс для цены

                # Извлекаем цену и убираем все символы, кроме цифр
                price_text = price_element.text.strip()
                price = Decimal(re.sub(r'\D', '', price_text))  # Преобразуем строку в Decimal

                # Ищем название товара (например, через другой селектор)
                name_element = driver.find_element(By.CLASS_NAME, 'wl7_27.tsHeadline550Medium')  # Убедитесь, что это правильный класс для названия товара
                name = name_element.text.strip()

                # Сохраняем цену и название в базе данных
                product, created = Product.objects.get_or_create(url=url)
                product.name = name  # Обновляем название товара
                product.price = price  # Обновляем цену
                product.save()  # Сохраняем в базе данных

                # Передаем информацию в шаблон, включая все товары
                return render(request, 'add_product.html', {'price': price, 'product': product, 'all_products': all_products})

            except Exception as e:
                driver.quit()
                return JsonResponse({'error': f"Ошибка при парсинге данных: {str(e)}"})

            driver.quit()

    # Если POST-запрос не был отправлен, просто отобразим все товары
    return render(request, 'add_product.html', {'all_products': all_products})
