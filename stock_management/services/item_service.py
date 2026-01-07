from django_tenants.utils import schema_context

from stock_management.models import (
    Item
)
from stock_management.serializers.item_serializer import ItemSerializer

def list_items_for_tenant(tenant):
    with schema_context(tenant.schema_name):
        items = Item.objects.all()
        
        return items
    
def get_item_for_tenant(tenant, id=None):
    with schema_context(tenant.schema_name):
        try:
            return Item.objects.get(id=id)
        except Item.DoesNotExist:
            return None

def create_item_for_tenant(tenant, item_data):
    with schema_context(tenant.schema_name):
        serializer = ItemSerializer(data=item_data)
        serializer.is_valid(raise_exception=True)
        
        item = serializer.save()
        
        return item