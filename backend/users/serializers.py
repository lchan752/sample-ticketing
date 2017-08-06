from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name")

    class Meta:
        model = User
        fields = ['id', 'full_name', 'is_manager', 'avatar']