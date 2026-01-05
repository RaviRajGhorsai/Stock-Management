from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from .services import create_user
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class CreateUserView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]  
    permission_classes = [permissions.IsAuthenticated]  
    
    role = None  # to be defined in subclasses
    
    def create(self, request, *args, **kwargs):
        if not request.user.is_admin():
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
        
        data = request.data
        try:
            user = create_user(
                username=data.get('username'),
                email=data.get('email'),
                phone=data.get('phone'),
                password=data.get('password'),
                tenant=request.user.tenant,
                role=self.role
            )
            return JsonResponse({'status': 'success', 'user_id': user.id, 'username': user.username}, status=201)
        except ValueError as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

class CreateStaffView(CreateUserView):
    role = 'staff'
    
class CreateCustomerView(CreateUserView):
    role = 'customer'
    
class AdminStaffLoginView(viewsets.ViewSet):
    
    def create(self, request, *args, **kwargs):
        
        name = request.data.get('username')
        password = request.data.get('password')
        
        
        user = authenticate(request, username=name, password=password)
        if user is None:
            
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
        if user.role not in ['admin', 'staff']:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        return JsonResponse({
            'status': 'success',
            'username': user.username,
            'role': user.role,
            'tenant': user.tenant.schema_name if user.tenant else None,
            'access': access_token,
            'refresh': refresh_token
        })