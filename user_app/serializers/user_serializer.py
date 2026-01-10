from user_app.models import (
    AdminUser
) 

from rest_framework import serializers

   
class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ['id', 'username', 'email', 'phone', 'role', 'tenant', 
                  'organization_name', 'organization_registration_number', 
                  'address', 'active_duration', 'sales_on', 'image', 'password']
        