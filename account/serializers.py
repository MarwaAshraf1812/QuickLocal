from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password


class SingUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True, allow_blank=False, validators=[
        validators.MinLengthValidator(8),
        validate_password,
    ])

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'confirm_password')

        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'username': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'password': {'required': True, 'allow_blank': False, 'min_length': 8}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": _("Password fields do not match.")})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password from User creation
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'full_name')

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}" if obj.first_name or obj.last_name else obj.username

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['email'] = instance.email.lower()
        representation['username'] = instance.username.lower()
        return representation


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'city', 'state', 'zip_code', 'country', 'profile_picture', 'date_of_birth', 'gender', 'preferred_language', 'currency']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        user = self.context['request'].user

        # Validate old password
        if not check_password(attrs['old_password'], user.password):
            raise serializers.ValidationError({"old_password": "Old password is not correct."})

        # Validate new password
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"new_password": "New password and confirm password do not match."})

        # Validate password complexity
        try:
            validate_password(attrs['new_password'], user)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"new_password": e.messages})

        return attrs

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

