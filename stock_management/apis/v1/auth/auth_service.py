
from rest_framework_simplejwt.tokens import RefreshToken
from user_app.models import AdminUser


def login_user_service(username, password):
    
    try:
        admin = AdminUser.objects.get(username=username)
    except AdminUser.DoesNotExist:
        raise ValueError("Invalid credentials")
    
    if not admin.check_password(password):
        raise ValueError("Invalid credentials")
    
    refresh = RefreshToken.for_user(admin)
    
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user_id": admin.id,
        "username": admin.username,
        "role": admin.role,
        "tenant": {
            "id": admin.tenant.id if admin.tenant else None,
            "schema_name": admin.tenant.schema_name if admin.tenant else None,
            "name": admin.tenant.name if admin.tenant else None,
            }
    }
    

def check_user_role(user):
    
    """ This is used to check user permissions
    Only admin and staff users are allowed to perform certain actions.
    """
    
    if not (user.is_admin_user() or user.is_staff_user()):
        return None
    else:
        return True