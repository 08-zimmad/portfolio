from django.contrib.auth import get_user_model
from rest_framework import serializers
from my_portal.models import Portfolio, Experience, Certificates

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "user_type"]

    def create(self, validated_data):
        validated_password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(validated_password)
        user.save()
        return user


class PortfolioApiViewSerializer(serializers.ModelSerializer):
    class Meta:

        model = Portfolio
        fields = ['first_name', 'last_name', 'full_name', 'email']

class EducationAPIViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experience
        fields = '__all__'


class CertificatesAPIViewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Certificates
        fields = '__all__'

