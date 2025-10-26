from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from . import views

urlpatterns = [
    # path('register/', views.RegisterView.as_view(), name='register'),
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('profile/', views.UserProfileView.as_view(), name='profile'),
    # path('profile/detail/', views.UserProfileDetailView.as_view(), name='profile-detail'),
    # path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    # path('verify-user/<int:user_id>/', views.verify_user, name='verify-user'),
    path('register/', views.register_user, name = 'register'),
    path('login/', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name = 'logout'),
    path('logout-all/', views.user_logout_all, name = 'logout-all'),
    path('token/refresh/', views.refresh_token, name = 'token-refresh'),
    path('token/verify/', TokenVerifyView.as_view, name = 'token-verify'),

    #user management endpoints
    path('profile/', views.user_profile, name = 'profile'),
    path('dashboard/', views.user_dashboard, name = 'dashboard'),
    path('check-auth/', views.check_auth, name = 'check-auth'),
    path('permissions/', views.user_permissions, name = 'permission'),

    #password management
    path('change-password/', views.change_password, name = 'change-password'),
    path('password-reset/', views.password_reset_request, name = 'passsword-reset'),
    path('password-reset-confirm/', views.password_reset_confirm, name = 'password-reset-confirm'),
]
