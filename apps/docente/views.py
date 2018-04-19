
import json
from django.shortcuts import render
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from apps.docente.serializers import DocenteSerializer
from rest_framework.response import Response
from apps.docente.models import Docente,DatosAcademicos,TipoGrado
from apps.disponibilidad.models import Disponibilidad
from apps.curso.models import Preferencia,Curso
from django.http import  HttpResponse
from reportlab.pdfgen import canvas
from Algoritmos.libreria_pdf import *
from Algoritmos.Algoritmos_Disponibilidad import devolver_disponibilidad,docente_dias_disponibilidad,docente_horas_disponibilidad
from reportlab.lib.pagesizes import letter,landscape
from PIL import Image
# Create your views here.

class DocenteList(APIView):
    serializer = DocenteSerializer
    def get(self, request, id):
        try:
            lista = Docente.objects.get(id=id)
        except Docente.DoesNotExist:
            return Response('NO EXISTE DOCENTE',status=status.HTTP_400_BAD_REQUEST)
        listajson=(self.serializer(lista)).data
        listaDatos_Academicos=DatosAcademicos.objects.filter(id_docente=id)
        for datos_academicos in listaDatos_Academicos:
            listajson[datos_academicos.id_tip_grado.nom_tip_grado]=datos_academicos.mencion_grado
        return Response(listajson)

