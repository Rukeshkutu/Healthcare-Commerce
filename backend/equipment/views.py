# from django.shortcuts import render
# from rest_framework import viewsets, status, filters
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
# from django_filters.rest_framework import DjangoFilterBackend
# from .models import Equipment, EquipmentCategory, EquipmentImage, EquipmentSpecification
# from .serializer import EquipmentSerializer, EquipmentImageSerializer, EquipmentCreateSerializer, EquipmentCategorySerializer
# from rest_framework.pagination import PageNumberPagination
# from django.db.models import Q


# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 50

# class EquipmentCategoryViewSet(viewsets.ModelViewSet):
#     queryset = EquipmentCategory.objects.all()
#     serializer_class = EquipmentCategorySerializer
#     pagination_class = StandardResultsSetPagination
#     permission_classes = [IsAuthenticated]

#     def get_permissions(self):
#         if self.action in ['create', 'update', 'partial_update', 'destroy']:
#             return [IsAdminUser()]
#         elif self.action in ['list', 'retrive']:
#             return[AllowAny]
#         return [IsAuthenticated()]
    

# class EquipmentViewSet(viewsets.ModelViewSet):
#     queryset = Equipment.objects.all()
#     permission_classes = [IsAuthenticated]
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_field = ['category', 'equipment_type', 'condition', 'is_verified']
#     search_field = ['name', 'description']
#     ordering_fields = ['price', 'rental_price_per_day', 'created_at']
#     ordering = ['-created_at']
#     pagination_class = StandardResultsSetPagination

#     def get_serializer_class(self):
#         if self.action == 'create':
#             return EquipmentCreateSerializer
#         elif self.action in ['update', 'partial_update']:
#             return EquipmentSerializer
#         return EquipmentSerializer
    
#     def get_permissions(self):
#         if self.action in ['list', 'retrive', 'search']:
#             return[AllowAny]
#         return [IsAuthenticated]
    
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         user = self.request.user
#         if not user.is_authenticated or user.user_type =='customer':
#             queryset = queryset.filter(is_verified = True, is_available = True)

#         elif user.user_type == 'vendor':
#             queryset = queryset.filter(vendor=user)
#         elif user.user_type in ['franchise_owner', 'staff']:
#             queryset = queryset.filter(is_verified = True)

#         return queryset.select_related('category', 'vendor').prefetch_related('images', 'specifications')
    
    
#     def perform_class(self, serializer):
#         serializer.save(vendor=self.request.user)
    
#     @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
#     def verify(self, request, pk=None):
#         equipment = self.get_object()
#         equipment.is_verified = True
#         equipment.save()

#         equipment.generate_qr_code()
#         equipment.save()
#         return Response({
#             'status':'Equipment verified successfully',
#             'qr_code_url': equipment.qr_code.url if equipment.qr_code else None
#             })
    
#     @action(detail=False, methods=['get'])
#     def my_equipment(self, request):
#         if request.user.user_type != 'vendor':
#             return Response({'error': 'Only Vendors can access this endpoint'}, status=status.HTTP_403_FORBIDDEN)
        
#         equipment = Equipment.objects.filter(vendor=request.user)
#         serializer = self.get_serializer(equipment, many=True)
#         return Response(serializer.data)
    
#     @action(detail=True, methods=['post'])
#     def add_image(self, request, pk=None):
#         equipment = self.get_object()

#         if equipment.vendor != request.user and not request.user.is_staff:
#             return Response({'error':'You do not have the permission to add image to the equipment'}, status=status.HTTP_403_FORBIDDEN)
        
#         serializer = EquipmentImageSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save(equipment=equipment)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)