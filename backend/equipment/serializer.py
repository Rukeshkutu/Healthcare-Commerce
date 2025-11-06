from rest_framework import serializers
from .models import EquipmentCategory, Equipment, EquipmentImage,EquipmentInspection
# from django.core.files.base import ContentFile
# import base64


# class EquipmentSpecificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EquipmentSpecification
#         fields = ['id', 'key', 'value', 'order']
#         read_only_field = ['id']

# class EquipmentImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EquipmentImage
#         fields = ['id', 'image', 'image_url', 'is_primary', 'caption', 'created_at']
#         read_only_fields = ['id', 'created_at']

#         def get_image_url(self, obj):
#             if obj.image:
#                 return obj.image.url
#             return None

# class EquipmentCategorySerializer(serializers.ModelSerializer):
#     equipment_count = serializers.SerializerMethodField()

#     class Meta:
#         model = EquipmentCategory
#         fields = ['id', 'name', 'description', 'image', 'equipment_count', 'created_at']
#         read_only_file = ['id', 'created_at']

#         def get_equipment_count(self, obj):
#             return obj.equipments.filter(is_verified = True, is_available = True).count()
        

# class EquipmentSerializer(serializers.ModelSerializer):
#     vendor_name = serializers.CharField(source='vendor.get_full_name', read_only=True)
#     vendor_email = serializers.CharField(source = 'vendor.email', read_only = True)
#     category_name = serializers.CharField(source='category.name', read_only=True)
#     images = EquipmentImageSerializer(many=True, read_only=True)
#     specifications = EquipmentSpecificationSerializer(many=True, read_only=True)
#     primary_image = serializers.SerializerMethodField()
#     qr_code_url = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Equipment
#         fields = [
#             'id', 'unique_id', 'name', 'description', 'category', 'category_name', 'equipment_type',
#             'condition', 'price', 'rental_price_per_day', 'vendor', 'vendor_name', 'vendor_email',
#             'is_verified', 'is_available', 'qr_code', 'qr_code_url', 'images', 'primary_image', 'specifications',
#             'created_at', 'updated_at'
#         ]
#         read_only_fields = ['id', 'unique_id','vendor', 'is_verified', 'qr_code', 'created_at', 'updated_at']

#         def get_primary_image(self, obj):
#             primary_img = obj.primary_image
#             if primary_img:
#                 return EquipmentImageSerializer(primary_img).data
#             return None
        
#         def get_qr_code_url(self, obj):
#             if obj.qr_code:
#                 return obj.qr_code.url
#             return None

# class EquipmentCreateSerializer(serializers.ModelSerializer):
#     images = serializers.ListField(
#         child=serializers.ImageField(),
#         write_only=True,
#         required=False
#     )
#     specifications = serializers.ListField(
#         child=serializers.DictField(),
#         write_only=True,
#         required=False
#     )
    
#     class Meta:
#         model = Equipment
#         fields = [
#             'name', 'description', 'category', 'equipment_type', 'condition',
#             'price', 'rental_price_per_day', 'images', 'specifications'
#         ]
    
#     def validate(self, data):
#         if data.get('equipment_type') in ['sale', 'both'] and not data.get('price'):
#             raise serializers.ValidationError({'prie': 'Price is requested for equipment available for sale.'})
        
#         if data.get('equipment_type') in ['rent', 'both'] and not data.get('rental_price_per_day'):
#             raise serializers.ValidationError({'rental_price_per_day': 'Rental price per day is required for equipment available for rent.'}
#             )
#         return data

#     def create(self, validated_data):
#         images_data = validated_data.pop('images', [])
#         specifications_data = validated_data.pop('specifications', [])
        
#         validated_data['vendor'] = self.context['request'].user
#         equipment = Equipment.objects.create(**validated_data)
        
#         for index, image_data in enumerate (images_data):
#             EquipmentImage.objects.create(equipment=equipment, image=image_data,
#             is_primary = (index==0)
#             )
        
#         for order, spec_data in enumerate (specifications_data):
#             EquipmentSpecification.objects.create(
#                 equipment=equipment,
#                 key=spec_data.get('key'),
#                 value=spec_data.get('value'),
#                 order = order
#             )
        
#         return equipment
    
# class EquipmentUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Equipment
#         fields = [
#             'name', 'description', 'category', 'equipment_type', 'condition', 'price', 'rental_price_per_day', 'is_available'
#         ]

#     def validate(self, attrs):
#         equipment = self.instance
        
#         if data.get('equipment_type', equipment.equipment_type) in ['sale', 'both'] and not data.get('price', equipment.price):
#             raise serializers.ValidationError({"price": "Price is required for equipment available for sale."})
        
#         # Validate that rental price is provided for rental equipment
#         if data.get('equipment_type', equipment.equipment_type) in ['rent', 'both'] and not data.get('rental_price_per_day', equipment.rental_price_per_day):
#             raise serializers.ValidationError({"rental_price_per_day": "Rental price per day is required for equipment available for rent."})
        
#         return data
    

# class EquipmentSearchSerializer(serializers.Serializer):
#     query = serializers.CharField(required=False)
#     category = serializers.IntegerField(required=False)
#     equipment_type = serializers.ChoiceField(choices=Equipment.EQUIPMENT_TYPES, required=False)
#     condition = serializers.ChoiceField(choices=Equipment.CONDITIONS, required=False)
#     min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
#     max_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
#     min_rental_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
#     max_rental_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

class EquipmentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentCategory
        fields = '__all__'


class EquipmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentImage
        fields = ['id', 'image', 'is_primary', 'uploaded_at']


class MedicalEquipmentSerializer(serializers.ModelSerializer):
    images = EquipmentImageSerializer(many = True, read_only = True)
    category_name = serializers.CharField(source = 'category.name', read_only = True)
    vendor_name = serializers.CharField(source ='vendor.get_full_name', read_only = True)

    class Meta:
        model = Equipment
        field = '__all__'
        read_only_fields = ['is_verified', 'qr_code', 'qr_code_date', 'created_at', 'updated_at']


class EquipmentInspectionSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source = 'equipment.name', read_only = True)
    inspector_name = serializers.CharField(source = 'inspector.get_full_name', read_only = True)

    class Meta:
        model = EquipmentInspection
        fields = '__all__'