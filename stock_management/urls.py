from rest_framework.routers import DefaultRouter

from stock_management.apis.v1.views.item_view import ItemView
from stock_management.apis.v1.views.expense_view import ExpenseView


router = DefaultRouter(trailing_slash=False)

router.register(r'items', ItemView, basename='items')
router.register(r'expenses', ExpenseView, basename='expenses')

urlpatterns = router.urls