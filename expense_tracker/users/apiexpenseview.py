from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ExpenseSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Expense
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ExpenseCategoryLimit, Expense
from .serializers import ExpenseCategoryLimitSerializer
from django.db import models



class AddExpenseAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Save with the logged-in user
            return Response({'message': 'Expense added successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# API: View Expenses
class ViewExpensesAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get all expenses for the logged-in user."""
        expenses = Expense.objects.filter(user=request.user)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

# API: Edit Expense
class EditExpenseAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, expense_id):
        """Edit an existing expense."""
        expense = get_object_or_404(Expense, id=expense_id, user=request.user)
        serializer = ExpenseSerializer(expense, data=request.data, partial=True)  # partial=True to allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Expense updated successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ViewExpenseLimitsAPI(APIView):
    """
    API endpoint to retrieve the expense limits for the authenticated user.
    """
    def get(self, request):
        category_limits = ExpenseCategoryLimit.objects.filter(user=request.user).first()
        if not category_limits:
            return Response({'error': 'Expense limits not set for the user.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ExpenseCategoryLimitSerializer(category_limits)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EditExpenseLimitsAPI(APIView):
    """
    API endpoint to edit the expense limits for the authenticated user.
    """
    def post(self, request):
        category_limits, created = ExpenseCategoryLimit.objects.get_or_create(user=request.user)
        serializer = ExpenseCategoryLimitSerializer(category_limits, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Expense limits updated successfully!', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckExpensesAgainstLimitsAPI(APIView):
    """
    API endpoint to check if the user's expenses exceed the limits.
    """
    def get(self, request):
        category_limits = ExpenseCategoryLimit.objects.filter(user=request.user).first()
        if not category_limits:
            return Response({'error': 'Expense limits not set for the user.'}, status=status.HTTP_404_NOT_FOUND)

        # Check expenses against limits
        category_expense_limits = {}
        for expense_type, _ in Expense.EXPENSE_TYPES:
            total_expenses = Expense.objects.filter(user=request.user, expense_type=expense_type).aggregate(total=models.Sum('amount'))['total'] or 0
            limit = getattr(category_limits, f"{expense_type}_limit", 0)
            category_expense_limits[expense_type] = {
                'total': total_expenses,
                'limit': limit,
                'exceeded': total_expenses > limit,
            }

        return Response({'category_expense_limits': category_expense_limits}, status=status.HTTP_200_OK)

# API: Delete Expense
class DeleteExpenseAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, expense_id):
        """Delete an expense."""
        expense = get_object_or_404(Expense, id=expense_id, user=request.user)
        expense.delete()
        return Response({'message': 'Expense deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)