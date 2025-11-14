from django.contrib import admin
from .models import Vendor, BusinessDocument
# Register your models here.

class VendorDocumentInline(admin.TabularInline):
    models = BusinessDocument
    extra = 1

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'vendor_type','user', 'is_verified', 'rating', 'total_equipment_listed']
    list_filter = ['vendor_type', 'is_verified', 'years_in_business']
    search_filter = ['business_name', 'user__username', 'gst_number']
    inline = [VendorDocumentInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
@admin.register(BusinessDocument)
class VendorDocumentAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'document_type','uploaded_at', 'is_verified']
    list_filter = ['document_type', 'is_verified', 'uploaded_at']
    search_filter = ['vendor__business_name', 'user__username', 'gst_number']
   