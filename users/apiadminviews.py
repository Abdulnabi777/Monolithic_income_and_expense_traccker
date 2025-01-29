from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

# API View for managing users (list with pagination)
class ManageUsersAPI(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        user_list = User.objects.exclude(is_superuser=True)  # Exclude superusers
        page = request.query_params.get('page', 1)  # Get page number from query params
        paginator = Paginator(user_list, 10)  # Paginate users, 10 per page
        
        try:
            users = paginator.page(page)
        except Exception:
            return Response({'error': 'Invalid page number'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(users, many=True)
        return Response({'users': serializer.data, 'total_pages': paginator.num_pages}, status=status.HTTP_200_OK)

# API View for editing a user
class EditUserAPI(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        data = request.data
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API View for deleting a user
class DeleteUserAPI(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
