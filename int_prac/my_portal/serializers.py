from django.contrib.auth import get_user_model
from rest_framework import serializers

from my_portal.models import Certificates, Education, Experience, Portfolio

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
        fields = ["first_name", "last_name", "full_name", "email", "user"]


class EducationAPIViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"


class CertificatesAPIViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificates
        fields = "__all__"


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = "__all__"


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"

    def validate(self, attr):
        attr
        if attr.get("is_currently_working") == True:
            attr["end_date"] = None

        return attr


class CertificatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificates
        fields = "__all__"
