from rest_framework import serializers
from .models import CustomUser, File

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            user_type=validated_data['user_type'],
        )
        return user

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file', 'uploader', 'uploaded_at']

    def validate_file(self, value):
        allowed_types = ['pptx', 'docx', 'xlsx']
        ext = value.name.split('.')[-1].lower()
        if ext not in allowed_types:
            raise serializers.ValidationError('Only pptx, docx, xlsx files are allowed.')
        return value
