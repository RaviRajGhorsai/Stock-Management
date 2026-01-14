from django.contrib.auth.password_validation import validate_password
from django.db import transaction

def create_user_service(user_model, data, role=None, tenant=None):
    
    if role not in ['admin', 'superadmin', 'staff', 'customer']:
        raise ValueError("Role must be specified ")

    username = data.get('username')

    if user_model.objects.filter(username=username, role=role).exists():
        raise ValueError("Username already exists for this role")
    
    password = data.pop('password')
    if not password:
        raise ValueError("Password is required")
    
    validate_password(password)
    
    with transaction.atomic():
        
        user = user_model(**data, 
                          role=role,
                          tenant=tenant
                          )
        user.set_password(password)
        user.save()
        
    return user
