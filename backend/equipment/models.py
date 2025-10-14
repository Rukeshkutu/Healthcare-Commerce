from django.db import models
from users.models import User
from django.core.files import File
import qrcode
import uuid
from io import BytesIO
# Create your models here.

class EquipmentCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Equipment Categories"
        ordering = ['name']

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
    rental_price_per_day = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type':'vendor'})
    is_verified = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    is_verified = models.BooleanField(default=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_verified', 'is_available']),
            models.Index(fields=['vendor']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_equipment_type_display()})"

    def save(self, *args, **kwargs):
        if self.is_verified and not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)

    def generate_qr_code(self):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size = 10, border=4)
        data = f""" 
            HealthCare Commerce Certified Equipment
            id: {self.unique_id}
            name: {self.name}
            category: {self.category.name}
            type : {self.get_equipment_type_display()}
            condition: {self.get_condition_display()}
            Verified: {'Yes' if self.is_verified else 'No'}""".strip()
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color= 'black', back_color = 'white')
        buffer = BytesIO
        img.save(buffer, 'PNG')
        self.qr_code.save(f'qr_{self.unique_idi}.png', File(buffer), save=False)

        @property
        def primary_image(self):
            return self.images.filter(is_primary = True).first()
            

class EquipmentImage(models.Model):
    equipment = models.ForeignKey(Equipment, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='equipment/')
    is_primary = models.BooleanField(default=False)
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['-is_primary', 'created_at']


    def __str__(self):
        return f"Image of {self.equipment.name}"
    
    def save(self):
        if self.is_primary:
            EquipmentImage.objects.filter(equipment = self.equipment, is_primary = True).update(is_primary = False)
            super().save(*args, **kwargs)
    

class EquipmentSpecification(models.Model):
    equipment = models.ForeignKey(Equipment, related_name='specifications', on_delete=models.CASCADE)
    key  = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'key']

    def __str__(self):
        return f"{self.key}: {self.value}"