from rest_framework.serializers import ModelSerializer,SlugRelatedField,PrimaryKeyRelatedField,ListField
from apps.curso.models import Programa, Curso, Preferencia, Ciclo


class CursoSerializer(ModelSerializer):
    class Meta:
        model= Curso
        fields = ('id_curso','nom_curso','id_programa','numciclo')

class ProgramaSerializer(ModelSerializer):
    cursos = CursoSerializer(many=True)

    class Meta:
        model = Programa
        fields = ('id_programa', 'nom_programa','id_tip_grado', 'cursos',)

class CursoPrefSerializer(ModelSerializer):
    class Meta:
        model= Curso
        fields = '__all__'

class CicloSerializer(ModelSerializer):
    class Meta:
        model= Ciclo
        fields = '__all__'
"""
class PreferenciaSerializer(ModelSerializer):
    class Meta:
        model = Preferencia
        fields = ('id_preferencia','curso',)"""