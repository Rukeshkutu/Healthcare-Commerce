from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile
# Register your models here.

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'phone_number', 'city', 'is_verified', 'is_staff')
    list_filter = ('user_type', 'is_verified', 'is_staff', 'city')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'address', 'city', 'state', 'pincode', 'is_verified')
        }),
    )
    inlines = [UserProfileInline]

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)