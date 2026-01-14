from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from stock_management.serializers.item_serializer import ItemSerializer
from stock_management.services.item_service import (
    list_items_for_tenant,
    get_item_for_tenant,
    create_item_for_tenant
)
from stock_management.apis.v1.auth.permissions import (
    IsAdminOrStaffUser
)

from django_tenants.utils import schema_context

# Need to specify which tenant's schema to use based on the authenticated user (line 27)
class ItemView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAuthenticated, IsAdminOrStaffUser]       

    def list(self, request, *args, **kwargs):
        with schema_context(request.user.tenant.schema_name):
            print(request.user.tenant.schema_name)
            items_data = list_items_for_tenant()
            
            return Response({"data": items_data}, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        with schema_context(request.user.tenant.schema_name):
            item = get_item_for_tenant(id=pk)
            if item is None:
                return Response({'status': 'error', 'message': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = ItemSerializer(item)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        with schema_context(request.user.tenant.schema_name):
            item = create_item_for_tenant(request.data)
            serializer = ItemSerializer(item)
            
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
            