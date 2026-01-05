from django.contrib.auth.models import AbstractUser
from django.db import models
from tenants.models import Client

class User(AbstractUser):
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

    phone = models.CharField(max_length=20, blank=True, null=True)

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