class PDFView(APIView):
    def get(self,request,id):
        response = HttpResponse(content_type='application/pdf')
        nombre_pdf='docente'+id
        response['Content-Disposition'] = 'filename="'+nombre_pdf+'.pdf"'

        try:
            informacion_docente=Docente.objects.get(id=id)
        except Docente.DoesNotExist:
            return Response('NO EXISTE DOCENTE',status=status.HTTP_400_BAD_REQUEST)

        #variables docente
        docente_nom=informacion_docente.nombres
        apellidos=informacion_docente.apell_pat+" "+informacion_docente.apell_mat
        docente_ape = apellidos
        docente_codigo = informacion_docente.codigo
        docente_tipo_documento=informacion_docente.tipo_document
        docente_nro_documento= informacion_docente.nro_document
        docente_email = informacion_docente.email
        docente_celular=informacion_docente.celular
        docente_genero= informacion_docente.genero
        docente_pagina_web= informacion_docente.pag_web
        docente_fecha_nac= informacion_docente.fecha_nac
        docente_pais= informacion_docente.pais
        docente_direccion= informacion_docente.direccion
        docente_sunedu_le= informacion_docente.sunedu_ley
        docente_categoria= informacion_docente.categoria
        docente_regimen_dedicacion= informacion_docente.regimen_dedicacion
        docente_cv = informacion_docente.cv

        total_datos_academicos = DatosAcademicos.objects.filter(id_docente=id).values()
        docente_Grado={}
        for datos_academicos in total_datos_academicos:
            Nombre_Tipo_Grado=(TipoGrado.objects.get(id_tip_grado=datos_academicos['id_tip_grado_id'])).nom_tip_grado
            Nombre_Mencion_Grado=datos_academicos['mencion_grado']
            docente_Grado[Nombre_Tipo_Grado]=Nombre_Mencion_Grado

        #variabls de ayuda para pintar docente
        fin_direccion=25
        direccion_caracter_siguiente_linea=''

        # variabls de ayuda para pintar programa de los cursos
        fin_programa_curso=55
        programa_curso_caracter_siguiente_linea=''

        # variabls de ayuda para pintar programa de los cursos
        fin_marco_curso = 53
        marco_curso_caracter_siguiente_linea = '-'

        if len(docente_direccion)>=fin_direccion :
            if docente_direccion[fin_direccion]!=' ':
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
            'linea':linea,
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
            'linea' : 20,
        }

        switcher_padding_left = {
            'campo': 15,
            'radio': 40,
            'campo_radio': 15,
            'valor': 25,
        }

        #variables:titulo1
        tamanio_letra_titulo1=19
        texto_titulo1='INFORMACION DEL DOCENTE' #ANTES DISPONIBILIDAD DEL DOCENTE
        tipo_letra_titulo1='Times-Bold'
        cantidad_pixeles_titulo1=295
        padding_titulo_bottom_top_titulo1=15
        padding_titulo_left_right_titulo1=130
        x_titulo1=ancho_pagina/2-cantidad_pixeles_titulo1/2
        y_titulo1=800


        #variables:titulo1_1
        tamanio_letra_titulo1_1=17
        texto_titulo1_1 ='Informacion personal'
        tipo_letra_titulo1_1='Times-Bold'
        cantidad_pixeles_titulo1_1=155
        padding_titulo_bottom_top_titulo1_1=10
        padding_titulo_left_right_titulo1_1=180
        x_titulo1_1 = ancho_pagina/2-cantidad_pixeles_titulo1_1/2
        y_titulo1_1 = 490

        #variables:titulo1_2
        tamanio_letra_titulo1_2=17
        texto_titulo1_2 = 'Informacion academica'
        tipo_letra_titulo1_2='Times-Bold'
        cantidad_pixeles_titulo1_2=150
        padding_titulo_bottom_top_titulo1_2=10
        padding_titulo_left_right_titulo1_2=185
        x_titulo1_2 = ancho_pagina/2-cantidad_pixeles_titulo1_2/2
        y_titulo1_2 = 198

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
            {'campo': {'text': docente_tipo_documento,
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'valor': {'text': docente_nro_documento,
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
            {'valor': {'text': docente_Grado.get('Titulo','NO TIENE'),
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
        #titulo1
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

        #titulo1_1
        titulo_texto(p,texto_titulo1_1,x_titulo1_1,y_titulo1_1,
               tipo_letra_titulo1_1,tamanio_letra_titulo1_1,
               padding_titulo_left_right_titulo1_1,padding_titulo_bottom_top_titulo1_1,cantidad_pixeles_titulo1_1)

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

        # titulo1_2
        titulo_texto(p, texto_titulo1_2, x_titulo1_2, y_titulo1_2,
                     tipo_letra_titulo1_2, tamanio_letra_titulo1_2,
                     padding_titulo_left_right_titulo1_2, padding_titulo_bottom_top_titulo1_2,
                     cantidad_pixeles_titulo1_2)

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

        p.showPage()

        #                   OTRA PAGINA

        #variables:titulo2
        tamanio_letra_titulo2=tamanio_letra_titulo1
        texto_titulo2 = 'PREFERENCIA DE CURSOS'
        tipo_letra_titulo2= tipo_letra_titulo1
        cantidad_pixeles_titulo2=270
        padding_titulo_bottom_top_titulo2=padding_titulo_bottom_top_titulo1
        padding_titulo_left_right_titulo2=padding_titulo_left_right_titulo1
        x_titulo2 = ancho_pagina/2-cantidad_pixeles_titulo2/2
        y_titulo2 = y_titulo1

        #variables:Marco
        margin_marco_left_right=41
        margin_marco_bottom_top=30
        x_marco=margin_marco_left_right
        y_marco=margin_marco_bottom_top
        ancho_marco=ancho_pagina-2*margin_marco_left_right
        alto_marco=alto_pagina-2*margin_marco_bottom_top


        #variables:Marcos
        margin_marcos_left_right=40
        margin_marcos_bottom=550
        margin_marcos_top=20
        separacion_marcos=40
        x_marcos=x_marco + margin_marcos_left_right
        y_marcos=y_marco + margin_marcos_bottom
        alto_marcos=alto_marco-margin_marcos_top-margin_marcos_bottom #margin_bottom es para que no se mueva el alto del marco
        ancho_marcos=ancho_marco - 2 * margin_marcos_left_right

        #variables:marcos form
        padding_marcos_form_left= 20
        x_form_marcos=x_marcos+padding_marcos_form_left
        y_form_marcos=y_marcos+alto_marcos*(7/8)

        # titulo2
        titulo_texto(p, texto_titulo2, x_titulo2, y_titulo2,
                     tipo_letra_titulo2, tamanio_letra_titulo2,
                     padding_titulo_left_right_titulo2, padding_titulo_bottom_top_titulo2,
                     cantidad_pixeles_titulo2)

        #Marco
        p.rect(x_marco,y_marco,ancho_marco,alto_marco)


        #Algoritmos

        #Devovler cursos x programa
        preferencias = Preferencia.objects.filter(id_docente=id).values()
        cursos=[]
        programas_cursos={}
        for preferencia in preferencias:
            curso=Curso.objects.get(id_curso=preferencia['id_curso_id'])
            """try:
                informacion_docente = Docente.objects.get(id_docente=id)
            except Docente.DoesNotExist:
                return HttpResponse('NO EXISTE DOCENTE') ver despues"""
            if curso.id_programa.nom_programa not in programas_cursos.keys() :
                programas_cursos[curso.id_programa.nom_programa]=[]
            programas_cursos[curso.id_programa.nom_programa].append(curso.nom_curso)

        #FORM_DINAMICO

        programas_cursos_keys=programas_cursos.keys()
        ultimovalor=(list(programas_cursos_keys)).pop()

        for key, value in programas_cursos.items():
            # Marcos
            #p.rect(x_marcos,
            #       y_marcos,
            #       ancho_marcos,
            #       alto_marcos)

            if len(key) >= fin_programa_curso:
                if key[fin_programa_curso] != ' ':
                    programa_curso_caracter_siguiente_linea = '-'

            lista_form_marcos_form = [
                {'campo': {'text': 'Nombre de programa',
                            'tipo_letra': campo_tipo_letra_form,
                            'tamanio_letra': campo_tamanio_letra_form}},
                {'valor': {'text':  key[:fin_programa_curso]+programa_curso_caracter_siguiente_linea,
                           'tipo_letra': valor_tipo_letra_form,
                           'tamanio_letra': valor_tamanio_letra_form}},
                {'valor': {'text': key[fin_programa_curso:],
                           'tipo_letra': valor_tipo_letra_form,
                           'tamanio_letra': valor_tamanio_letra_form}},
                {'linea': {'x_inicio_linea': x_marcos,
                           'x_ancho_linea': ancho_marcos}},
                {'campo': {'text': 'Nombre(s) de( los) curso(s)',
                           'tipo_letra': campo_tipo_letra_form,
                           'tamanio_letra': campo_tamanio_letra_form}},
            ]
            y = formulario(p, x_form_marcos, y_form_marcos,
                           lista_form_marcos_form, switcher_formulario,
                           switcher_salto_linea
                           , switcher_padding_left)
            y_form_inicial=y
            y_form_marcos = y
            x_form_inicial=x_form_marcos
            for curso in value:
                curso="-"+curso
                lista_second_form_marcos_form = []
                faltante=len(curso)
                while(faltante>fin_marco_curso):
                    curso_text=curso[:fin_marco_curso]
                    curso=curso[fin_marco_curso:]
                    faltante=len(curso)
                    lista_second_form_marcos_form.append(
                        {'valor': {'text': curso_text+marco_curso_caracter_siguiente_linea,
                                   'tipo_letra': valor_tipo_letra_form,
                                   'tamanio_letra': valor_tamanio_letra_form}},
                    )
                lista_second_form_marcos_form.append(
                    {'valor': {'text': curso,
                               'tipo_letra': valor_tipo_letra_form,
                               'tamanio_letra': valor_tamanio_letra_form}},
                )
                y = formulario(p, x_form_marcos, y_form_marcos,
                               lista_second_form_marcos_form, switcher_formulario,
                               switcher_salto_linea
                               , switcher_padding_left)
                y_form_marcos=y
                if y_form_marcos < y_marcos + alto_marcos * (1 / 8):
                    y_marcos=y_marcos-switcher_salto_linea['valor']
                    alto_marcos=alto_marcos+switcher_salto_linea['valor']

            p.rect(x_marcos,
                   y_marcos,
                   ancho_marcos,
                   alto_marcos)

            x_form_marcos=x_form_inicial
            y_form_marcos=y_marcos-separacion_marcos-alto_marcos*(1/8)
            y_marcos=y_marcos-alto_marcos-separacion_marcos
            if y_marcos < 0 and key!=ultimovalor:
                p.showPage()
                #OTRA PAGINA

                # variables:Marcos
                margin_marcos_left_right = 40
                margin_marcos_bottom = 550
                margin_marcos_top = 20
                separacion_marcos = 40
                x_marcos = x_marco + margin_marcos_left_right
                y_marcos = y_marco + margin_marcos_bottom
                alto_marcos = alto_marco - margin_marcos_top - margin_marcos_bottom  # margin_bottom es para que no se mueva el alto del marco
                ancho_marcos = ancho_marco - 2 * margin_marcos_left_right

                # variables:marcos form
                padding_marcos_form_left = 20
                x_form_marcos = x_marcos + padding_marcos_form_left
                y_form_marcos = y_marcos + alto_marcos * (7 / 8)

                # titulo2
                titulo_texto(p, texto_titulo2, x_titulo2, y_titulo2,
                             tipo_letra_titulo2, tamanio_letra_titulo2,
                             padding_titulo_left_right_titulo2, padding_titulo_bottom_top_titulo2,
                             cantidad_pixeles_titulo2)
                #titulo
                p.rect(x_marco, y_marco, ancho_marco, alto_marco)

        p.showPage()


        p.setPageSize(landscape(letter))
        #               OTRA PAGINA

        tamanio_letra_titulo3 = 19
        texto_titulo3 = 'DISPONIBILIDAD DE HORARIO'  # ANTES DISPONIBILIDAD DEL DOCENTE
        tipo_letra_titulo3 = 'Times-Bold'
        cantidad_pixeles_titulo3 = 295
        padding_titulo_bottom_top_titulo3 = 15
        padding_titulo_left_right_titulo3 = 130
        x_titulo3 = alto_pagina / 2 - cantidad_pixeles_titulo3 / 2
        y_titulo3 = ancho_pagina-60

        # titulo3
        titulo_texto(p, texto_titulo3, x_titulo3, y_titulo3,
                     tipo_letra_titulo3, tamanio_letra_titulo3,
                     padding_titulo_left_right_titulo3, padding_titulo_bottom_top_titulo3, cantidad_pixeles_titulo3)


        #Algoritmo Disponibilidad
        horarios_intervalos = Disponibilidad.objects.filter(id_docente=id).order_by('id_disponibilidad').values()
        array=[]
        if horarios_intervalos:
            array = devolver_disponibilidad(horarios_intervalos, 8, 14)



        #variables:Fechas
        x_dias=100
        y_dias=420
        x_dias_intervalo=60
        dias_tipo_letra = 'Times-Roman'
        dias_tamanio_letra = 12
        dias=['Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo']

        i=0


        #variables:horas
        x_horas=50
        y_horas=400
        y_horas_intervalo=20
        horas_tipo_letra = 'Times-Roman'
        horas_tamanio_letra = 12

        #Mostrar dias
        for x in range(x_dias,x_dias+x_dias_intervalo*len(dias),x_dias_intervalo):
            dia=texto(p,dias[i],x,y_dias,dias_tipo_letra,dias_tamanio_letra)
            p.drawText(dia)
            i=i+1

        y_inicial_horas=y_horas
        #Mostrar horas
        for x in range(8,22):
            hora=str(x)+"-"+str(x+1)
            dia = texto(p, hora, x_horas, y_horas, horas_tipo_letra, horas_tamanio_letra)
            y_horas=y_horas-y_horas_intervalo
            p.drawText(dia)

        Disponibilidad_marcado=True
        if not array:
            Disponibilidad_marcado=False
        for dia in range(len(dias)):
            for horas in range(14):
                if Disponibilidad_marcado and array[horas+14*(dia)] :
                    marcado = 1
                else:
                    marcado = 0
                p.rect(x_dias+dia*(x_dias_intervalo)+10,y_inicial_horas-horas*(y_horas_intervalo),10,10,1,marcado)

        # variables:marco_horario
        x_marco_horario=x_horas-20
        y_marco_horario=y_horas
        alto_marco_horario=y_dias-y_marco_horario+30
        ancho_marco_horario=x_dias+len(dias)*x_dias_intervalo-30

        #Marco_Horario
        p.rect(x_marco_horario, y_marco_horario, ancho_marco_horario, alto_marco_horario)

        total_dias_disponible=docente_dias_disponibilidad(id)
        total_horas_disponible=docente_horas_disponibilidad(id)

    # variables:resumen
        ancho_resumen = 220
        alto_resumen = 150
        x_resumen = 550
        y_resumen = 300
        x_form_resumen = x_resumen + ancho_resumen * (1 / 8)
        y_form_resumen = y_resumen + alto_resumen * (7 / 8)-10


        lista_form_resumen = [
            {'campo': {'text': 'RESUMEN',
                        'tipo_letra': titulo_tipo_letra_form,
                        'tamanio_letra': 13}},
            {'campo': {'text': 'Toral de horas disponibles :',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'valor': {'text': str(total_horas_disponible),
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'campo': {'text': 'Total de dias disponibles :',
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
            {'valor': {'text': str(total_dias_disponible),
                       'tipo_letra': campo_tipo_letra_form,
                       'tamanio_letra': campo_tamanio_letra_form}},
        ]

        # resumen
        p.rect(x_resumen, y_resumen, ancho_resumen, alto_resumen)
        formulario(p, x_form_resumen, y_form_resumen, lista_form_resumen, switcher_formulario, switcher_salto_linea, switcher_padding_left)


        #Mostrar pagina y guardar los cambios
        p.showPage()
        p.save()
        return response
