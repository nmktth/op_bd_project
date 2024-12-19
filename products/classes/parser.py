import re
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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
        
        def check_exists(xpath):
            try:
                self.driver.find_element(By.XPATH, xpath)
            except NoSuchElementException:
                return False
            return True
        
        def is_loaded():
            if not check_exists('//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span'):
                if not check_exists('//*[@id="layoutPage"]/div[1]/div[3]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span'):
                    return False
            return True


        try:
            if not is_loaded():
                self.driver.implicitly_wait(1)
                if not is_loaded():
                    self.driver.refresh()

                    # Подождем некоторое время, чтобы страница обновилась
                    self.driver.implicitly_wait(2)
            
            
            # Ищем элемент с ценой
            try:
                price_element = self.driver.find_element(By.XPATH, '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span')
            except:
                price_element = self.driver.find_element(By.XPATH, '//*[@id="layoutPage"]/div[1]/div[3]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span')

            # Извлекаем цену и убираем все символы, кроме цифр
            price_text = price_element.text.strip()
            price = re.sub(r'\D', '', price_text)

            # Ищем название товара (например, через другой селектор)
            try:
                name_element = self.driver.find_element(By.XPATH, '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[1]/div[1]/div[2]/div/div/div/div[1]/h1') 
            except:
                name_element = self.driver.find_element(By.XPATH, '//*[@id="layoutPage"]/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/div/div/div[1]/h1')
            
            name = name_element.text.strip()
            
            return price, name
        except Exception as e:
            return e
        finally:
            # self.driver.close()
            pass
    