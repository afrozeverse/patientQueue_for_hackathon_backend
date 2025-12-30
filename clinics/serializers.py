from rest_framework import serializers
from .models import ClinicProfile, Session

class ClinicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=ClinicProfile
        fields='__all__'

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Session
        fields='__all__'
