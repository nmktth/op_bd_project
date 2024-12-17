# products/models.py
from django.db import models

class Product(models.Model):
    url = models.URLField(unique=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Убедитесь, что используется DecimalField

    def __str__(self):
        return self.name
