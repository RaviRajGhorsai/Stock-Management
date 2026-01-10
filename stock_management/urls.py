from rest_framework.routers import DefaultRouter

from stock_management.apis.v1.views.create_user_view import(
    CreateStaffView,
    CreateCustomerView
)
from stock_management.apis.v1.views.item_view import ItemView
from stock_management.apis.v1.views.expense_view import ExpenseView
from stock_management.apis.v1.views.user_lists_view import (
    StaffUserView,
    CustomerUserView
)
from stock_management.apis.v1.views.admin_login_view import AdminLoginView

router = DefaultRouter(trailing_slash=False)

router.register(r'login', AdminLoginView, basename='admin_login')
router.register(r'create_staff', CreateStaffView, basename='create_staff')
router.register(r'create_customer', CreateCustomerView, basename='create_customer')
router.register(r'staff', StaffUserView, basename='staff')
router.register(r'customer', CustomerUserView, basename='customer')
router.register(r'items', ItemView, basename='items')
router.register(r'expenses', ExpenseView, basename='expenses')

urlpatterns = router.urls