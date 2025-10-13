from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    USER_TYPES=(
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
        ('franchise_owner', 'Franchise_owner'),
    )
    user_type = models.CharField(max_length=50, choices=USER_TYPES, default='customer')
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}({self.user_type})"


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    national_id = models.CharField(max_length = 10, null = True, blank = True)
    pan_number = models.CharField(max_length = 12, null= True, blank = True)
    bio = models.TextField(blank=True
    )
    
    def __str__(self):
        return f"Profile of {self.user.username}"