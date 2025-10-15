from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# Create your models here.


class User(AbstractUser):
    USER_TYPES=(
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
        ('franchise owner', 'Franchise owner'),
    )
    user_type = models.CharField(max_length=50, choices=USER_TYPES, default='customer')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9, 15}$', message=' Phone number must be entered in the format :"+999999". UP to 15 digit allowed')
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username}({self.user_type})"


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    national_id = models.CharField(max_length = 10, null = True, blank = True)
    pan_number = models.CharField(max_length = 12, null= True, blank = True)
    
    profile_picture = models.ImageField(upload_to='profile/', null=True, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    # bio = models.TextField(blank=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"