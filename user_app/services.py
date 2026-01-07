

def create_user(user_model, data, tenant=None, role=None):
    
    
    if role not in ('admin', 'staff', 'customer'):
        raise ValueError("Role must be 'admin', 'staff', or 'customer'")

    username = data.get('username')

    if user_model.objects.filter(username=username, role=role).exists():
        raise ValueError("Username already exists for this role")
    
    password = data.pop('password')
    if not password:
        raise ValueError("Password is required")
     
    user = user_model(**data, tenant=tenant, role=role)
    user.set_password(password)
    user.save()
    return user
