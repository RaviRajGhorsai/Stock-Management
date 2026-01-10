
from stock_management.models import (
    Item
)
from stock_management.serializers.item_serializer import ItemSerializer

def list_items_for_tenant():
    
    items = Item.objects.all()
    
    serializer = ItemSerializer(items, many=True)
    return serializer.data 
    
def get_item_for_tenant(id=None):
    
        try:
            return Item.objects.get(id=id)
        except Item.DoesNotExist:
            return None

def create_item_for_tenant(item_data):
    
    serializer = ItemSerializer(data=item_data)
    serializer.is_valid(raise_exception=True)
    
    item = serializer.save()
    
    return item