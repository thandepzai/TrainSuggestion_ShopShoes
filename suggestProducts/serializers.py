from rest_framework.serializers import ModelSerializer
from .models import SessionList


class SessionListSerializer(ModelSerializer):
    class Meta:
        model = SessionList
        fields = ["id", "listCodeProduct", "status"]
