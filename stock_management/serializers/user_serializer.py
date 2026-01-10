from stock_management.models import (
    StaffUser,
    CustomerUser
) 

from rest_framework import serializers

   
class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffUser
        fields = ['id', 'username', 'email', 'phone', 'role','address', 
                  'gender', 'nid_citizenship_number', 'salary_amount',
                  'hire_date', 'shift_start', 'shift_end', 'image', 'password']

class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['id', 'username', 'phone', 'role', 'address', 
                  'customer_reg_no', 'opening_balance',
                  ]