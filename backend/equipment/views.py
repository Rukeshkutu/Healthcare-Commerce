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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from .models import Equipment, EquipmentCategory, EquipmentInspection
from .serializer import MedicalEquipmentSerializer, EquipmentCategorySerializer, EquipmentInspectionSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def equipment_list(request):
    if request.method == 'GET':
        # Filter equipment based on query parameters
        category = request.GET.get('category')
        condition = request.GET.get('condition')
        transaction_type = request.GET.get('transaction_type')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        
        queryset = Equipment.objects.filter(is_verified=True, is_available=True)
        
        if category:
            queryset = queryset.filter(category__id=category)
        if condition:
            queryset = queryset.filter(condition=condition)
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        if min_price:
            queryset = queryset.filter(sale_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(sale_price__lte=max_price)
        
        serializer = MedicalEquipmentSerializer(queryset, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Only vendors can list equipment
        if request.user.user_type != 'vendor':
            return Response(
                {'error': 'Only vendors can list equipment'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = MedicalEquipmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(vendor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def equipment_detail(request, pk):
    try:
        equipment = Equipment.objects.get(pk=pk)
    except Equipment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MedicalEquipmentSerializer(equipment)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Only owner or admin can update
        if equipment.vendor != request.user and request.user.user_type != 'admin':
            return Response(
                {'error': 'You do not have permission to edit this equipment'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = MedicalEquipmentSerializer(equipment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if equipment.vendor != request.user and request.user.user_type != 'admin':
            return Response(
                {'error': 'You do not have permission to delete this equipment'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        equipment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([AllowAny])
def category_list(request):
    categories = EquipmentCategory.objects.filter(is_active=True)
    serializer = EquipmentCategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_inspection(request, equipment_id):
    try:
        equipment = Equipment.objects.get(id=equipment_id)
    except Equipment.DoesNotExist:
        return Response(
            {'error': 'Equipment not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if inspection already exists
    existing_inspection = EquipmentInspection.objects.filter(
        equipment=equipment, 
        status__in=['pending', 'in_progress']
    ).exists()
    
    if existing_inspection:
        return Response(
            {'error': 'Inspection already requested or in progress'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    inspection = EquipmentInspection.objects.create(
        equipment=equipment,
        inspector=request.user,  # This should be assigned to appropriate staff
        inspection_date=request.data.get('preferred_date'),
        notes=request.data.get('notes', '')
    )
    
    serializer = EquipmentInspectionSerializer(inspection)
    return Response(serializer.data, status=status.HTTP_201_CREATED)