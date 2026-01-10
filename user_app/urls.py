from rest_framework.routers import DefaultRouter

from user_app.apis.v1.views.super_user_login_view import SuperUserLoginView
from user_app.apis.v1.views.user_create_view import CreateAdminView

admin_router = DefaultRouter(trailing_slash=False)

admin_router.register(r'login', SuperUserLoginView, basename='superuser_login')
admin_router.register(r'create_admin', CreateAdminView, basename='create_admin')

urlpatterns = admin_router.urls