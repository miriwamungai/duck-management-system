from django.forms import model_to_dict
from rest_framework import serializers

from .models import Veterinary




class VeterinarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Veterinary
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.response = validated_data.get("response", instance.response)
        instance.save()
        return instance



