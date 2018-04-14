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
        programas=Programa.objects.all()
        response = self.serializer(programas,many=True)
        #programas={'programas':response.data}
        return Response(response.data)

class ProgramaDocenteLista(APIView):
    serializerCurso=CursoSerializer
    serializerPrograma=ProgramaSerializer
    def get(self,request,pk):
        preferencias = Preferencia.objects.filter(id_docente=pk).values()
        programas=[]
        cursos={}
        for preferencia in preferencias:
            curso=Curso.objects.get(id_curso=preferencia['id_curso_id'])
            if curso.id_programa not in cursos :
                cursos[curso.id_programa]=[]
            serializercurso=self.serializerCurso(curso)
            cursos[curso.id_programa].append(serializercurso.data)
        for key in cursos.keys():
            serializerprograma=self.serializerPrograma(key)
            listaprogramas=serializerprograma.data
            listaprogramas['cursos']=cursos[key]
            programas.append(listaprogramas)
        seleccion={'seleccion':programas}
        return Response(seleccion)

    def post(self,request,pk):
        Preferencia.objects.filter(id_docente=pk).delete()
        lista=request.data
        listaProgramas=lista['seleccion']
        id_inicial = Preferencia.objects.count() + 1
        for programa in listaProgramas:
            for curso in programa['cursos']:
                while Preferencia.objects.filter(id_preferencia=id_inicial).exists():
                    id_inicial=id_inicial+1
                Preferencia.objects.create(
                                            id_preferencia=id_inicial,
                                            id_curso=Curso.objects.get(pk=curso['id_curso']),
                                            id_docente=Docente.objects.get(pk=pk),
                                            )
                id_inicial=id_inicial+1
        return Response(lista, status=status.HTTP_201_CREATED)
