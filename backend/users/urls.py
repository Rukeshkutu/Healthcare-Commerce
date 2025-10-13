from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/detail/', views.UserProfileDetailView.as_view(), name='profile-detail'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('verify-user/<int:user_id>/', views.verify_user, name='verify-user'),

]
