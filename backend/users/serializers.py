from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'date_of_birth', 'national_id', 'pan_number', 'bio']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, validators = [validate_password])
    password2 = serializers.CharField(write_only = True)
    profile = UserProfileSerializer(required = False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'user_type', 'phone', 'address', 'city', 'state', 'pincode', 'first_name', 'last_name', 'is_verified', 'profile', 'password', 'password2')
        def validate(self, attrs):
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError({"password": "password field does not match."})
            return attrs
        
        def create(self, validated_date):
            profile_data = validated_date.pop('profile', None)
            validated_date.pop('password2')
            user = User.objects.create_user(**validated_date)

            if profile_data:
                UserProfile.objects.create(user=user, **profile_data)
            else:
                UserProfile.objects.create(user=user)
            return user

# class UserProfileSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(read_only = True)

#     class Meta:
#         model = UserProfile
#         fields = ('id', 'username', 'email', 'user_type', 'phone', 'address', 'city', 'state', 'pincode', 'first_name', 'last_name', 'is_verified', 'profile')

class UserSerializer(serializers.ModelSerializer):
    model = User
    fields = ('id', 'username', 'email', 'user_type', 'phone', 'address', 'city', 'state', 'pincode', 'first_name', 'last_name', 'is_verified', 'profile', 'date_joined')
    read_only_fields = ('id', 'date_joined', 'is_verified')


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required = True, validators = [validate_password])

    def validate_old_password (self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is not correct.')
        return value
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)