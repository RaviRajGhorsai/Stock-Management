from django.apps import AppConfig
from django.contrib.auth import get_user_model
import os
from django.db import OperationalError, ProgrammingError

class UserAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_app'

    def ready(self):
        import user_app.signals
        
        User = get_user_model()
       
        try:
             
            username = os.getenv("DJANGO_SUPERUSER_USERNAME")
            email = os.getenv("DJANGO_SUPERUSER_EMAIL")
            password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

            if not username or not password:
                return

            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
        except (OperationalError, ProgrammingError):
            pass
        