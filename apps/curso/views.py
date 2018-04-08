import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import HttpResponse
from apps.curso.serializers import ProgramaSerializer,CursoPrefSerializer
from apps.curso.models import Programa,Preferencia,Curso
# Create your views here.

class ProgramasCursoList(APIView):
    serializer=ProgramaSerializer
    def get(self, request):
        programas=Programa.objects.all()
        response = self.serializer(programas,many=True)
        print(response.data)
        return Response(response.data)

class ProgramaDocenteLista(APIView):
    serializer=CursoPrefSerializer
    def get(self,request,pk):
        preferencias = Preferencia.objects.filter(id_docente=pk).values()           #filter(id_docente=pk)
        cursos=[]
        for preferencia in preferencias:
            curso=Curso.objects.get(id_curso=preferencia['id_curso_id'])
            serializer=self.serializer(curso)
            cursos.append(serializer.data)
        return Response(cursos)

    #def post(self,request,pk):