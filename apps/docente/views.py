
import json
from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from apps.docente.serializers import DocenteSerializer
from rest_framework.response import Response
from apps.docente.models import Docente,DatosAcademicos,TipoGrado
from django.http import  HttpResponse
from reportlab.pdfgen import canvas
from Algoritmos.libreria_pdf import *
from reportlab.lib.pagesizes import letter
from PIL import Image
# Create your views here.

class DocenteList(APIView):
    serializer = DocenteSerializer
    def get(self, request, id):
        lista = Docente.objects.get(id_docente=id)
        response=self.serializer(lista)
        return Response(response.data)

class PDFView(APIView):
    def get(self,request,id):
        response = HttpResponse(content_type='application/pdf')
        nombre_pdf='docente'+id
        response['Content-Disposition'] = 'filename="'+nombre_pdf+'.pdf"'

        try:
            informacion_docente=Docente.objects.get(id_docente=id)
        except Docente.DoesNotExist:
            return HttpResponse('NO EXISTE DOCENTE')

        #variables docente
        docente_nom=informacion_docente.nom_docente
        docente_ape = informacion_docente.ape_docente
        docente_codigo = informacion_docente.codigo_docente
        docente_dni= informacion_docente.dni_docente
        docente_email = informacion_docente.email_docente
        docente_celular=informacion_docente.celular_docente
        docente_genero= informacion_docente.genero
        docente_pagina_web= informacion_docente.pagina_web
        docente_fecha_nac= informacion_docente.fecha_nac
        docente_pais= informacion_docente.pais
        docente_direccion= informacion_docente.direccion
        docente_sunedu_le= informacion_docente.sunedu_le
        docente_categoria= informacion_docente.categoria
        docente_regimen_dedicacion= informacion_docente.regimen_dedicacion
        docente_cv = informacion_docente.cv

        total_datos_academicos = DatosAcademicos.objects.filter(id_docente=id).values()
        docente_Grado={}
        for datos_academicos in total_datos_academicos:
            Nombre_Tipo_Grado=(TipoGrado.objects.get(id_tip_grado=datos_academicos['id_tip_grado_id'])).nom_tip_grado
            Nombre_Mencion_Grado=datos_academicos['mencion_grado']
            print(Nombre_Tipo_Grado)
            print(Nombre_Mencion_Grado)
            docente_Grado[Nombre_Tipo_Grado]=Nombre_Mencion_Grado

        #variabls de ayuda para pintar docente
        fin_direccion=35
        direccion_caracter_siguiente_linea=''

        if len(docente_direccion)>=35 :
            if docente_direccion[35]!=' ':
                direccion_caracter_siguiente_linea='-'

        docente_genero_radio = {'Masculino':False,'Femenino':False}

        if docente_genero=='M' :
            docente_genero_radio['Masculino']=True
        elif docente_genero=='F':
            docente_genero_radio['Femenino']=True

        p = canvas.Canvas(response)

        #variables globales
        ancho_pagina,alto_pagina=letter
        espacio_medio_left_right=6
        y_informacion_personal=238
        y_informacion_academica=10

        #variables:FORMULARIO TOTAL
        titulo_tipo_letra_form='Times-Bold'
        titulo_tamanio_letra_form=16

        titulo_medio_tipo_letra_form = 'Times-Bold'
        titulo_medio_tamanio_letra_form = 16

        campo_tipo_letra_form = 'Times-Roman'
        campo_tamanio_letra_form = 12

        valor_tipo_letra_form= 'Times-Roman'
        valor_tamanio_letra_form = 12

        campo_radio_tipo_letra_form = 'Times-Roman'
        campo_radio_tamanio_letra_form = 12

        radio_tipo_letra_form = 'Times-Roman'
        radio_tamanio_letra_form = 12
        radio_longitud_radio=3
        radio_espacio_nombre=15

        switcher_formulario = {
            'titulo': titulo,
            'campo': campo,
            'campo_radio': campo,
            'radio': radio,
            'titulo_medio':titulo_medio,
            'valor': campo,
        }
        switcher_salto_linea = {
            'titulo': 40,
            'campo': 20,
            'campo_radio': 15,
            'radio': 20,
            'titulo_medio': 30,
            'valor': 20,
        }

        switcher_padding_left = {
            'campo': 15,
            'radio': 40,
            'campo_radio': 15,
            'valor': 25,
        }

        #variables:titulo1
        tamanio_letra_titulo1=19
        texto_titulo1='DISPONIBILIDAD DEL DOCENTE'
        tipo_letra_titulo1='Times-Bold'
        cantidad_pixeles_titulo1=295
        padding_titulo_bottom_top_titulo1=15
        padding_titulo_left_right_titulo1=130
        x_titulo1=ancho_pagina/2-cantidad_pixeles_titulo1/2
        y_titulo1=800


        #variables:titulo2_1
        tamanio_letra_titulo2_1=17
        texto_titulo2_1 ='Informacion personal'
        tipo_letra_titulo2_1='Times-Bold'
        cantidad_pixeles_titulo2_1=155
        padding_titulo_bottom_top_titulo2_1=10
        padding_titulo_left_right_titulo2_1=180
        x_titulo2_1 = ancho_pagina/2-cantidad_pixeles_titulo2_1/2
        y_titulo2_1 = 490

        #variables:titulo2_2
        tamanio_letra_titulo2_2=17
        texto_titulo2_2 = 'Informacion academica'
        tipo_letra_titulo2_2='Times-Bold'
        cantidad_pixeles_titulo2_2=150
        padding_titulo_bottom_top_titulo2_2=10
        padding_titulo_left_right_titulo2_2=185
        x_titulo2_2 = ancho_pagina/2-cantidad_pixeles_titulo2_2/2
        y_titulo2_2 = 198

        #variables:Imagen
        x_imagen=60
        y_imagen=530
        ancho_porcentaje_imagen=27
        alto_porcentaje_imagen=30

        #variables:Cursos form
        ancho_cursos=250
        alto_cursos=235
        x_cursos=ancho_pagina/2+espacio_medio_left_right
        y_cursos=530
        x_form_cursos=x_cursos+ancho_cursos*(1/8)
        y_form_cursos=y_cursos+alto_cursos*(7/ 8)

        lista_form_cursos = [
            {'titulo': {'text': 'Cursos',
                        'tipo_letra': titulo_tipo_letra_form,
                        'tamanio_letra': titulo_tamanio_letra_form}},
            {'campo': {'text': 'Curso1',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'campo': {'text': 'Curso2',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'campo': {'text': 'Curso3',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
        ]


        #variables:informacion_personal1 form
        ancho_informacion_personal1=250
        alto_informacion_personal1=235
        x_informacion_personal1=ancho_pagina/2-ancho_informacion_personal1-espacio_medio_left_right
        y_informacion_personal1=y_informacion_personal
        x_form_informacion_personal1 = x_informacion_personal1 + ancho_informacion_personal1 * (1 / 8)
        y_form_informacion_personal1 = y_informacion_personal1 + alto_informacion_personal1 * (7 / 8)

        lista_form_informacion_personal1 = [
            {'campo': {'text': 'Nombres',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'valor': {'text': docente_nom,
                       'tipo_letra': valor_tipo_letra_form,
                       'tamanio_letra': valor_tamanio_letra_form}},
            {'campo': {'text': 'Apellidos',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'valor': {'text': docente_ape,
                       'tipo_letra': valor_tipo_letra_form,
                       'tamanio_letra': valor_tamanio_letra_form}},
            {'campo': {'text': 'DNI',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'valor': {'text': docente_dni,
                       'tipo_letra': valor_tipo_letra_form,
                       'tamanio_letra': valor_tamanio_letra_form}},
            {'campo_radio': {'text': 'Sexo',
                             'tipo_letra': campo_radio_tipo_letra_form,
                             'tamanio_letra': campo_radio_tamanio_letra_form}},
            {'radio': {'text': 'Masculino',
                       'tipo_letra': radio_tipo_letra_form,
                       'radio': radio_longitud_radio,
                       'Marcado': docente_genero_radio,
                       'espacio_nombre': radio_espacio_nombre,
                       'tamanio_letra': radio_tamanio_letra_form}},
            {'radio': {'text': 'Femenino',
                       'tipo_letra': radio_tipo_letra_form,
                       'radio': radio_longitud_radio,
                       'Marcado': docente_genero_radio,
                       'espacio_nombre': radio_espacio_nombre,
                       'tamanio_letra': radio_tamanio_letra_form}},
            {'campo': {'text': 'Correo',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'valor': {'text': docente_email,
                       'tipo_letra': valor_tipo_letra_form,
                       'tamanio_letra': valor_tamanio_letra_form}},
        ]

        #variables:informacion_personal2 form
        ancho_informacion_personal2 = 250
        alto_informacion_personal2 = 235
        x_informacion_personal2 = ancho_pagina/2+espacio_medio_left_right
        y_informacion_personal2 = y_informacion_personal
        x_form_informacion_personal2 = x_informacion_personal2 + ancho_informacion_personal2 * (1 / 8)
        y_form_informacion_personal2 = y_informacion_personal2 + alto_informacion_personal2 * (7 / 8)

        lista_form_informacion_personal2 = [
            {'campo': {'text': 'Fecha de Nacimiento',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'valor': {'text': docente_fecha_nac.strftime('%m/%d/%Y'),
                       'tipo_letra': valor_tipo_letra_form,
                       'tamanio_letra': valor_tamanio_letra_form}},
            {'campo': {'text': 'Pais',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'valor': {'text': docente_pais,
                       'tipo_letra': valor_tipo_letra_form,
                       'tamanio_letra': valor_tamanio_letra_form}},
            {'campo': {'text': 'Direccion',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'valor': {'text': docente_direccion[:fin_direccion]+direccion_caracter_siguiente_linea,
                       'tipo_letra': valor_tipo_letra_form,
                       'tamanio_letra': valor_tamanio_letra_form}},
            {'valor': {'text': docente_direccion[fin_direccion:],
                       'tipo_letra': valor_tipo_letra_form,
                       'tamanio_letra': valor_tamanio_letra_form}},
            {'campo': {'text': 'Celular',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'valor': {'text': docente_celular,
                       'tipo_letra': valor_tipo_letra_form,
                       'tamanio_letra': valor_tamanio_letra_form}},
        ]
        # variables:informacion_academica1 form
        ancho_informacion_academica1 = 250
        alto_informacion_academica1 = 170
        x_informacion_academica1 = ancho_pagina/2-ancho_informacion_academica1-espacio_medio_left_right
        y_informacion_academica1 = y_informacion_academica
        x_form_informacion_academica1 = x_informacion_academica1 + ancho_informacion_academica1 * (1 / 8)
        y_form_informacion_academica1 = y_informacion_academica1 + alto_informacion_academica1 * (7 / 8)

        lista_form_informacion_academica1 = [
            {'campo': {'text': 'Codigo',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'valor': {'text': docente_codigo,
                       'tipo_letra': valor_tipo_letra_form,
                       'tamanio_letra': valor_tamanio_letra_form}},
            {'titulo_medio': {'text': 'Grados',
                              'x_medio': x_informacion_academica1+ancho_informacion_academica1*(1/2),
                              'cantidad_espacio_texto':40,
                              'tipo_letra': titulo_medio_tipo_letra_form,
                              'tamanio_letra': titulo_medio_tamanio_letra_form}},
            {'campo': {'text': 'Titulo Profesional',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'valor': {'text': docente_Grado.get('Titulo Profesional','NO TIENE'),
                       'tipo_letra': valor_tipo_letra_form,
                       'tamanio_letra': valor_tamanio_letra_form}},
            {'campo': {'text': 'Licenciatura',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'valor': {'text': docente_Grado.get('Licenciatura', 'NO TIENE'),
                       'tipo_letra': valor_tipo_letra_form,
                       'tamanio_letra': valor_tamanio_letra_form}},
        ]

        # variables:informacion_academica2 form
        ancho_informacion_academica2 = 250
        alto_informacion_academica2 = 170
        x_informacion_academica2 = ancho_pagina/2+espacio_medio_left_right
        y_informacion_academica2 = y_informacion_academica
        x_form_informacion_academica2 = x_informacion_academica2 + ancho_informacion_academica2 * (1 / 8)
        y_form_informacion_academica2 = y_informacion_academica2 + alto_informacion_academica2 * (7 / 8)

        lista_form_informacion_academica2 = [
            {'titulo_medio': {'text': 'PostGrados',
                              'x_medio': x_informacion_academica2 + ancho_informacion_academica2 * (
                                          1 / 2) - espacio_medio_left_right*2,
                              'cantidad_espacio_texto': 50,
                              'tipo_letra': titulo_medio_tipo_letra_form,
                              'tamanio_letra': titulo_medio_tamanio_letra_form}},
            {'campo': {'text': 'Maestria',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'valor': {'text': docente_Grado.get('Maestria', 'NO TIENE'),
                       'tipo_letra': valor_tipo_letra_form,
                       'tamanio_letra': valor_tamanio_letra_form}},
            {'campo': {'text': 'Especialidad',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'valor': {'text': docente_Grado.get('Especialidad', 'NO TIENE'),
                       'tipo_letra': valor_tipo_letra_form,
                       'tamanio_letra': valor_tamanio_letra_form}},
            {'campo': {'text': 'Doctorado',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'valor': {'text': docente_Grado.get('Doctorado', 'NO TIENE'),
                       'tipo_letra': valor_tipo_letra_form,
                       'tamanio_letra': valor_tamanio_letra_form}},
        ]
        #titulo
        titulo_texto(p,texto_titulo1,x_titulo1,y_titulo1,
               tipo_letra_titulo1,tamanio_letra_titulo1,
               padding_titulo_left_right_titulo1,padding_titulo_bottom_top_titulo1,cantidad_pixeles_titulo1)

        #imagen profesor
        dibujar_imagen(p,'profesor.jpg',
                       x_imagen,
                       y_imagen,
                       ancho_porcentaje_imagen,
                       alto_porcentaje_imagen)

        #Cursos
        p.rect(x_cursos,y_cursos,ancho_cursos,alto_cursos)
        formulario(p,x_form_cursos,y_form_cursos,lista_form_cursos,switcher_formulario,switcher_salto_linea
                   ,switcher_padding_left)

        #titulo2_1
        titulo_texto(p,texto_titulo2_1,x_titulo2_1,y_titulo2_1,
               tipo_letra_titulo2_1,tamanio_letra_titulo2_1,
               padding_titulo_left_right_titulo2_1,padding_titulo_bottom_top_titulo2_1,cantidad_pixeles_titulo2_1)

        #informacion_personal1
        p.rect(x_informacion_personal1,y_informacion_personal1,ancho_informacion_personal1,alto_informacion_personal1)
        formulario(p,x_form_informacion_personal1,y_form_informacion_personal1,
                   lista_form_informacion_personal1,switcher_formulario,
                   switcher_salto_linea
                   ,switcher_padding_left)

        #informacion_personal2
        p.rect(x_informacion_personal2,y_informacion_personal2,ancho_informacion_personal2,alto_informacion_personal2)
        formulario(p,x_form_informacion_personal2,y_form_informacion_personal2,
                   lista_form_informacion_personal2,switcher_formulario,
                   switcher_salto_linea
                   ,switcher_padding_left)

        # titulo2_2
        titulo_texto(p, texto_titulo2_2, x_titulo2_2, y_titulo2_2,
                     tipo_letra_titulo2_2, tamanio_letra_titulo2_2,
                     padding_titulo_left_right_titulo2_2, padding_titulo_bottom_top_titulo2_2,
                     cantidad_pixeles_titulo2_2)

        # informacion_academica1
        p.rect(x_informacion_academica1, y_informacion_academica1, ancho_informacion_academica1,
               alto_informacion_academica1)
        formulario(p, x_form_informacion_academica1, y_form_informacion_academica1,
                   lista_form_informacion_academica1, switcher_formulario,
                   switcher_salto_linea
                   , switcher_padding_left)

        # informacion_academica2
        p.rect(x_informacion_academica2, y_informacion_academica2, ancho_informacion_academica2,
               alto_informacion_academica2)
        formulario(p, x_form_informacion_academica2, y_form_informacion_academica2,
                   lista_form_informacion_academica2, switcher_formulario,
                   switcher_salto_linea
                   , switcher_padding_left)

        #Mostrar pagina y guardar los cambios
        p.showPage()
        p.save()
        return response
