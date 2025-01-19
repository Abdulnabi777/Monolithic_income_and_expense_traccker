from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Income
from .serializers import IncomeSerializer

class AddIncomeAPI(APIView):
    """API to add income for the authenticated user."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = IncomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Income added successfully!", "income": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewIncomesAPI(APIView):
    """API to view all incomes for the authenticated user."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        incomes = Income.objects.filter(user=request.user)
        serializer = IncomeSerializer(incomes, many=True)
        return Response({"incomes": serializer.data}, status=status.HTTP_200_OK)


class EditIncomeAPI(APIView):
    """API to edit an income for the authenticated user."""
    permission_classes = [IsAuthenticated]

    def put(self, request, income_id):
        income = get_object_or_404(Income, id=income_id, user=request.user)
        serializer = IncomeSerializer(income, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Income updated successfully!", "income": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteIncomeAPI(APIView):
    """API to delete an income for the authenticated user."""
    permission_classes = [IsAuthenticated]

    def delete(self, request, income_id):
        income = get_object_or_404(Income, id=income_id, user=request.user)
        income.delete()
        return Response({"message": "Income deleted successfully!"}, status=status.HTTP_200_OK)
