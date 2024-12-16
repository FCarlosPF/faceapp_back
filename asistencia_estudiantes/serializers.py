from rest_framework import serializers
from .models import Estudiante, Clase, RegistroAsistencia, CaracteristicasFaciales

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'

class ClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clase
        fields = '__all__'

class RegistroAsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroAsistencia
        fields = '__all__'

class CaracteristicasFacialesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaracteristicasFaciales
        fields = '__all__'