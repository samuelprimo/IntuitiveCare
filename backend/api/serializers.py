from rest_framework import serializers
from api.models import Operadora

class OperadoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operadora
        fields = '__all__'