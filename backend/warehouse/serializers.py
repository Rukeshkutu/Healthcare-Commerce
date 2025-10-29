from rest_framework import serializers
from .models import Warehouse, WarehouseStock, StockMovement

class WarehouseSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    current_capacity = serializers.SerializerMethodField()
    
    class Meta:
        model = Warehouse
        fields = '__all__'
    
    def get_current_capacity(self, obj):
        # Calculate current capacity usage (simplified)
        total_items = WarehouseStock.objects.filter(warehouse=obj).count()
        return f"{total_items}/{obj.capacity}"

class WarehouseStockSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    equipment_value = serializers.DecimalField(source='equipment.sale_price', read_only=True, max_digits=10, decimal_places=2)
    
    class Meta:
        model = WarehouseStock
        fields = '__all__'

class StockMovementSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    from_warehouse_name = serializers.CharField(source='from_warehouse.name', read_only=True)
    to_warehouse_name = serializers.CharField(source='to_warehouse.name', read_only=True)
    handled_by_name = serializers.CharField(source='handled_by.get_full_name', read_only=True)
    
    class Meta:
        model = StockMovement
        fields = '__all__'