from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.vendor_registration, name='vendor-registration'),
    path('profile/', views.vendor_profile, name='vendor-profile'),
    path('documents/', views.vendor_documents, name='vendor-documents'),
    path('dashboard/', views.vendor_dashboard, name='vendor-dashboard'),
    path('performance/', views.vendor_performance, name='vendor-performance'),
]