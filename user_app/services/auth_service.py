from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

def login_user_service(username, password):
    
    user = authenticate(username=username, password=password)
    
    if user is None:
            
        raise ValueError('Invalid credentials')
        
    if user.role not in ['admin', 'staff']:
        raise ValueError('Unauthorized')
    
    refresh = RefreshToken.for_user(user)
    
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user_id": user.id,
        "username": user.username,
        "role": user.role
    }
    
    