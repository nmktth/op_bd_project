import re
import json
import time
import requests
from selenium.common.exceptions import NoSuchElementException
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
        options.add_argument("--user-data-dir=C:\\Users\\hecke\AppData\\Local\\Google\Chrome\\User Data")
        options.add_argument("--profile-directory=Default")

        # Укажи путь к Chrome, если он не добавлен в системный путь
        options.binary_location = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.loop()
        
    def check_exists(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True
        
    def url(self, url):
        self.driver.get(url)
        
        
        def is_loaded():
            if not self.check_exists('//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span'):
                if not self.check_exists('//*[@id="layoutPage"]/div[1]/div[3]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span'):
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
                price_element = self.driver.find_element(By.XPATH, '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span')  # Убедись, что это правильный класс для цены
            except:
                price_element = self.driver.find_element(By.XPATH, '//*[@id="layoutPage"]/div[1]/div[3]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span')


            # Извлекаем цену и убираем все символы, кроме цифр
            price_text = price_element.text.strip()
            price = re.sub(r'\D', '', price_text)
            
            return price
        except Exception as e:
            return e
        finally:
            # self.driver.close()
            pass
    
    
    def loop(self):
        time.sleep(2)
        while True:
            resp = requests.get("http://127.0.0.1:8000/get-all/")
            products = json.loads(resp.content)['data']
            
            for product in products:
                
                url = product["url"]
                checked_price = float(self.url(url))
                print(f"{product['price']} --- {checked_price}")
                
                if float(product["price"]) != checked_price:
                    requests.post("http://127.0.0.1:8000/update/", {"url": url, "price": checked_price})
                prod = json.loads(requests.get("http://127.0.0.1:8000/get", params={"url": product["url"]}).content)['data']
                
                cur_percent = float(prod['cur_percent']) * -1
                percent = float(prod['percent'])
                
                if cur_percent >= percent:
                
                    if not self.check_exists('//*[@id="layoutPage"]/div[1]/div[3]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[4]/div/div/div[1]/div/div/div/div[1]/button/div[2]'):
                        print("NOT LOGGED IN?\n"*10)
                    else:
                        self.driver.find_element(By.XPATH, '//*[@id="layoutPage"]/div[1]/div[3]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[4]/div/div/div[1]/div/div/div/div[1]/button/div[2]').click()
                        print("ADDED")
                        requests.get("http://127.0.0.1:8000/delete", params={"url": product["url"]})

                


            time.sleep(1800)