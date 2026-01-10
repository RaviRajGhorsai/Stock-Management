from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_tenants.utils import schema_context

from stock_management.services.create_user_service import create_user_service
from stock_management.models import (
    StaffUser,
    CustomerUser
)
from stock_management.apis.v1.auth.permissions import (
    IsAdminUser,
    IsAdminOrStaffUser
)
from stock_management.serializers.user_serializer import (
    StaffUserSerializer,
    CustomerUserSerializer
)

class CreateUserView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]  
    permission_classes = [permissions.IsAuthenticated]  
    
    role = None  # to be defined in subclasses
    serializer_class = None
    user_model = None
    
    def create(self, request, *args, **kwargs):
        print("\n🔥🔥🔥 VIEW WAS CALLED! 🔥🔥🔥\n")
        # get serializer class based on role
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
           
        try:
            print("\n\nuser: ", request.user)
            print("Tenant: ", request.tenant)
            tenant = request.tenant
            with schema_context(tenant.schema_name):
                user = create_user_service(
                user_model=self.user_model,
                data=serializer.validated_data,
                role=self.role 
                )
            
                return Response({'status': 'success',
                                'user_id': user.id, 
                                'username': user.username,
                                'role': user.role,
                                }, status=201)
        except ValueError as e:
            return Response({'status': 'error', 'message': str(e)}, status=400)

class CreateStaffView(CreateUserView):
    permission_classes = [IsAdminUser]
    
    serializer_class = StaffUserSerializer
    user_model = StaffUser
    role = 'staff'
    
class CreateCustomerView(CreateUserView):
    permission_classes = [IsAdminOrStaffUser]
    
    serializer_class = CustomerUserSerializer
    user_model = CustomerUser
    role = 'customer'
    