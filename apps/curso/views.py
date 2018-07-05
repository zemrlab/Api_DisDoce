import json

from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.curso.serializers import ProgramaSerializer, CursoPrefSerializer, CursoSerializer, CicloSerializer, \
    PreferenciaSerializer
from apps.curso.models import Programa, Preferencia, Curso, Ciclo
from apps.docente.models import Docente
from rest_framework import status,generics

# Create your views here.
from apps.docente.serializers import DocenteSerializer
from apps.disponibilidad.models import Disponibilidad


class ProgramasCursoList(APIView):
    serializer=ProgramaSerializer
    def get(self, request):
        programas=Programa.objects.filter(vigencia_programa=True)
        response = self.serializer(programas,many=True)
        for programa in response.data:
            programa['id_tip_grado']=int(programa['id_tip_grado'])
            for curso in programa['cursos']:
                #curso['numciclo']=curso['numciclo'].replace(" ","");
                curso['numciclo']=int(curso['numciclo'])
        #programas={'programas':response.data}
        return Response(response.data)

class ProgramaDocenteLista(APIView):
    serializerCurso=CursoSerializer
    serializerPrograma=ProgramaSerializer
    def get(self,request,pk,ciclo):
        preferencias = Preferencia.objects.filter(id_docente=pk,id_ciclo=ciclo).values()  # filter(id_docente=pk)
        cursos = []
        for preferencia in preferencias:
            curso = Curso.objects.get(id_curso=preferencia['id_curso_id'])
            serializer = self.serializerCurso(curso)
            cursos.append(serializer.data)
        return Response(cursos)

    def post(self,request,pk,ciclo):
        Preferencia.objects.filter(id_docente=pk,id_ciclo=ciclo).delete()
        lista=request.data
        listaprogramas=lista['coursesSelection']
        preferencias = []
        for programa in listaprogramas:
            for curso in programa['cursos']:
                preferencia=[curso['id_curso'],int(pk),int(ciclo)]

                """Preferencia.objects.create(
                                            id_preferencia=id_inicial,
                                            id_curso=Curso.objects.get(pk=curso['id_curso']),
                                            id_docente=Docente.objects.get(pk=pk)
                                            )
                                            """
                preferencias.append(preferencia)
        cursor = connection.cursor()
        cursor.executemany('INSERT INTO preferencia (id_curso, id_docente,id_ciclo) VALUES (%s, %s,%s)',preferencias)
        cursor.close()
        return Response(lista, status=status.HTTP_201_CREATED)

class CicloList(generics.ListAPIView):
    serializer_class = CicloSerializer
    queryset = Ciclo.objects.all().order_by('-id_ciclo')

class CicloCreate(generics.CreateAPIView):
    serializer_class = CicloSerializer
    queryset = Ciclo.objects.all()

class CicloGetUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = CicloSerializer
    queryset = Ciclo.objects.all()

    def get(self, request,pk):
        try:
            ciclo = Ciclo.objects.get(id_ciclo=pk)
        except Ciclo.DoesNotExist:
            return Response('NO EXISTE CICLO', status=status.HTTP_400_BAD_REQUEST)
        serializer=self.serializer_class(ciclo)
        return Response(serializer.data)

class CicloListHabilitados(generics.ListAPIView):
    serializer_class = CicloSerializer
    queryset = Ciclo.objects.all().filter(estado=True).order_by('-id_ciclo')

class cicloListUpdate(APIView):
    def post(self,request):
        ciclos=request.data
        cursor = connection.cursor()
        ids=[]
        sql="""update ciclo set nom_ciclo=(%s),fecha_inicio=(%s),fecha_fin=(%s),estado=(%s)  where id_ciclo=(%s)"""
        for ciclo in ciclos:
            ids.append(ciclo['id_ciclo'])
            cursor.execute(sql,[ciclo['nom_ciclo'],ciclo['fecha_inicio'],ciclo['fecha_fin'],ciclo['estado'],ciclo['id_ciclo']])
        cursor.close()
        Ciclo.objects.exclude(id_ciclo__in=ids).delete()
        return Response("completado")

"""  ALEJANDRO HABLAR
class CicloCursoList(generics.ListAPIView):
    serializer_class = CursoSerializer

    def get_queryset(self):
        ciclo = self.request.query_params.get('ciclo')

        if ciclo:
            queryset = Curso.objects.filter(id_ciclo=ciclo)
            queryset.

        return queryset"""