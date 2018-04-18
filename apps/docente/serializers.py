from rest_framework.serializers import ModelSerializer
from apps.docente.models import Docente


class DocenteSerializer(ModelSerializer):
    class Meta:
        model = Docente
        fields = ('id',
                  'nombres',
                  'fecha_nac',
                  'apell_pat',
                  'apell_mat',
                  'genero',
                  'email',
                  'pais',
                  'direccion',
                  'celular',
                  'codigo',)
