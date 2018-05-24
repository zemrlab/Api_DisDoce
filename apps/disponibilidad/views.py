from django.db import connection
from django.shortcuts import render
import json
from rest_framework.views import APIView
from django.http import  HttpResponse
from rest_framework.response import Response
from apps.disponibilidad.serializers import DisponibilidadSerializer
from django.db.models.query import QuerySet
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
        horarios_intervalos=Disponibilidad.objects.filter(id_docente=pk).order_by('id_disponibilidad')
        disponibilidades=[disponibilidad for disponibilidad in horarios_intervalos.values()]
        array = devolver_disponibilidad(disponibilidades,8,14)
        return Response(json.dumps(array))
    def post(self, request, pk):
        Disponibilidad.objects.filter(id_docente=pk).delete()
        Diccionarios_intervalos=Descifrar_disponibilidad(json.dumps(request.data),7,14,8,'selection')
        id_inicial=Disponibilidad.objects.count()+1
        disponibilidades=[]
        for dia in Diccionarios_intervalos:
            for intervalos in Diccionarios_intervalos[dia]:

                disponibilidad=[id_inicial,pk,dia,intervalos[0],intervalos[1],intervalos[1]-intervalos[0]]
                """Disponibilidad.objects.create(
                                            id_disponibilidad=id_inicial,
                                            id_docente=Docente.objects.get(pk=pk),
                                            id_dia=Dia.objects.get(pk=dia),
                                            hr_inicio=intervalos[0],
                                            hr_fin=intervalos[1],
                                            tot_hrs=intervalos[1]-intervalos[0]
                                            )"""
                disponibilidades.append(disponibilidad)
                id_inicial=id_inicial+1
        cursor = connection.cursor()
        cursor.executemany('INSERT INTO disponibilidad (id_disponibilidad, id_docente, id_dia,hr_inicio,hr_fin,tot_hrs) VALUES (%s, %s, %s,%s,%s,%s)', disponibilidades)
        cursor.close()
        estado={}
        estado['estado']='correcto'
        return Response(estado, status=status.HTTP_201_CREATED)