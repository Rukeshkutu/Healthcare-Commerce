from django.contrib import admin
from .models import MedicalEquipment, EquipmentCategory, EquipmentImage, EquipmentInspection

class EquipmentImageInline(admin.TabularInline):
    model = EquipmentImage
    extra = 1

@admin.register(MedicalEquipment)
class MedicalEquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'model', 'condition', 'transaction_type', 'sale_price', 'is_verified', 'is_available']
    list_filter = ['condition', 'transaction_type', 'is_verified', 'is_available', 'category']
    search_fields = ['name', 'brand', 'model', 'vendor__username']
    inlines = [EquipmentImageInline]
    readonly_fields = ['created_at', 'updated_at']

@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_category', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(EquipmentInspection)
class EquipmentInspectionAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'inspector', 'inspection_date', 'status']
    list_filter = ['status', 'inspection_date']
    readonly_fields = ['created_at']