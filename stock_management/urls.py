from rest_framework.routers import DefaultRouter
from .views import ItemView

router = DefaultRouter(trailing_slash=False)
router.register(r'items', ItemView, basename='items')

urlpatterns = router.urls