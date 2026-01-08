from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from .models import AdminUser, BaseUser
from tenants.models import Client, Domain
from django.db import transaction
from django_tenants.utils import schema_context

@receiver(post_save, sender=AdminUser)
def create_tenant_for_admin(sender, instance, created, **kwargs):
    
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
                domain=f"{schema_name}.stock-management-j34y.onrender.com",
                tenant=tenant,
                is_primary=True
            )

            # Assign tenant to user WITHOUT triggering post_save again
            AdminUser.objects.filter(id=instance.id).update(tenant=tenant)
              
@receiver(post_migrate, sender=BaseUser)
def create_default_public_tenant(sender, **kwargs):
    
    if not Client.objects.filter(schema_name='public').exists():
        with schema_context('public'), transaction.atomic():
            tenant = Client(schema_name='public', name='public tenant')
            tenant.save()

            Domain.objects.create(
                domain='public.localhoststock-management-j34y.onrender.com',
                tenant=tenant,
                is_primary=True
            )