from django.http import JsonResponse
from rest_framework import viewsets
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
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
        
        
