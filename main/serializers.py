from rest_framework import serializers
from .models import IrisPlant

class IrisPlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = IrisPlant
        fields = '__all__'