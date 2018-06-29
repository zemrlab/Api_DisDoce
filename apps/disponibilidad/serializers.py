from rest_framework.serializers import ModelSerializer
from apps.disponibilidad.models import Disponibilidad,Dia


class DisponibilidadSerializer(ModelSerializer):
    class Meta:
        model = Disponibilidad
        fields = ('id_disponibilidad','id_docente','id_dia','hr_inicio', 'hr_fin', 'tot_hrs')

class DiaSerializer(ModelSerializer):
    class Meta:
        model = Dia
        fields = '__all__'
