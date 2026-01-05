from django.contrib.auth import get_user_model

User = get_user_model()

def create_user(username, password, email, tenant, phone, role):
    if role not in ('staff', 'customer'):
        raise ValueError("Role must be 'staff' or 'customer'")

    if User.objects.filter(username=username, role=role).exists():
        raise ValueError("Username already exists")
    
    return User.objects.create_user(
        username=username,
        password=password,
        email=email,
        phone=phone,
        tenant=tenant,
        role=role
    )
