from rest_framework.response import Response
from django_tenants.utils import schema_context
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user_app.serializers.user_serializer import (
    StaffUserSerializer,
    CustomerUserSerializer
)
from user_app.apis.v1.auth.permissions import (
    IsAdminUser,
    IsAdminOrStaffUser
)
from user_app.services.user_detail_service import (
    list_staff_user_service,
    get_staff_user_service,
    list_customer_user_service,
    get_customer_user_service
)

class StaffUserView(viewsets.ViewSet):
    
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def list(self, request, *args, **kwargs):
        with schema_context(request.user.tenant.schema_name):
            staff_users_data = list_staff_user_service()
            
            serializer = StaffUserSerializer(staff_users_data, many=True)
            
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        
    def retrieve(self, request, pk=None, *args, **kwargs):
        with schema_context(request.user.tenant.schema_name):
            staff_user = get_staff_user_service(id=pk)
            if staff_user is None:
                return Response({'status': 'error', 'message': 'Staff user not found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = StaffUserSerializer(staff_user)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

class CustomerUserView(viewsets.ViewSet):
    
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAuthenticated, IsAdminOrStaffUser]

    def list(self, request, *args, **kwargs):
        with schema_context(request.user.tenant.schema_name):
            customer_users_data = list_customer_user_service()
            
            serializer = CustomerUserSerializer(customer_users_data, many=True)
            
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        with schema_context(request.user.tenant.schema_name):
            customer_user = get_customer_user_service(id=pk)
            
            if customer_user is None:
                return Response({'status': 'error', 'message': 'Customer user not found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = CustomerUserSerializer(customer_user)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    