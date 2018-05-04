import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import HttpResponse
from apps.curso.serializers import ProgramaSerializer,CursoPrefSerializer,CursoSerializer
from apps.curso.models import Programa,Preferencia,Curso
from apps.docente.models import Docente
from rest_framework import status

# Create your views here.

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
    def get(self,request,pk):
        preferencias = Preferencia.objects.filter(id_docente=pk).values()  # filter(id_docente=pk)
        cursos = []
        for preferencia in preferencias:
            curso = Curso.objects.get(id_curso=preferencia['id_curso_id'])
            serializer = self.serializerCurso(curso)
            cursos.append(serializer.data)
        return Response(cursos)

    def post(self,request,pk):
        Preferencia.objects.filter(id_docente=pk).delete()
        lista=request.data
        listaprogramas=lista['coursesSelection']
        id_inicial = 0
        for programa in listaprogramas:
            for curso in programa['cursos']:
                while Preferencia.objects.filter(id_preferencia=id_inicial).exists():
                    id_inicial=id_inicial+1
                Preferencia.objects.create(
                                            id_preferencia=id_inicial,
                                            id_curso=Curso.objects.get(pk=curso['id_curso']),
                                            id_docente=Docente.objects.get(pk=pk)
                                            )
                id_inicial=id_inicial+1
        return Response(lista, status=status.HTTP_201_CREATED)
