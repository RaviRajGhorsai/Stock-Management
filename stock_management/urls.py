from rest_framework.routers import DefaultRouter
from stock_management.adapter.views.item_view import ItemView

router = DefaultRouter(trailing_slash=False)
router.register(r'items', ItemView, basename='items')

urlpatterns = router.urls