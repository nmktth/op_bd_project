import re
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


paths = {
    'prices': [
        '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span',
        '//*[@id="layoutPage"]/div[1]/div[3]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span',
        '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span',
        '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span',
        '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div[3]/div[1]/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span',
        '//*[@id="layoutPage"]/div[1]/div[3]/div[3]/div[2]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span',
        '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div/div[1]/span[1]'
        ],
    'names': [
        '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[1]/div[1]/div[2]/div/div/div/div[1]/h1',
        '//*[@id="layoutPage"]/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/div/div/div[1]/h1'
    ]
    
}

class Parser:
    
    def __init__(self):
        options = Options()
        options.add_argument("--log-level=3")
        options.add_argument("--disable-webgl")
        options.add_argument("--disable-permissions-api")

        # Укажи путь к Chrome, если он не добавлен в системный путь
        options.binary_location = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
    def url(self, url):
        self.driver.get(url)
        
        def check_exists(xpath):
            try:
                el = self.driver.find_element(By.XPATH, xpath)
            except NoSuchElementException:
                return None
            return el
        
        
        
        def is_loaded():
            for price in paths['prices']:
                if check_exists(price):
                    return True
            return True


        try:
            if not is_loaded():
                self.driver.implicitly_wait(2)
                if not is_loaded():
                    self.driver.refresh()
            
            time.sleep(5)
            

            check = check_exists('//*[@id="reload-button"]')
            if check is not None: 
                self.driver.refresh()
            
            
            # Ищем элемент с ценой
            for path in paths['prices']:
                price_element = check_exists(path)
                if price_element is not None: break
                
            # Извлекаем цену и убираем все символы, кроме цифр
            price_text = price_element.text.strip()
            price = re.sub(r'\D', '', price_text)

            # Ищем название товара (например, через другой селектор)
            for path in paths['names']:
                name_element = check_exists(path)
                if name_element is not None: break
            
            name = name_element.text.strip()
            
            return price, name
        except Exception as e:
            return e
        finally:
            # self.driver.close()
            pass
    