from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from .models import Warehouse, WarehouseStock, StockMovement
from .serializers import WarehouseSerializer, WarehouseStockSerializer, StockMovementSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def warehouse_list(request):
    warehouses = Warehouse.objects.filter(is_active=True)
    serializer = WarehouseSerializer(warehouses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def warehouse_stock(request, warehouse_id):
    try:
        warehouse = Warehouse.objects.get(id=warehouse_id)
    except Warehouse.DoesNotExist:
        return Response(
            {'error': 'Warehouse not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    stock_items = WarehouseStock.objects.filter(warehouse=warehouse)
    serializer = WarehouseStockSerializer(stock_items, many=True)
    
    return Response({
        'warehouse': WarehouseSerializer(warehouse).data,
        'stock': serializer.data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_stock(request):
    serializer = WarehouseStockSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def record_stock_movement(request):
    serializer = StockMovementSerializer(data=request.data)
    if serializer.is_valid():
        movement = serializer.save(handled_by=request.user)
        
        # Update stock quantities
        if movement.movement_type == 'in':
            stock, created = WarehouseStock.objects.get_or_create(
                equipment=movement.equipment,
                warehouse=movement.to_warehouse,
                defaults={'quantity': movement.quantity}
            )
            if not created:
                stock.quantity += movement.quantity
                stock.save()
        
        elif movement.movement_type == 'out':
            stock = WarehouseStock.objects.get(
                equipment=movement.equipment,
                warehouse=movement.from_warehouse
            )
            stock.quantity -= movement.quantity
            stock.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def warehouse_analytics(request):
    # Total stock by warehouse
    stock_by_warehouse = WarehouseStock.objects.values(
        'warehouse__name'
    ).annotate(
        total_items=Sum('quantity'),
        unique_products=Count('equipment')
    )
    
    # Stock value estimation (simplified)
    stock_value = WarehouseStock.objects.aggregate(
        total_value=Sum('equipment__sale_price')
    )
    
    return Response({
        'stock_by_warehouse': list(stock_by_warehouse),
        'total_stock_value': stock_value['total_value'] or 0,
        'movement_stats': {
            'recent_movements': StockMovement.objects.count(),
            # Add more stats as needed
        }
    })