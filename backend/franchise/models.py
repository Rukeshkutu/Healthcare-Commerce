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
    # location = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length = 100)
    pincode = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=FRANCHISE_STATUS, default= 'active')
    registration_date = models.DateField(auto_now_add=True)
    monthly_royalty_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=15.00)

    def __str__(self):
        return f"{self.name} - {self.city}"
    

class FranchisePerformance(models.Model):
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    month = models.DateField()
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_rentals = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    staff_hire_count = models.IntegerField(default=0)
    customer_count = models.IntegerField(default=0)
    royalty_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('franchise', 'month')
    
    def __str__(self):
        return f"{self.franchise.name} - {self.month.strftime('%B %Y')}"
