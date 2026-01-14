from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from user_app.serializers.auth_serializer import UserLoginSerializer
from user_app.apis.v1.auth.auth_service import login_user_service

# Create your views here.
class UserLoginView(viewsets.ViewSet):
    
    def create(self, request, *args, **kwargs):
        
        serializer =  UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            data = login_user_service(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            
            return Response({
                'status': 'success',
                'data': data
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({'error': str(e)}, status=401)