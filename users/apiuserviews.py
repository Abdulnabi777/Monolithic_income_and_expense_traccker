from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated

# API: Signup
class SignupAPI(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User created successfully", "user_id": user.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API: Login
class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)\
        
# API: Logout
class LogoutAPI(APIView):
    @method_decorator(login_required)
    def post(self, request):
        logout(request)
        return redirect('login')  # Redirect to the login page after API logout
    
class UserHomeRedirectAPI(APIView):
    """
    Redirects the user to the appropriate homepage based on their role.
    Admins -> Home1
    Regular Users -> Home
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            return Response(
                {"message": "Redirect to admin homepage", "redirect_url": "/home1/"},
                status=200
            )
        return Response(
            {"message": "Redirect to user homepage", "redirect_url": "/home/"},
            status=200
        )
