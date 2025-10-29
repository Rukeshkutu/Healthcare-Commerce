from django.urls import path
from . import views

urlpatterns = [
    path('', views.equipment_list, name='equipment-list'),
    path('categories/', views.category_list, name='category-list'),
    path('<int:pk>/', views.equipment_detail, name='equipment-detail'),
    path('<int:equipment_id>/inspect/', views.request_inspection, name='request-inspection'),
]