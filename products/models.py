# products/models.py
from datetime import date
from django import utils
from django.db import models

class Product(models.Model):
    url = models.URLField(unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # DecimalField
    start_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # DecimalField
    
    percent = models.IntegerField(default=100)
    cur_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # DecimalField
    
    created = models.DateTimeField(default=utils.timezone.now)

    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            'url': self.url,
            'name': self.name,

            'price': str(self.price),  # Конвертируем цену в строку для JSON
            'percent': self.percent,
            'cur_percent': self.cur_percent
        }
