from rest_framework.serializers import ModelSerializer
from apps.docente.models import Docente


class DocenteSerializer(ModelSerializer):
    class Meta:
        model = Docente
        fields = '__all__'
