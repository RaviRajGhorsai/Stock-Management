from django.db import models
from user_app.models import BaseUser
from tenants.models import Client

# Create your models here.

class StaffUser(BaseUser):
    
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    
    gender = models.CharField(max_length=10,
                              choices=GENDER_CHOICES,
                              )
    nid_citizenship_number = models.CharField(max_length=20, null=True, blank=True)
    salary_amount = models.DecimalField(max_digits=12, decimal_places=2,)
    hire_date = models.DateField(null=True, blank=True)
    shift_start = models.TimeField(null=True, blank=True)
    shift_end = models.TimeField(null=True, blank=True)
    
class CustomerUser(BaseUser):
    customer_reg_no = models.CharField(max_length=20, null=True, blank=True)
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    due_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    

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
    
class Bill(models.Model):
    
    PAYMENT_CHOICES = (
        ("online", "Online"),
        ("cash", "Cash"),
        ("due", "Due")
    )
    
    customer_name = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    name_of_product = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    discount_rate = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=7, choices=PAYMENT_CHOICES)
    