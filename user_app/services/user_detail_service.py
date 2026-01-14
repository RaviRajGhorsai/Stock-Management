
from user_app.models import (
    StaffUser,
    CustomerUser
)

def list_staff_user_service():
    
    return StaffUser.objects.all()
    
def get_staff_user_service(id=None):
    
    try:
        return StaffUser.objects.get(id=id)
    except StaffUser.DoesNotExist:
        return None
        
def list_customer_user_service():
    
    return CustomerUser.objects.all()

def get_customer_user_service(id=None):

    try:
        return CustomerUser.objects.get(id=id)
    except CustomerUser.DoesNotExist:
        return None