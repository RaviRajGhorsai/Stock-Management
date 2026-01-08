from django.core.management.base import BaseCommand
from django_tenants.utils import schema_context
from django.db import transaction
import os
from tenants.models import Client, Domain

class Command(BaseCommand):
    help = "Create public tenant and domain if missing"

    def handle(self, *args, **options):
        
        schema = "public"
        domain = os.getenv("TENANT_DOMAIN")

        if not domain:
            self.stdout.write("❌ TENANT_DOMAIN not set")
            return

        if Client.objects.filter(schema_name=schema).exists():
            self.stdout.write("ℹ️ Public tenant already exists")
            return

        with transaction.atomic():
            tenant = Client.objects.create(
                schema_name=schema,
                name="Public Tenant"
            )

            Domain.objects.create(
                domain=domain,
                tenant=tenant,
                is_primary=True
            )

        self.stdout.write("✅ Public tenant + domain created")
