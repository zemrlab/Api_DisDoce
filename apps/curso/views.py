import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import HttpResponse
from apps.curso.serializers import ProgramaSerializer,CursoPrefSerializer
from apps.curso.models import Programa,Preferencia,Curso
from apps.docente.models import Docente
from rest_framework import status

# Create your views here.

class ProgramasCursoList(APIView):
    serializer=ProgramaSerializer
    def get(self, request):
        programas=Programa.objects.all()
        response = self.serializer(programas,many=True)
        return Response(response.data)

class ProgramaDocenteLista(APIView):
    serializer=CursoPrefSerializer
    def get(self,request,pk):
        preferencias = Preferencia.objects.filter(id_docente=pk).values()
        cursos=[]
        for preferencia in preferencias:
            curso=Curso.objects.get(id_curso=preferencia['id_curso_id'])
            serializer=self.serializer(curso)
            cursos.append(serializer.data)
        return Response(cursos)

    def post(self,request,pk):
        Preferencia.objects.filter(id_docente=pk).delete()
        lista=request.data
        listaProgramas=lista['seleccion']
        id_inicial = Preferencia.objects.count() + 1
        for programa in listaProgramas:
            for curso in programa['cursos']:
                Preferencia.objects.create(
                                            id_preferencia=id_inicial,
                                            id_curso=Curso.objects.get(pk=curso['id_curso']),
                                            id_docente=Docente.objects.get(pk=pk),
                                            )
                id_inicial=id_inicial+1
        return Response(lista, status=status.HTTP_201_CREATED)
