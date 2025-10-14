from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.EquipmentCategoryViewSet)
router.register(r'', views.EquipmentViewSet, basename='equipment')

urlpatterns = [
    path('', include(router.urls)),
]
