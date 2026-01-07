from rest_framework import status
from rest_framework.response import Response

def check_user_role(user):
    
    """ This is used to check user permissions
    Only admin and staff users are allowed to perform certain actions.
    """
    
    if not (user.is_admin_user() or user.is_staff_user()):
        return None
    else:
        return True