from django_tenants.utils import schema_context

from user_app.models import (
    StaffUser,
    CustomerUser
)

def list_staff_user_for_tenant_service(tenant):
    with schema_context(tenant.schema_name):
        return StaffUser.objects.all()
    
def get_staff_user_for_tenant_service(tenant, id=None):
    with schema_context(tenant.schema_name):
        try:
            return StaffUser.objects.get(id=id)
        except StaffUser.DoesNotExist:
            return None
        
def list_customer_user_for_tenant_service(tenant):
    with schema_context(tenant.schema_name):
        return CustomerUser.objects.all()

def get_customer_user_for_tenant_service(tenant, id=None):
    with schema_context(tenant.schema_name):
        try:
            return CustomerUser.objects.get(id=id)
        except CustomerUser.DoesNotExist:
            return None