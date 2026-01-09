from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response


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
    

def check_user_role(user, role=None):
    
    """ This is used to check user permissions
    Only admin and staff users are allowed to perform certain actions.
    """
    if role is None:
        if not (user.is_admin_user() or user.is_staff_user()):
            return None
        else:
            return True
    else:
        if not user.role == role:
            return None
        else:
            return True