import os
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


paths = {
    'prices': [
        '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span',
        '//*[@id="layoutPage"]/div[1]/div[3]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span',
        '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span',
        '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span',
        '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div[3]/div[1]/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span',
        '//*[@id="layoutPage"]/div[1]/div[3]/div[3]/div[2]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span',
        '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div/div[1]/span[1]',
        '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div/div[1]/span[1]',
        '//*[@id="layoutPage"]/div[1]/div[3]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div/div[1]/span[1]'
        
        ],
    'add': [
        '//*[@id="layoutPage"]/div[1]/div[3]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[4]/div/div/div[1]/div/div/div/div[1]/button',
        '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div[3]/div[1]/div[4]/div/div/div[1]/div/div/div/div[1]/button',
        '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div/div/div[4]/div/div/div[1]/div/div/div/div[1]/button',
        '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[4]/div/div/div[1]/div/div/div/div/div[1]/div[1]/button',
        '//*[@id="layoutPage"]/div[1]/div[3]/div[3]/div[2]/div/div/div[1]/div[2]/div[1]/div[4]/div/div/div[1]/div/div/div/div[1]/button'
    ]
    
}


class Parser:
    
    def __init__(self):
        self.token = "7624024176:AAH1sj-vmez_yH5syCBAQzOTRdn7OBfpkJk"
        self.chats = [1395010208, 6990242186]
        
        options = Options()
        options.add_argument("--log-level=3")
        options.add_argument("--disable-webgl")
        options.add_argument("--disable-permissions-api")
        options.add_argument(f"--user-data-dir=C:\\Users\\{os.getlogin()}\AppData\\Local\\Google\Chrome\\User Data")
        options.add_argument("--profile-directory=Default")

        # Укажи путь к Chrome, если он не добавлен в системный путь
        options.binary_location = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.loop()
        
    def check_exists(self, xpath):
        try:
            el = self.driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return None
        return el
    
    def tg_notificate(self, text):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        
        for username in self.chats:
            print(requests.post(url, data={'chat_id': username, 'text': text, 'parse_mode': "Markdown"}).content)

        
    def url(self, url):
        self.driver.get(url)
        
        
        def is_loaded():
            for price in paths['prices']:
                if self.check_exists(price):
                    return True
            return True

        if not is_loaded():
            self.driver.implicitly_wait(2)
            if not is_loaded():
                self.driver.refresh()
        
        time.sleep(3)
        

        check = self.check_exists('//*[@id="reload-button"]')
        if check is not None: 
            self.driver.refresh()
        
        # Ищем элемент с ценой
        for path in paths['prices']:
            price_element = self.check_exists(path)
            if price_element is not None: break



        # Извлекаем цену и убираем все символы, кроме цифр
        price_text = price_element.text.strip()
        price = re.sub(r'\D', '', price_text)
        
        return price
    
    
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
                    self.tg_notificate(f"Изменилась цена на товар [{product['name']}]({product['url']})\nБыло: {product['price']}\nСтало: {checked_price}")
                    requests.post("http://127.0.0.1:8000/update/", {"url": url, "price": checked_price})
                prod = json.loads(requests.get("http://127.0.0.1:8000/get", params={"url": product["url"]}).content)['data']
                
                cur_percent = float(prod['cur_percent']) * -1
                percent = float(prod['percent'])
                
                if cur_percent >= percent:
                    
                    for path in paths['add']:
                        el = self.check_exists(path)
                        if el: break
                        
                    if not el:
                        print("NO\n" * 10)
                        return
                    
                    el.click()
                    print("ADDED")
                    
                    self.tg_notificate(f"Товар [{product['name']}]({product['url']}) был добавлен в корзину!")
                    requests.get("http://127.0.0.1:8000/delete", params={"url": product["url"]})

                


            time.sleep(1800)