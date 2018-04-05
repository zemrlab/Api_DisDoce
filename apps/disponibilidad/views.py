from django.shortcuts import render
import json
from rest_framework.views import APIView
from django.http import  HttpResponse
from rest_framework.response import Response
from apps.disponibilidad.serializers import DisponibilidadSerializer
from apps.disponibilidad.models import Disponibilidad,Dia
from apps.docente.models import Docente
from rest_framework import status

#MIS ALGORITMOS
from Algoritmos.Algoritmos_Disponibilidad import Descifrar_disponibilidad,devolver_disponibilidad
#

# Create your views here.

class DisponibilidadList(APIView):
    serializer = DisponibilidadSerializer
    def get(self, request, pk):
        #lista = Disponibilidad.objects.all() #para mostrar las disponibilidad
        array = devolver_disponibilidad(pk,8)
        #response = self.serializer(lista, many=True) #para mostrar todos las listas
        return Response(json.dumps(array))

    def post(self, request, pk):
        Diccionarios_intervalos=Descifrar_disponibilidad(json.dumps(request.data),7,14,8,'selection')
        id_inicial=Disponibilidad.objects.count()+1
        print(Diccionarios_intervalos)
        for dia in Diccionarios_intervalos:
            for intervalos in Diccionarios_intervalos[dia]:
                disponibilidad=Disponibilidad.objects.create(
                                            id_disponibilidad=id_inicial,
                                            id_docente=Docente.objects.get(pk=pk),
                                            id_dia=Dia.objects.get(pk=dia),
                                            hr_inicio=intervalos[0],
                                            hr_fin=intervalos[1],
                                            tot_hrs=intervalos[1]-intervalos[0]
                                            )
                serializer = DisponibilidadSerializer(data=disponibilidad) #cambiar por self.serializer
                if serializer.is_valid():
                    serializer.save()
                id_inicial=id_inicial+1
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)