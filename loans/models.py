from django.db import models
from apps.users.models import User
from apps.equipment.models import MedicalEquipment

class NBFCPartner(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=17)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Commission percentage")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class LoanApplication(models.Model):
    LOAN_STATUS = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
    )
    
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'customer'})
    equipment = models.ForeignKey(MedicalEquipment, on_delete=models.CASCADE)
    nbfc_partner = models.ForeignKey(NBFCPartner, on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    tenure_months = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    emi_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=LOAN_STATUS, default='draft')
    application_date = models.DateTimeField(auto_now_add=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    disbursement_date = models.DateTimeField(null=True, blank=True)
    processing_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Loan #{self.id} - {self.applicant.username}"

class LoanDocument(models.Model):
    loan_application = models.ForeignKey(LoanApplication, related_name='documents', on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100)
    document_file = models.FileField(upload_to='loan_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.loan_application} - {self.document_type}"