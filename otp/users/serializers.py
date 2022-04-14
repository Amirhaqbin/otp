from django.dispatch import receiver
from .models import OtpRequest
from django.db import models
from rest_framework import serializers


class OtpRequestSerializer(serializers.Serializer):
    receiver = serializers.CharField(max_length=50, allow_null=False)
    channel = serializers.ChoiceField(allow_null=False, choices= OtpRequest.OtpChannel.choices)

class OtpResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpRequest
        fields = ['request_id']

class VerfyOtpRequestSerializer(serializers.Serializer):
    request_id = serializers.UUIDField(allow_null=False)
    password = serializers.CharField(max_length=4, allow_null=False)
    receiver = serializers.CharField(max_length=64, allow_null=False)

class ObtainTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=128, allow_null=False)
    refresh = serializers.CharField(max_length=128, allow_null=False)
    created = serializers.BooleanField()