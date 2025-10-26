from django.db import models
from users.models import User

class Staff(models.Model):
    STAFF_TYPES = (
        ('delivery', 'Delivery Staff'),
        ('inspection', 'Inspection Staff'),
        ('warehouse', 'Warehouse Staff'),
        ('franchise', 'Franchise Staff'),
        ('admin', 'Admin Staff'),
    )
    
    STAFF_STATUS = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('on_leave', 'On Leave'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_type = models.CharField(max_length=20, choices=STAFF_TYPES)
    employee_id = models.CharField(max_length=50, unique=True)
    date_of_joining = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STAFF_STATUS, default='active')
    franchise = models.ForeignKey('franchise.Franchise', on_delete=models.SET_NULL, null=True, blank=True)
    warehouse = models.ForeignKey('warehouse.Warehouse', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.staff_type}"

class StaffAttendance(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField()
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    total_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_long = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    class Meta:
        unique_together = ('staff', 'date')
    
    def __str__(self):
        return f"{self.staff.user.username} - {self.date}"

class StaffPerformance(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    month = models.DateField()
    tasks_completed = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    customer_feedback = models.TextField(blank=True)
    attendance_days = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('staff', 'month')
    
    def __str__(self):
        return f"{self.staff.user.username} - {self.month.strftime('%B %Y')}"