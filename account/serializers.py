from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.utils.translation import gettext_lazy as _


class SingUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True, allow_blank=False, validators=[
        validators.MinLengthValidator(8),
        validate_password,
         ])
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'confirm_password')

        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
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
