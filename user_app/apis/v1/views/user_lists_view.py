from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user_app.apis.v1.auth.auth_service import check_user_role
from user_app.serializers.user_serializer import (
    StaffUserSerializer,
    CustomerUserSerializer
)

from user_app.services.user_detail_service import (
    list_staff_user_for_tenant_service,
    get_staff_user_for_tenant_service,
    list_customer_user_for_tenant_service,
    get_customer_user_for_tenant_service
)

class StaffUserView(viewsets.ViewSet):
    
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        
        user = request.user
        
        auth_response = check_user_role(user, role="admin")
        if auth_response is None:
            return Response({'status': 'error', 'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        tenant = user.tenant
        
        staff_users_data = list_staff_user_for_tenant_service(tenant)
        
        serializer = StaffUserSerializer(staff_users_data, many=True)
        
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        
        user = request.user
        
        auth_response = check_user_role(user, role="admin")
        if auth_response is None:
            return Response({'status': 'error', 'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        tenant = user.tenant
        
        staff_user = get_staff_user_for_tenant_service(tenant, id=pk)
        if staff_user is None:
            return Response({'status': 'error', 'message': 'Staff user not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StaffUserSerializer(staff_user)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

class CustomerUserView(viewsets.ViewSet):
    
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        
        user = request.user
        
        auth_response = check_user_role(user)
        if auth_response is None:
            return Response({'status': 'error', 'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        tenant = user.tenant
        
        customer_users_data = list_customer_user_for_tenant_service(tenant)
        
        serializer = CustomerUserSerializer(customer_users_data, many=True)
        
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        
        user = request.user
        
        auth_response = check_user_role(user)
        if auth_response is None:
            return Response({'status': 'error', 'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        tenant = user.tenant
        
        customer_user = get_customer_user_for_tenant_service(tenant, id=pk)
        
        if customer_user is None:
            return Response({'status': 'error', 'message': 'Customer user not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CustomerUserSerializer(customer_user)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    