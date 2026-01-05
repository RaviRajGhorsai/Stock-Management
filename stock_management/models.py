from django.db import models

# Create your models here.

class Item(models.Model):
    
    name = models.CharField(max_length=100)
    model_no = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    cost_price = models.DecimalField(max_digits=12, decimal_places=2)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} ({self.model_no})"

class Expense(models.Model):
    
    description = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    