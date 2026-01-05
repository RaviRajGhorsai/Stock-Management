from rest_framework.routers import DefaultRouter
from .views import CreateStaffView, CreateCustomerView, AdminStaffLoginView

admin_router = DefaultRouter(trailing_slash=False)
admin_router.register(r'login', AdminStaffLoginView, basename='admin_staff_login')
admin_router.register(r'create-staff', CreateStaffView, basename='create_staff')
admin_router.register(r'create-customer', CreateCustomerView, basename='create_customer')

urlpatterns = admin_router.urls