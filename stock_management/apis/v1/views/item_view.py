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
from stock_management.services.auth_service import check_user_role


# Need to specify which tenant's schema to use based on the authenticated user (line 27)
class ItemView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAuthenticated]       

    def list(self, request, *args, **kwargs):
        
        user = request.user
        
        auth_response = check_user_role(user)
        if auth_response is None:
            return Response({'status': 'error', 'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        tenant = user.tenant
    
        items_data = list_items_for_tenant(tenant)
        
        return Response({"data": items_data}, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        
        user = request.user
        
        auth_response = check_user_role(user)
        if auth_response is None:
            return Response({'status': 'error', 'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        tenant = user.tenant
        
        item = get_item_for_tenant(tenant, id=pk)
        if item is None:
            return Response({'status': 'error', 'message': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ItemSerializer(item)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        
        user = request.user
        
        auth_response = check_user_role(user)
        if auth_response is None:
            return Response({'status': 'error', 'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        tenant = user.tenant
        
        item = create_item_for_tenant(tenant, request.data)
        serializer = ItemSerializer(item)
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        