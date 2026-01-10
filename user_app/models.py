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
    
    tenant = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name='admin_user',
        null=True,
        blank=True
    )
    
    organization_name = models.CharField(max_length=150)
    organization_registration_number = models.CharField(max_length=50)
    active_duration = models.IntegerField(default=0)  # in days
    sales_on = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    