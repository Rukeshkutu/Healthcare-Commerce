from django.db import models
from users.models import User
from warehouse.models import Warehouse

# Create your models here.
class Franchise(models.Model):
    FRANCHISE_STATUS = (
      ('active', 'Active'),
      ('inactive', 'Inactive'),
      ('suspended', 'Suspended'),
    )
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type':'franchise_owner'})
    location = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length = 100)
    pincode = models.CharField(max_length=10)
    warehouse = models.OneToOneField(Warehouse, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()