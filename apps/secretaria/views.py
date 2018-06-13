from django.db import  connection
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.docente.models import Docente
from apps.disponibilidad.models import Dia
from apps.curso.models import Ciclo, Preferencia
from django.http import  HttpResponse
from reportlab.pdfgen import canvas
from Algoritmos.libreria_pdf import *
from reportlab.lib.pagesizes import letter,landscape
from Algoritmos.algoritmos_bd import dictfetchall
# Create your views here.
from apps.docente.serializers import DocenteSerializer
from apps.secretaria.serializers import PreferenciaSerializer


class ConsultaDocentePDF(APIView):
    def get(self,request,id,ciclo):
        response = HttpResponse(content_type='application/pdf')
        nombre_pdf='Consulta Docente '+id
        response['Content-Disposition'] = 'filename="'+nombre_pdf+'.pdf"'
        """try:
            informacion_docente=Docente.objects.get(id=id)
        except Docente.DoesNotExist:
            return Response('NO EXISTE DOCENTE',status=status.HTTP_400_BAD_REQUEST)"""
        p = canvas.Canvas(response)
        p.setTitle("Empezando...")

        p.setPageSize(landscape(letter))

        #Variables curso
        docente = Docente.objects.get(id=id)
        docente_nom = docente.nombres
        docente_apellidos = docente.apell_pat
        docente_tipo_documento=docente.tipo_document
        docente_documento=docente.nro_document

        #Variable ciclo
        ciclo = Ciclo.objects.get(nom_ciclo=ciclo)
        ciclo_nom=ciclo.nom_ciclo


        #Variables GLOBALES
        ancho_pagina,alto_pagina=letter

        #Variables:FORMULARIO TOTAL
        titulo_tipo_letra_form = 'Times-Bold'
        titulo_tamanio_letra_form = 12

        titulo_medio_tipo_letra_form = 'Times-Bold'
        titulo_medio_tamanio_letra_form = 16

        campo_tipo_letra_form = 'Times-Bold'
        campo_tamanio_letra_form = 10

        valor_tipo_letra_form = 'Times-Roman'
        valor_tamanio_letra_form = 10

        campo_radio_tipo_letra_form = 'Times-Bold'
        campo_radio_tamanio_letra_form = 10

        radio_tipo_letra_form = 'Times-Roman'
        radio_tamanio_letra_form = 10
        radio_longitud_radio = 2
        radio_espacio_nombre = 15

        switcher_formulario = {
            'titulo': titulo,
            'campo': campo,
            'campo_radio': campo,
            'campo_sgt': campo,
            'radio': radio,
            'linea': linea,
            'titulo_medio': titulo_medio,
            'valor': campo,
            'valor_x_variable': valor_x_variable,
        }
        switcher_salto_linea = {
            'titulo': 20,
            'campo': 0,
            'campo_sgt': 20,
            'campo_radio': 0,
            'radio': 20,
            'titulo_medio': 30,
            'valor': 20,
            'linea': 20,
            'valor_x_variable': 20,
        }

        switcher_padding_left = {
            'campo': 0,
            'campo_sgt': 0,
            'radio': 100,
            'campo_radio': 0,
            'valor': 100,
        }

        #Variables : Formulario docente
        x_formulario=ancho_pagina/2
        y_formulario=alto_pagina*(5.5/8)
        lista_form_docente = [
            {'titulo_medio': {'text': 'CONSULTAR POR DOCENTE',
                        'tipo_letra': titulo_tipo_letra_form,
                        'x_medio': x_formulario,
                        'cantidad_espacio_texto': 30,
                        'tamanio_letra': titulo_tamanio_letra_form}},
            {'campo': {'text': 'DOCENTE',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'valor': {'text': docente_nom+docente_apellidos,
                       'tipo_letra': valor_tipo_letra_form,
                       'tamanio_letra': valor_tamanio_letra_form}},
            {'campo': {'text':docente_tipo_documento,
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'valor': {'text': docente_documento,
                       'tipo_letra': valor_tipo_letra_form,
                       'tamanio_letra': valor_tamanio_letra_form}},
            {'campo': {'text': 'SEMESTRE',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'valor': {'text': ciclo_nom,
                       'tipo_letra': valor_tipo_letra_form,
                       'tamanio_letra': valor_tamanio_letra_form}},
        ]

        formulario(p, x_formulario, y_formulario, lista_form_docente,
                   switcher_formulario, switcher_salto_linea
                   , switcher_padding_left)


        #Variables : Tabla

        y_tabla = 350
        x_tabla = 60

        dias = Dia.objects.all()

        encabezados=[]
        detalles=[]
        for dia in dias :
            encabezados.append(dia.nom_dia)
            detalles

        detalles = [
            # Equipo             Descripción
            ('NOMBRE', "STEVE",'3',3),
            ('MARCA', "KHO",45,3),
            ('MODELO',"OK",5,4),
            ('SERIE',"NIAW",7,5)
        ]
        estilos = [
                # La primera fila(encabezados) va a estar centrada
                ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.green),
                # Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                # El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        tabla(p,encabezados,detalles,x_tabla,y_tabla,estilos)
        p.showPage()
        p.save()
        return response

class buscadorTotal(APIView):
    serializer_preferencia=PreferenciaSerializer
    serializer_docente=DocenteSerializer
    def post(self,request):
        data=request.data
        semestre=data['semestreFilter']
        curso=data['cursoFilter']
        docente=data['docenteFilter']
        dia=data['diaFilter']
        hora_inicio=data['horaInicio']
        hora_fin=data['horaFin']

        buscarValidar=[]

        buscarValidar.append((True if semestre != '' else False))
        buscarValidar.append((True if curso != '' else False))
        buscarValidar.append((True if docente != '' else False))
        buscarValidar.append((True if dia != '' else False))
        buscarValidar.append((True if hora_inicio != '' else False))
        buscarValidar.append((True if hora_fin != '' else False))

        print(buscarValidar)
        resultado = []
        cursor = connection.cursor()
        if buscarValidar[0] and buscarValidar[1]:
            sql1="""select d.id,d.nombres,(d.apell_pat|| ' '|| d.apell_mat) as apellido,d.nro_document,d.celular from preferencia p
                    join curso c on p.id_curso = c.id_curso
                    join docente d on p.id_docente = d.id
                    where c.nom_curso like '%"""+curso+"""%' and p.id_ciclo="""+semestre

            sqldisponibilidad="""select dis.id_disponibilidad as id,di.nom_dia as nombre,dis.hr_inicio as hinicio,dis.hr_fin as hfin from disponibilidad dis
                                    join docente d on dis.id_docente = d.id
                                    join dia di on dis.id_dia = di.id_dia
                                    where d.id=(%s)"""
            #docentes=[]
            #for prefe in preferencia:
             #   docentes.append(prefe.id_docente)
            cursor.execute(sql1)
            docentes=dictfetchall(cursor)
            for docente in docentes:
                cursor.execute(sqldisponibilidad,[docente['id']])
                disponibilidad=dictfetchall(cursor)
                docente['disponibilidad']=disponibilidad
                resultado.append(docente)
        return Response(resultado)
        #preferencia=Preferencia.objects.filter(id_ciclo__nom_ciclo__contains=semestre,id_curso__nom_curso__contains=curso)

        #preferenciaSerializado=self.serializer_preferencia(preferencia,many=True)

        #for prefe in preferencia:
        #   print(prefe.id_curso.nom_curso)

        #return Response(preferenciaSerializado.data)