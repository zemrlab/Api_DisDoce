from rest_framework.serializers import ModelSerializer,Serializer
from apps.disponibilidad.models import Disponibilidad


class DisponibilidadSerializer(ModelSerializer):
    class Meta:
        model = Disponibilidad
        fields = ('id_disponibilidad','id_docente','id_dia','hr_inicio', 'hr_fin', 'tot_hrs')

