import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class Parser:
    
    def __init__(self):
        options = Options()
        options.add_argument("--log-level=3")

        # Укажи путь к Chrome, если он не добавлен в системный путь
        options.binary_location = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
    def url(self, url):
        self.driver.get(url)
        

        # Подождем несколько секунд, чтобы страница полностью загрузилась
        self.driver.implicitly_wait(5)

        try:
            try:
                WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span')))
            except:
                time.sleep(1)
                self.driver.refresh()

            # Подождем некоторое время, чтобы страница обновилась
            self.driver.implicitly_wait(5)
            
            
            
            # Ищем элемент с ценой
            price_element = self.driver.find_element(By.XPATH, '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span')  # Убедись, что это правильный класс для цены

            # Извлекаем цену и убираем все символы, кроме цифр
            price_text = price_element.text.strip()
            price = re.sub(r'\D', '', price_text)

            # Ищем название товара (например, через другой селектор)
            name_element = self.driver.find_element(By.XPATH, '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[1]/div[1]/div[2]/div/div/div/div[1]/h1')  # Убедитесь, что это правильный класс для названия товара
            name = name_element.text.strip()
            
            return price, name
        except Exception as e:
            return e
        finally:
            # self.driver.close()
            pass
    