from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Item
from .serializers import ItemSerializer
from django_tenants.utils import schema_context

class ItemView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAuthenticated]       
    
    def get_user(self, request):
        return request.user

    def list(self, request, *args, **kwargs):
        
        user = self.get_user(request)
        
        if not (user.is_admin() or user.is_staff_member()):
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        tenant = user.tenant
        with schema_context(tenant.schema_name):
            items = Item.objects.all()
            serializer = ItemSerializer(items, many=True)
            return JsonResponse({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        
        user = self.get_user(request)
        
        if not (user.is_admin() or user.is_staff_member()):
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        
        tenant = user.tenant
        with schema_context(tenant.schema_name):
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        