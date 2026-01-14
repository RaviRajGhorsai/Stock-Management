from user_app.models import (
    AdminUser,
    StaffUser,
    CustomerUser
) 

from rest_framework import serializers

   
class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ['id', 'username', 'email', 'phone', 'role', 'tenant', 
                  'organization_name', 'organization_registration_number', 
                  'address', 'active_duration', 'sales_on', 'image', 'password']
        
class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffUser
        fields = ['id', 'username', 'email', 'phone', 'role','address', 
                  'gender', 'nid_citizenship_number', 'salary_amount', 'tenant',
                  'hire_date', 'shift_start', 'shift_end', 'image', 'password']

class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['id', 'username', 'phone', 'role', 'address', 'tenant',
                  'customer_reg_no', 'opening_balance',
                  ]