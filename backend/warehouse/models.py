from django.db import models
from equipment.models import Equipment
from users.models import User
# Create your models here.

class Warehouse(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    capacity = models.IntegerField(help_text="Total capacity in  units")
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'user_type':'staff'})
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Stock(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    min_stock_level = models.IntegerField(default=5)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('equipment', 'wharehouse')

    def __str__(self):
        return f"{self.equipment.name}- {self.warehouse.name}({self.quantity})"
    

class Inspection(models.Model):
    INSPECTION_STATUS = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
    )
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    inspector = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type':'staff'})
    inspection_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=INSPECTION_STATUS, default='pending')
    notes = models.TextField(blank = True)
    inspection_report = models.FileField(upload_to='inspection_reports/', null=True, blank= True)
    created_at = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"Inspection of {self.equipment.name} on {self.inspection_date}"
