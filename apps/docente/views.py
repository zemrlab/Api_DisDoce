
import json
from django.shortcuts import render
from rest_framework.views import APIView
from apps.docente.serializers import DocenteSerializer
from rest_framework.response import Response
from apps.docente.models import Docente
from django.http import  HttpResponse
# Create your views here.

class DocenteList(APIView):
    serializer = DocenteSerializer
    def get(self, request, id):
        lista = Docente.objects.get(id_docente=id)
        response=self.serializer(lista)
        return Response(response.data)