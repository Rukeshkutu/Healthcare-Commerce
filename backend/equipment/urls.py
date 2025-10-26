from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# router = DefaultRouter()
# router.register(r'categories', views.EquipmentCategoryViewSet)
# router.register(r'', views.EquipmentViewSet, basename='equipment')

urlpatterns = [
    # path('', include(router.urls)),
    path('', views.equipment_list, name = 'equipment-list'),
    path('categories/', views.category_list, name = 'category-list'),
    path('<int:pk>/', views.equipment_detail, name = 'equipment-detail'),
    path('<int:equipment_id>/inspect/', views.request_inspection, name = 'request-inspection'),
]
