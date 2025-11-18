from rest_framework import serializers
from .models import Franchise, FranchisePerformance

class FranchiseSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source = 'owner.get_full_name', read_only = True)
    warehouse_name = serializers.CharField(source = 'warehouse.name', read_only = True)

    class Meta:
        model = Franchise
        fields = '__all__'


class FranchisePerformanceSerializer(serializers.ModelSerializer):
    franchise_name = serializers.CharField (source = 'franchise.name', read_only = True)

    class Meta:
        model = FranchisePerformance
        fields = '__all__'


class FranchiseRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only = True)
    email = serializers.EmailField(write_only = True)
    password = serializers.CharField(write_only = True)
    phone_number = serializers.CharField(write_only = True)

    class Meta:
        model = Franchise
        fields = [
            'username', 'email', 'password', 'phone_number', 'name', 'address', 'city', 'state', 'pincode', 'contact_number', 'email', 'warehouse'
        ]

        def create(self, validated_data):
            from users.models import User
            user_data = {
                'username': validated_data.pop('username'),
                'email': validated_data.pop('email'),
                'password': validated_data.pop('password'),
                'phone_number': validated_data.pop('phone_number'),
                'user_type': 'franchise'
            }
            
            user = User.objects.create_user(**user_data)
            
            # Create franchise
            franchise = Franchise.objects.create(owner=user, **validated_data)
            return franchise