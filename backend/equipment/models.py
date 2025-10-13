from django.db import models
from users.models import User

# Create your models here.

class EquipmentCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/)', null=True, blank=True)

    def __str__(self):
        return self.name
    

class Equipment(models.Model):
    EQUIPMENT_TYPES = (
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
        ('both', 'Both Sale and Rent'),
    )

    CONDITIONS = (
        ('new', 'New'),
        ('used', 'Used'),
        ('refurbished', 'Refurbished'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(EquipmentCategory, on_delete=models.CASCADE)
    equipment_type = models.CharField(max_length=20, choices=EQUIPMENT_TYPES)
    condition = models.CharField(max_length=20, choices=CONDITIONS)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rental_price_per_day = models.DecimalField(max_length=10, decimal_places=2, null=True, blank=True)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type':'vendor'})
    is_verified = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class EquipmentImage(models.Model):
    equipment = models.ForeignKey(Equipment, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='equipment/')
    is_primary = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image of {self.equipment.name}"
    

class EquipmentSpecification(models.Model):
    equipment = models.ForeignKey(Equipment, related_name='specifications', on_delete=models.CASCADE)
    key  = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.key}: {self.value}"