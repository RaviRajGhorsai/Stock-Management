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
from user_app.apis.v1.auth.permissions import (
    IsSuperAdminUser,
    IsAdminUser,
    IsAdminOrStaffUser
)

class CreateUserView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]  
    permission_classes = [permissions.IsAuthenticated]  
    
    role = None  # to be defined in subclasses
    serializer_class = None
    user_model = None

    requires_tenant = False  

    def get_tenant(self, request):
        if self.requires_tenant:
            if not request.user.tenant:
                raise ValueError("Tenant context required")
            return request.user.tenant
        return None
   
    def create(self, request, *args, **kwargs):
        
        # get serializer class based on role
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
           
        try:
            
            user = create_user_service(
               user_model=self.user_model,
               data=serializer.validated_data,
               role=self.role,
               tenant=self.get_tenant(request)
            )
        
            return Response({'status': 'success',
                             'user_id': user.id, 
                             'username': user.username,
                             'role': user.role,
                             'tenant': user.tenant
                             }, status=201)
        except ValueError as e:
            return Response({'status': 'error', 'message': str(e)}, status=400)

    
class CreateAdminView(CreateUserView):
    permission_classes = [IsSuperAdminUser]
    
    serializer_class = AdminUserSerializer
    user_model = AdminUser
    role = 'admin'
    requires_tenant = False
    
class CreateStaffView(CreateUserView):
    permission_classes = [IsAdminUser]
    
    serializer_class = StaffUserSerializer
    user_model = StaffUser
    role = 'staff'
    requires_tenant = True
    
class CreateCustomerView(CreateUserView):
    permission_classes = [IsAdminOrStaffUser]
    
    serializer_class = CustomerUserSerializer
    user_model = CustomerUser
    role = 'customer'
    requires_tenant = True