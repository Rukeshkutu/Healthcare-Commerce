from rest_framework import serializers
from .models import Vendor, BusinessDocument

class VendorDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDocument
        fields = ['id', 'document_type', 'document_file', 'upload_at', 'is_verified']


class VendorSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only = True)
    documents = VendorDocumentSerializer(many = True, read_only = True)
    user_details = serializers.SerializerMethodField()

    class Meta:
        models = Vendor
        fields = '__all__'

    def get_user_details(self, obj):
        return{
            'username': obj.user.username,
            'email': obj.user.email,
            'phone': obj.user.phone_number
        }
    

class VendorRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only = True)
    email = serializers.EmailField(write_only = True)
    password = serializers.CharField(write_only = True)
    phone_number = serializers.CharField(write_only = True)

    class Meta:
        model = Vendor
        fields = [
            'username', 'email', 'password', 'phone_number', 'vendor_tyep', 'business_name', 'business_registration_number', 'gst_number', 'bussiness_name', 'business_address', 'business_phone', 'business_email'
        ]

    def create(self, validated_data):
        from users.models import User

        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'password':validated_data.pop('password'),
            'phone_number': validated_data.pop('phone_number'),
            'user_type': 'vendor'
        }

        user = User.objects.create_user(**user_data)

        vendor = Vendor.objects.create(user = user, **validated_data)
        return vendor
    
