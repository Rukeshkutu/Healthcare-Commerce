from django.db import models
from equipment.models import Equipment
from users.models import User
# Create your models here.

class Warehouse(models.Model):
    name = models.CharField(max_length=200)
    # location = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    capacity = models.IntegerField(help_text="Total capacity in  units")
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'user_type':'staff'})
    contact_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.city}"
    

class WarehouseStock(models.Model):
    STOCK_STATUS = (
        ('available', 'Available'),
        ('reserved', 'reserved'),
        ('in_transit', 'In Transit'),
        ('sold', 'Sold'),
    )
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STOCK_STATUS, default='available')
    rack_number = models.CharField(max_length=50, blank=True)
    shelf_number = models.CharField(max_length=50, blank=True)
    last_checked = models.DateTimeField(auto_now=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('equipment', 'wharehouse')

    def __str__(self):
        return f"{self.equipment.name}- {self.warehouse.name}"
    

class StockMovement(models.Model):
    MOVEMENT_TYPES= (
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('transfer', 'Transfer'),
    )
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    from_warehouse = models.ForeignKey(Warehouse, related_name='movements_out', on_delete=models.CASCADE, null=True, blank=True)
    to_warehouse = models.ForeignKey(Warehouse, related_name='movements_in', on_delete=models.CASCADE, null=True, blank=True)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    reason = models.TextField(blank=True)
    handled_by = models.ForeignKey(User, on_delete=models.CASCADE)
    movement_date = models.DateTimeField()
    # status = models.CharField(max_length=20, choices=INSPECTION_STATUS, default='pending')
    # notes = models.TextField(blank = True)
    # inspection_report = models.FileField(upload_to='inspection_reports/', null=True, blank= True)
    # created_at = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.equipment_type} - {self.equipment.name}"
