from rest_framework.routers import DefaultRouter

from user_app.apis.v1.views.user_login_view import UserLoginView
from user_app.apis.v1.views.user_create_view import (
    CreateAdminView,
    CreateStaffView,
    CreateCustomerView
)

from user_app.apis.v1.views.user_lists_view import (
    StaffUserView,
    CustomerUserView
)

admin_router = DefaultRouter(trailing_slash=False)

admin_router.register(r'login', UserLoginView, basename='user_login')
admin_router.register(r'create_admin', CreateAdminView, basename='create_admin')
admin_router.register(r'create_staff', CreateStaffView, basename='create_staff')
admin_router.register(r'create_customer', CreateCustomerView, basename='create_customer')
admin_router.register(r'staff', StaffUserView, basename='staff')
admin_router.register(r'customer', CustomerUserView, basename='customer')

urlpatterns = admin_router.urls