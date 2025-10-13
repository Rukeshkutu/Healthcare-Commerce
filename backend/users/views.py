from django.shortcuts import render
from .models import User, UserProfile
from .serializers import UserProfileSerializer, ChangePasswordSerializer, UserRegistrationSerializer, UserSerializer, LoginSerializer
from django.contrib.auth import authenticate

from rest_framework import status, generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data
            })
        return Response({"error": 'Invalid Credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data = request.data)

        if serializer.is_valid():
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({'message': ' Password update successfully'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def verify_user(request, user_id):
    try:
        user = User.objects.get(id = user_id)
        user.is_verified = True
        user.save()
        return Response({'message':'User verified successfully'})
    except User.DoesNotExist:
        return Response({'error':'User not found!'}, status=status.HTTP_404_NOT_FOUND)