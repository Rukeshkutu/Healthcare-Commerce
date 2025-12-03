# from django.shortcuts import render
from .models import User, UserProfile
from .serializers import UserProfileSerializer, ChangePasswordSerializer, UserSerializer, LoginSerializer, UserUpdateSerializer, PasswordResetRequestSerializer, UserRegistrationSerializer
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
# from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken 
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from equipment.models import Equipment
# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = [permissions.AllowAny]
#     serializer_class = UserRegistrationSerializer


# class LoginView(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
        
#         user = authenticate(username=username, password=password)

#         if user:
#             refresh = RefreshToken.for_user(user)
#             user_serializer = UserSerializer(user)

#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'user': user_serializer.data
#             })
#         return Response({"error": 'Invalid Credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    

# class UserProfileView(generics.RetrieveAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         return self.request.user

# class ChangePasswordView(generics.UpdateAPIView):
#     serializer_class = ChangePasswordSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         return self.request.user
    
#     def update(self, request, *args, **kwargs):
#         user = self.get_object()
#         serializer = self.get_serializer(data = request.data)

#         if serializer.is_valid():
#             user.set_password(serializer.validated_data["new_password"])
#             user.save()
#             return Response({'message': ' Password update successfully'})
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class UserProfileDetailView(generics.RetrieveUpdateAPIView):
#     serializer_class = UserProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         return self.request.user.profile
    

# @api_view(['POST'])
# @permission_classes([permissions.IsAdminUser])
# def verify_user(request, user_id):
#     try:
#         user = User.objects.get(id = user_id)
#         user.is_verified = True
#         user.save()
#         return Response({'message':'User verified successfully'})
#     except User.DoesNotExist:
#         return Response({'error':'User not found!'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data

            # UserProfile.objects.create(user = user)
            return Response({
                'message': 'User registered Successfully',
                'user': user_data,
                'token':{
                    'refresh':str(refresh),
                    'access':str(refresh.access_token),
                }
            }, status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data

            return Response({
                'message': 'Login Successfully',
                'user': user_data,
                'token': {
                    'refresh': str(refresh),
                    'access':str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    try: 
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'message':'Successfully logged out'
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'error': 'Invalid token',
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout_all(request):
    #logout user from all the devices by blacklisting refresh token
    try:
        tokens = OutstandingToken.objects.filter(user_id = request.user.id)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token = token)

        return Response({
            'message': 'Successfully logged out from all deviecs'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'errors':'Could not log out from all devices'
        },status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    #refresh jwt access token
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({
                'error':'Refresh token is required.'

            }, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken(refresh_token)
        return Response({
            'access': str(token.access_token),

        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'error':'Invalid or expired refresh token'
        }, status = status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'GET'])
@permission_classes([AllowAny])
def user_profile(request):
    user = request.user
    
    if request.method  == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserUpdateSerializer(user, data=request.data, partial = True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def user_dashboard(request):
    user = request.user

    dashboard_data = {
        'user_info':{
            'name':user.get_full_name(),
            'user_type':user.user_type,
            'email': user.email,
            'phone':user.phone_number,
            'is_verified':user.is_verified
        },
        'quick_stats':{},
        'recent_activity':[]
    }

    if user.user_type == 'customer':
        # from equipment.models import Equipment
        from loans.models import LoanApplication

        dashboard_data['quick_stats'] = {
            'view_equipment':0,
            'save_items':0,
            'active_rentals':0,
            'loan_applications':LoanApplication.objects.filter(appicant = user).count()
        }
    elif user.user_type == 'vendor':
        equipment_stats = Equipment.objects.filter(vendor = user)
        dashboard_data['quick_stats'] = {
            'total_equipment': equipment_stats.count(),
            'verified_equipment': equipment_stats.filter(is_verified= True).count(),
            'available_equipment': equipment_stats.filter(is_available=True).count(),
            'pending_inspections':equipment_stats.filter(is_verified=True).count()
        }
    
    elif user.user_type == 'franchise':
        from franchise.models import FranchisePerformance
        from django.utils import timezone
        from datetime import datetime

        try: 
            franchise = user.franchise
            current_month = timezone.now().replace(day=1)
            performance = FranchisePerformance.objects.filter(franchise= franchise, month=current_month).first()
            dashboard_data['quick_stats']={
                'monthly_sales': performance.total_sales if performance else 0,
                'active_rentals':performance.total_rentals if performance else 0,
                'staff_placement':performance.staff_hire_count if performance else 0,
                'new_customers': performance.customer_count if performance else 0
            }
        except:
            dashboard_data['quick_stats']={
                'monthly_sales': 0,
                'active_rentals':0,
                'staff_placement':0,
                'new_customers': 0
            }
    elif user.user_type == 'staff':
        from staff.models import StaffAttendance
        from django.utils import timezone

        today = timezone.now().date()
        today_attendance = StaffAttendance.objects.filter(staff_user = user, date=today).first()
        dashboard_data['quick_stats'] = {
            'today_hours': today_attendance.total_hours if today_attendance else 0,
            'tasks_completed':0,
            'pending_task':0,
            'performance_rating':0     
        }
    elif user.user_type == 'admin':
        from users.models import User
        from loans.models import LoanApplication

        dashboard_data['quick_stats'] = {
            'total_users': User.objects.count(),
            'total_equipment': Equipment.objects.count(),
            'pending_verifications': Equipment.objects.filter(status = 'submitted').count(),
            'loan_applications':LoanApplication.objects.filter(is_verified = False).count()
        }
    return Response(dashboard_data)


@api_view(['POST'])
@permission_classes([AllowAny])
def change_password(request):
    user = request.user
    serializer = ChangePasswordSerializer(data = request.data)

    if serializer.is_valid():
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'error':'Current password is incorrect.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        update_session_auth_hash(request, user)
        return Response({
            'message':'Password updated successfully.'
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    user = request.user
    serializer = PasswordResetRequestSerializer(data = request.data)

    if serializer.is_valid():
        # In a real implementation, you would:
        # 1. Generate reset token
        # 2. Send email with reset link
        # 3. Return success message
        
        email = serializer.validated_data['email']
        
        # For now, just return success message
        return Response({
            'message':'if an account with this mail exit, a password link has been sent.'
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    serializer = PasswordResetRequestSerializer(data=request.data)
    
    if serializer.is_valid():
        # In a real implementation, you would:
        # 1. Verify token and uid
        # 2. Find user and set new password
        # 3. Return success message
        
        return Response({
            'message': 'Password has been reset successfully'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_auth(request):
    user = request.user
    serializer = UserSerializer(user)
    
    return Response({
        'authenticated': True,
        'user': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_permissions(request):
    user = request.user

    permissions = {
        'can_list_equipment': user.user_type in ['vendor', 'admin'],
        'can_rent_equipment': user.user_type in ['customer', 'admin'],
        'can_manage_users': user.user_type == 'admin',
        'can_manage_franchises': user.user_type in ['admin', 'franchise'],
        'can_process_loans': user.user_type in ['admin', 'franchise'],
        'can_view_analytics': user.user_type == 'admin',
        'can_manage_warehouse': user.user_type in ['admin', 'staff'],
    }
    
    return Response(permissions, status=status.HTTP_200_OK)

