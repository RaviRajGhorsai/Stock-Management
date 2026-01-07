from rest_framework.routers import DefaultRouter
from user_app.apis.v1.views.user_create_view import CreateStaffView, CreateCustomerView
from user_app.apis.v1.auth.admin_login_view import AdminStaffLoginView

admin_router = DefaultRouter(trailing_slash=False)
admin_router.register(r'login', AdminStaffLoginView, basename='admin_staff_login')
admin_router.register(r'create-staff', CreateStaffView, basename='create_staff')
admin_router.register(r'create-customer', CreateCustomerView, basename='create_customer')

urlpatterns = admin_router.urls