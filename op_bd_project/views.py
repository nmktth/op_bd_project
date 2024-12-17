from django.shortcuts import render
from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def index(request):
    # Главная страница
    return render(request, 'index.html')

def add_product(request):
    if request.method == 'POST':
        url = request.POST.get('ozon')

        if url:
            # Настроим Selenium
            options = Options()
            options.headless = True  # Запуск браузера без окна

            # Укажите путь к Chrome, если он не добавлен в системный путь
            options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'  # Укажите свой путь

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
                price_element = driver.find_element(By.CLASS_NAME, 'v6l_27')  # Убедитесь, что это правильный класс для цены

                # Извлекаем цену
                price = price_element.text.strip()

                # Возвращаем цену в JSON-формате
                return JsonResponse({'price': price})

            except Exception as e:
                driver.quit()
                return JsonResponse({'error': f"Ошибка при парсинге цены: {str(e)}"})

            driver.quit()
    return render(request, 'add_product.html')  # Форма для добавления товара
