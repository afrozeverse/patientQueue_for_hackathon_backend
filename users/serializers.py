from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields='__all__'

    def validate(self,data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Password must match')
        return data
    
    def create(self,validate_data):
        user=User.objects.create_user(
            phone=validate_data['phone'],
            password=validate_data['password']
        )
        return user