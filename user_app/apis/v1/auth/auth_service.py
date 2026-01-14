from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

def login_user_service(username, password):
    user = authenticate(username=username, password=password)
    if not user:
        raise ValueError("Invalid credentials")

    refresh = RefreshToken.for_user(user)

    if user.is_superuser:
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "role": "superuser",
            },
            "tenant": {
                "schema": "public",
                "url": settings.PUBLIC_BASE_URL,  
            }
        }

    tenant = user.tenant
    if not tenant:
        raise ValueError("Tenant not assigned")

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role,
        },
        "tenant": {
            "schema": tenant.schema_name,
            "url": f"http://{tenant.schema_name}.localhost:8000"
        }
    }