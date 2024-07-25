from rest_framework import serializers #type: ignore
from .models import SupportMessage


class SupportMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportMessage
        fields = '__all__'
