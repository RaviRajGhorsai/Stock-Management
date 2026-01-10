
from stock_management.models import (
    Expense
)
from stock_management.serializers.expense_serializer import ExpenseSerializer

def list_expenses_for_tenant():
      
    expenses = Expense.objects.all()
    
    serializer = ExpenseSerializer(expenses, many=True)
    return serializer.data

def get_expense_for_tenant(id=None):
   
    try:
        return Expense.objects.get(id=id)
    except Expense.DoesNotExist:
        return None

def create_expense_for_tenant(expense_data):
    
    serializer = ExpenseSerializer(data=expense_data)
    serializer.is_valid(raise_exception=True)
    
    expense = serializer.save()
    
    return expense