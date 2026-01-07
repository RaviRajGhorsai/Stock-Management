from rest_framework.routers import DefaultRouter
from user_app.views.admin_user_view import CreateStaffView, CreateCustomerView
from user_app.auth.admin_login_view import AdminStaffLoginView

admin_router = DefaultRouter(trailing_slash=False)
admin_router.register(r'login', AdminStaffLoginView, basename='admin_staff_login')
admin_router.register(r'create-staff', CreateStaffView, basename='create_staff')
admin_router.register(r'create-customer', CreateCustomerView, basename='create_customer')

urlpatterns = admin_router.urls