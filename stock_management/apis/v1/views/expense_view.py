from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from stock_management.serializers.expense_serializer import ExpenseSerializer
from stock_management.apis.v1.auth.auth_service import check_user_role
from stock_management.services.expense_service import (
    list_expenses_for_tenant,
    get_expense_for_tenant,
    create_expense_for_tenant
)

class ExpenseView(viewsets.ViewSet):
    
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        
        user = request.user
        
        auth_response = check_user_role(user)
        
        if auth_response is None:
            return Response({'status': 'error', 'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        tenant = user.tenant
        
        expenses = list_expenses_for_tenant(tenant)
        
        return Response({"data": expenses}, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        
        user = request.user
        
        auth_response = check_user_role(user)
        if auth_response is None:
            return Response({'status': 'error', 'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        tenant = user.tenant
        
        expense = get_expense_for_tenant(tenant, id=pk)
        if expense is None:
            return Response({'status': 'error', 'message': 'Expense not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ExpenseSerializer(expense)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        
        user = request.user
        
        auth_response = check_user_role(user)
        if auth_response is None:
            return Response({'status': 'error', 'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        tenant = user.tenant
        
        expense = create_expense_for_tenant(tenant, request.data)
        
        serializer = ExpenseSerializer(expense)
        
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
    