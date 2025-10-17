from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
# from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ['profile_picture', 'date_of_birth', 'national_id', 'pan_number', 'bio']


# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only = True, validators = [validate_password])
#     password2 = serializers.CharField(write_only = True)
#     profile = UserProfileSerializer(required = False)

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'user_type', 'phone', 'address', 'city', 'state', 'pincode', 'first_name', 'last_name', 'is_verified', 'profile', 'password', 'password2')
#         def validate(self, attrs):
#             if attrs['password'] != attrs['password2']:
#                 raise serializers.ValidationError({"password": "password field does not match."})
#             return attrs
        
#         def create(self, validated_date):
#             profile_data = validated_date.pop('profile', None)
#             validated_date.pop('password2')
#             user = User.objects.create_user(**validated_date)

#             if profile_data:
#                 UserProfile.objects.create(user=user, **profile_data)
#             else:
#                 UserProfile.objects.create(user=user)
#             return user

# # class UserProfileSerializer(serializers.ModelSerializer):
# #     user = serializers.StringRelatedField(read_only = True)

# #     class Meta:
# #         model = UserProfile
# #         fields = ('id', 'username', 'email', 'user_type', 'phone', 'address', 'city', 'state', 'pincode', 'first_name', 'last_name', 'is_verified', 'profile')

# class UserSerializer(serializers.ModelSerializer):
#     model = User
#     fields = ('id', 'username', 'email', 'user_type', 'phone', 'address', 'city', 'state', 'pincode', 'first_name', 'last_name', 'is_verified', 'profile', 'date_joined')
#     read_only_fields = ('id', 'date_joined', 'is_verified')


# class ChangePasswordSerializer(serializers.ModelSerializer):
#     old_password = serializers.CharField(required = True)
#     new_password = serializers.CharField(required = True, validators = [validate_password])

#     def validate_old_password (self, value):
#         user = self.context['request'].user
#         if not user.check_password(value):
#             raise serializers.ValidationError('Old password is not correct.')
#         return value
    

# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only = True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_type', 'phone_number', 'address', 'city', 'state', 'pincode', 'is_verified', 'profile']
        read_only_fields = ['id', 'is_verified']


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required = True, validators = [UniqueValidator(queryset = User.objects.all())])     
    username = serializers.CharField(required = True, validators = [UniqueValidator(queryset = User.objects.all())])     
    password = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'user_type', 'phone_number', 'first_name', 'last_name', 'address', 'city', 'state', 'pincode']
        extra_kwargs = {
            'first_name': {'required':True},
            'last_name': {'required':True},
            'phone_number':{'required': True},
        }
        

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password':'Password fields did not match.'})
        
        phone = attrs.get('phone_number', '')
        if not phone.startswith('+91') and len(phone) == 10:
            attrs['phone_number'] = f"+91{phone}"

        return attrs

    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user = user)

        return user
        

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username = username, password = password)
            if not user:
                try:
                    user_obj = User.objects.get(email = username)
                    user = authenticate(username = user_obj.username, password= password)
                except User.DoesNotExist:
                    pass

            if not user:
                raise serializers.ValidationError('unable to login in with the provided credientials.')
            if not user.is_active:
                raise serializers.ValidationError('User Account is disabled')
        else:
            raise serializers.ValidationError('Must include "username" and "password".')
        attrs['user'] = user
        return attrs

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required = True, write_only = True)
    new_password = serializers.CharField(required = True, validators = [validate_password])
    new_password2 = serializers.CharField(required = True)

    def validate (self, attrs):
        if attrs ['new_password'] != attrs['newpasword2']:
            raise serializers.ValidationError({'new_password':'Password field didnot match.'})
        return attrs
    

class PasswordResetRequestSerializer(serializers.ModelSerializer):
    token = serializers.CharField(required = True)
    uid = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs

class UserUpdateSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number', 'address',
            'city', 'state', 'pincode', 'profile'
        ]
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        
        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update profile if provided
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance