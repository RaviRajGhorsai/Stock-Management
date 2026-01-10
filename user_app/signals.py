from pathlib import Path
from django.db.models.signals import post_save
from django.dispatch import receiver
from user_app.models import AdminUser
from tenants.models import Client, Domain
from django.db import transaction
from django_tenants.utils import schema_context
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

@receiver(post_save, sender=AdminUser)
def create_tenant_for_admin(sender, instance, created, **kwargs):
    
    domain_name = os.getenv("TENANT_DOMAIN")
    
    if created and instance.is_admin_user():
        schema_name = instance.username.lower()
        username = instance.username
        
        # Make sure tenant creation is in the public schema
        with schema_context('public'), transaction.atomic():
            # Create tenant (this will create the new schema)
            tenant = Client(schema_name=schema_name, name=username)
            tenant.save()  # This triggers TenantMixin and creates the schema

            # Create the domain
            Domain.objects.create(
                domain=f"{schema_name}.{domain_name}",
                tenant=tenant,
                is_primary=True
            )

            # Assign tenant to user WITHOUT triggering post_save again
            AdminUser.objects.filter(id=instance.id).update(tenant=tenant)
              
