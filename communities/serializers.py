from .models import Field
from rest_framework import serializers


class FieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Field
        fields = [
            'name',
            'field_type',
            'required',
        ]