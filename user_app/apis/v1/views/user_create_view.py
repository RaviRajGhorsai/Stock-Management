from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from user_app.services.create_user import create_user_service

from user_app.models import (
    AdminUser,
    StaffUser,
    CustomerUser
)
from user_app.serializers.user_serializer import (
    AdminUserSerializer,
    StaffUserSerializer,
    CustomerUserSerializer
)

class CreateUserView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]  
    permission_classes = [permissions.IsAuthenticated]  
    
    role = None  # to be defined in subclasses
    
    def get_serializer_class(self):
        if self.role == 'admin':
            return AdminUserSerializer
        elif self.role == 'staff':
            return StaffUserSerializer
        elif self.role == 'customer':
            return CustomerUserSerializer
        return None

    def get_user_model(self):
        if self.role == 'admin':
            return AdminUser
        elif self.role == 'staff':
            return StaffUser
        elif self.role == 'customer':
            return CustomerUser
        return None
    
    def create(self, request, *args, **kwargs):
        
        if not request.user.is_admin_user():
            return Response({'status': 'error', 'message': 'Unauthorized'}, status=403)
        
        # get serializer class based on role
        serializer_class = self.get_serializer_class()
        if not serializer_class:
            return Response({'status': 'error', 'message': 'Invalid role'}, status=400)
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
           
        try:
            
            user = create_user_service(
               user_model=self.get_user_model(),
               data=serializer.validated_data,
               tenant=request.user.tenant,
               role=self.role 
            )
        
            return Response({'status': 'success',
                             'user_id': user.id, 
                             'username': user.username,
                             'role': user.role,
                            'tenant': user.tenant.schema_name
                             }, status=201)
        except ValueError as e:
            return Response({'status': 'error', 'message': str(e)}, status=400)

class CreateStaffView(CreateUserView):
    role = 'staff'
    
class CreateCustomerView(CreateUserView):
    role = 'customer'
    
class CreateAdminView(CreateUserView):
    role = 'admin'