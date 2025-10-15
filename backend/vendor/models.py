from django.db import models
from users.models import User

# Create your models here.
class Vendor(models.Model):
    VENDOR_TYPES = (
        ('individual', 'Individual'),
        ('hospital', 'Hospital'),
        ('clinic', 'Clinic'),
        ('dealer', 'Dealer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vendor_type = models.CharField(max_length=20, choices=VENDOR_TYPES)
    business_name = models.CharField(max_length=200)
    business_registration_number = models.CharField(max_length=100, blank=True)
    gst_number = models.CharField(max_length=15, blank=True)
    business_address = models.TextField()
    business_phone = models.CharField(max_length=15, blank= True)
    business_email = models.EmailField(blank=True)
    years_in_business = models.IntegerField(default=0)
    total_equipment_list = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.business_name
    

class BusinessDocument(models.Model):
    vendor = models.ForeignKey(Vendor, related_name='documents', on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100)
    document_file = models.FileField(upload_to='vendor_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.vendor.business_name} - {self.document_type}"