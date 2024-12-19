from decimal import Decimal
from ..models import Product

class DB:
    @staticmethod
    def get_all():
        return Product.objects.all()
    
    @staticmethod
    def delete(url):
        pr = Product.objects.filter(url=url)
        if pr:
            pr.delete()
    
    @staticmethod
    def get(url) -> Product:
        try:
            return Product.objects.get(url=url)
        except Product.DoesNotExist:
            return None
        
    @staticmethod
    def update_price(url, price):
        def get_change(current, previous):
            if current == previous:
                return 0.00
            try:
                return ((current - previous) / previous) * 100.0
            except ZeroDivisionError:
                return 0.00
        
        prod = DB.get(url)
        if prod is None: return
        
        prod.price = Decimal(price)
        prod.cur_percent = Decimal(get_change(price, float(prod.start_price)))
        prod.save()
        
    @staticmethod
    def update_percent(url, percent):
        
        prod = DB.get(url)
        
        prod.percent = percent
        prod.save()
    
    @staticmethod
    def create(name, price, url):
        if DB.get(url) is None:
            Product.objects.create(url=url, name=name, price = Decimal(price), start_price = Decimal(price)).save()