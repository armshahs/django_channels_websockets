from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        read_only_fields = (
            "created_at",
            "updated_at",
        )
        fields = (
            "title",
            "desc",
            "is_complete",
            "created_at",
            "updated_at",
            "owner",
        )
