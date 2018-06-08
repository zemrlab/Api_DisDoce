from django.contrib.gis import serializers
from rest_framework.serializers import ModelSerializer
from apps.curso.models import Preferencia
from apps.docente.models import Docente


class PreferenciaSerializer(ModelSerializer):
    class Meta:
        model = Preferencia
        fields = '__all__'

class DocenteSerializer(ModelSerializer):
    #apellidos=serializers.CharField(source="apell_pat")
    class Meta:
        model = Docente
        fields='_all__'