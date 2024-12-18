from decimal import Decimal
from ..models import Product

class DB:
    def get_all():
        return Product.objects.all()
    
    def get(url) -> Product:
        return Product.objects.get(url=url)
        
    def update(url, price):
        prod = DB.get(url)
        prod.price = Decimal(price)
        prod.save()
    
    def create(name, price, url):
        Product.objects.create(url=url, name=name, price = Decimal(price)).save()