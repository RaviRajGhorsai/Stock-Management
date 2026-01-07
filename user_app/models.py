from django.contrib.auth.models import AbstractUser
from django.db import models
from tenants.models import Client

class BaseUser(AbstractUser):
    ROLE_CHOICES = (
        ('superuser', 'Superuser'),
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='customer'
    )

    tenant = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='logos/', blank=True, null=True)

    def is_admin_user(self):
        return self.role == 'admin'

    def is_staff_user(self):
        return self.role == 'staff'

    def is_customer_user(self):
        return self.role == 'customer'

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'superuser'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"

class AdminUser(BaseUser):
    organization_name = models.CharField(max_length=150)
    organization_registration_number = models.CharField(max_length=50)
    active_duration = models.IntegerField(default=0)  # in days
    sales_on = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    logo_image = models.ImageField(upload_to='logos/', blank=True, null=True)


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
    