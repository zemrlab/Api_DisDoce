from django.db import  connection
from django.http.request import host_validation_re
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

        p1=[True,True,False,False,False,False]
        p2=[True,True,False,True,True,True]
        p3=[True,False,False,False,False,False]
        p4 = [True, False, True, False, False, False]
        p5 = [True, False, False, True, False, False]
        p6 = [True, False, False, False, True, False]
        p7 = [True, False, False, False, False, True]
        p8 = [False,True,True,False,False,False]
        p9 = [False, True, False, True, False, False]
        p10 = [False, True, False, False, True, False]
        p11 = [False, True, False, False, False, True]
        p12 = [False, False, True, True, False, False]
        p13 = [False, False, True, False, True, False]
        p14 = [False, False, True, False, False, True]
        p15 = [False, False, False, True, True, False]
        p16 = [False, False, False, True, False, True]
        p17 = [False, False, True, False, False, False]
        p18 = [True, False, False, True, True, False]
        p19 = [True, False, False, True, False, True]
        p20 = [True, False, False, True, True, True]
        p21 = [False, False, False, True, True, True]

        curso=curso.lower()
        docente=docente.lower()

        print(buscarValidar)
        resultado = []
        cursor = connection.cursor()
        if buscarValidar==p1:
            sql1="""select d.id,d.nombres,(d.apell_pat|| ' '|| d.apell_mat) as apellido,d.nro_document as dni,d.celular from preferencia p
                    join curso c on p.id_curso = c.id_curso
                    join docente d on p.id_docente = d.id
                    where lower(c.nom_curso) like '%"""+curso+"""%' and p.id_ciclo="""+semestre
            cursor.execute(sql1)
            docentes=dictfetchall(cursor)
            sqldisponibilidad="""select dis.id_disponibilidad as id,di.nom_dia as nombre,dis.hr_inicio as hinicio,dis.hr_fin as hfin from disponibilidad dis
                                    join docente d on dis.id_docente = d.id
                                    join dia di on dis.id_dia = di.id_dia
                                    where d.id=(%s)"""
            #docentes=[]
            #for prefe in preferencia:
             #   docentes.append(prefe.id_docente)
            for docente in docentes:
                cursor.execute(sqldisponibilidad,[docente['id']])
                del docente['id']
                disponibilidad=dictfetchall(cursor)
                if disponibilidad:
                    docente['disponibilidad']=disponibilidad
                    resultado.append(docente)
        if buscarValidar==p2:
            sql1 = """select d.nombres,(d.apell_pat|| ' '|| d.apell_mat) as apellido,d.nro_document as dni,d.celular from preferencia p
                        join curso c on p.id_curso = c.id_curso
                        join docente d on p.id_docente = d.id
                        join disponibilidad dis on d.id = dis.id_docente
                        where lower(c.nom_curso) like '%"""+curso+"""%' and p.id_ciclo="""+semestre+""" and NULLIF(dis.id_dia, '')::int="""+dia+"""
                              and NULLIF(dis.hr_inicio, '')::int>="""+hora_inicio+""" and NULLIF(dis.hr_fin, '')::int>="""+hora_fin+"""  
                              and NULLIF(dis.hr_fin, '')::int > NULLIF(dis.hr_inicio, '')::int"""
            cursor.execute(sql1)
            resultado=dictfetchall(cursor)
        if buscarValidar == p3:
            sql1="""select c.nom_curso as curso,pr.nom_programa as programa,c.numciclo as "nr ciclo",c.numcreditaje as creditos from preferencia p
                    join curso c on p.id_curso = c.id_curso
                    join programa pr on c.id_programa = pr.id_programa
                    join ciclo ci on p.id_ciclo = ci.id_ciclo
                    where ci.id_ciclo=(%s) group by pr.nom_programa,c.numciclo,c.numcreditaje,c.nom_curso"""
            cursor.execute(sql1,[semestre])
            resultado=dictfetchall(cursor)
        if buscarValidar == p4 :
            sql1 = """select c.nom_curso,pr.nom_programa,c.numciclo,c.numcreditaje,(d.nombres||' '||d.apell_pat||' '||d.apell_mat) as apellido
                        from preferencia p
                        join curso c on p.id_curso = c.id_curso
                        join programa pr on c.id_programa = pr.id_programa
                        join ciclo ci on p.id_ciclo = ci.id_ciclo
                        join docente d on p.id_docente = d.id
                        where ci.id_ciclo="""+semestre+""" and
                        lower (d.nombres||' '||d.apell_pat||' '||d.apell_mat) like '%"""+docente+"""%' group by pr.nom_programa,c.numciclo,c.numcreditaje,p.id_docente,apellido,c.nom_curso
                        """
            cursor.execute(sql1)
            resultado=dictfetchall(cursor)
        if buscarValidar == p5 :
            sql1 = """select d.id,(d.nombres||' '|| d.apell_pat|| ' '|| d.apell_mat) as docente, d.email as correo,d.direccion,d.celular,d.mayor_grado as "mayor grado"
                        from docente d
                        join disponibilidad dis on d.id = dis.id_docente group by d.mayor_grado,d.celular,d.direccion,d.email,d.id,docente"""
            cursor.execute(sql1)
            docentes=dictfetchall(cursor)
            sqldisponibilidad="""select dis.id_disponibilidad as id,di.nom_dia as nombre,dis.hr_inicio as hinicio,dis.hr_fin as hfin from disponibilidad dis
                                    join docente d on dis.id_docente = d.id
                                    join dia di on dis.id_dia = di.id_dia
                                    where NULLIF(dis.id_dia, '')::int=(%s) and dis.id_ciclo=(%s) and d.id=(%s)"""
            for docente in docentes:
                cursor.execute(sqldisponibilidad,[dia,semestre,docente['id']])
                del docente['id']
                disponibilidad=dictfetchall(cursor)
                if disponibilidad:
                    docente['disponibilidad']=disponibilidad
                    resultado.append(docente)
        if buscarValidar == p6 :
            sql1 = """select d.id,(d.nombres||' '|| d.apell_pat|| ' '|| d.apell_mat) as docente, d.email as correo,d.direccion,d.celular,d.mayor_grado as "mayor grado"
                        from docente d
                        join disponibilidad dis on d.id = dis.id_docente group by d.mayor_grado,d.celular,d.direccion,d.email,d.id,docente"""
            cursor.execute(sql1)
            docentes=dictfetchall(cursor)
            sqldisponibilidad="""select dis.id_disponibilidad as id,di.nom_dia as nombre,dis.hr_inicio as hinicio,dis.hr_fin as hfin from disponibilidad dis
                                    join docente d on dis.id_docente = d.id
                                    join dia di on dis.id_dia = di.id_dia
                                    where NULLIF(dis.hr_fin, '')::int>(%s)
                                     and NULLIF(dis.hr_inicio, '')::int<=(%s)
                                     and dis.id_ciclo=(%s) and d.id=(%s)"""
            for docente in docentes:
                cursor.execute(sqldisponibilidad,[hora_inicio,hora_inicio,semestre,docente['id']])
                del docente['id']
                disponibilidad=dictfetchall(cursor)
                if disponibilidad:
                    docente['disponibilidad']=disponibilidad
                    resultado.append(docente)
        if buscarValidar == p7 :
            sql1 = """select d.id,(d.nombres||' '|| d.apell_pat|| ' '|| d.apell_mat) as docente, d.email as correo,d.direccion,d.celular,d.mayor_grado as "mayor grado"
                        from docente d
                        join disponibilidad dis on d.id = dis.id_docente group by d.mayor_grado,d.celular,d.direccion,d.email,d.id,docente"""
            cursor.execute(sql1)
            docentes=dictfetchall(cursor)
            sqldisponibilidad="""select dis.id_disponibilidad as id,di.nom_dia as nombre,dis.hr_inicio as hinicio,dis.hr_fin as hfin from disponibilidad dis
                                    join docente d on dis.id_docente = d.id
                                    join dia di on dis.id_dia = di.id_dia
                                    where NULLIF(dis.hr_fin, '')::int>=(%s) 
                                    and NULLIF(dis.hr_inicio, '')::int<(%s)
                                    and dis.id_ciclo=(%s) and d.id=(%s)"""
            for docente in docentes:
                cursor.execute(sqldisponibilidad,[hora_fin,hora_fin,semestre,docente['id']])
                del docente['id']
                disponibilidad=dictfetchall(cursor)
                if disponibilidad:
                    docente['disponibilidad']=disponibilidad
                    resultado.append(docente)
        if buscarValidar == p8 :
            sql1="""select d.id,d.nombres,(d.apell_pat||' '||d.apell_mat) as apellido from preferencia p
                        join curso c on p.id_curso = c.id_curso
                        join docente d on p.id_docente = d.id
                        where lower(c.nom_curso) like '%"""+curso+"""%' and (lower(d.nombres||' '|| d.apell_pat||' '||d.apell_mat)  like '%"""+docente+"""%'"""
            cursor.execute(sql1)
            docentes = dictfetchall(cursor)
            sqldisponibilidad = """select dis.id_disponibilidad as id,di.nom_dia as nombre,dis.hr_inicio as hinicio,dis.hr_fin as hfin from disponibilidad dis
                                    join docente d on dis.id_docente = d.id
                                    join dia di on dis.id_dia = di.id_dia
                                    where dis.id_docente=(%s)"""
            for docente in docentes:
                cursor.execute(sqldisponibilidad,[docente['id']])
                del docente['id']
                disponibilidad=dictfetchall(cursor)
                if disponibilidad:
                    docente['disponibilidad']=disponibilidad
                    resultado.append(docente)
        if buscarValidar == p9:
            sql1="""select d.id,d.nombres,(d.apell_pat||' '||d.apell_mat) as apellido,d.nro_document as dni,d.celular from preferencia p
                        join curso c on p.id_curso = c.id_curso
                        join docente d on p.id_docente = d.id
                        where lower(c.nom_curso) like '%"""+curso+"""%'"""
            cursor.execute(sql1)
            docentes = dictfetchall(cursor)
            sqldisponibilidad = """select dis.id_disponibilidad as id,di.nom_dia as nombre,dis.hr_inicio as hinicio,dis.hr_fin as hfin from disponibilidad dis
                                    join docente d on dis.id_docente = d.id
                                    join dia di on dis.id_dia = di.id_dia
                                    where dis.id_docente=(%s) and  NULLIF(dis.id_dia, '')::int=(%s)"""
            for docente in docentes:
                cursor.execute(sqldisponibilidad, [docente['id'],dia])
                del docente['id']
                disponibilidad = dictfetchall(cursor)
                if disponibilidad:
                    docente['disponibilidad'] = disponibilidad
                    resultado.append(docente)
        if buscarValidar == p10:
            sql1 = """select d.id,d.nombres,(d.apell_pat||' '||d.apell_mat) as apellido,d.nro_document as dni,d.celular from preferencia p
                                   join curso c on p.id_curso = c.id_curso
                                   join docente d on p.id_docente = d.id
                                   where lower(c.nom_curso) like '%""" + curso + """%'"""
            cursor.execute(sql1)
            docentes = dictfetchall(cursor)
            sqldisponibilidad = """select dis.id_disponibilidad as id,di.nom_dia as nombre,dis.hr_inicio as hinicio,dis.hr_fin as hfin from disponibilidad dis
                                               join docente d on dis.id_docente = d.id
                                               join dia di on dis.id_dia = di.id_dia
                                               where dis.id_docente=(%s) 
                                               and  NULLIF(dis.hr_inicio, '')::int<=(%s)
                                               and NULLIF(dis.hr_fin, '')::int>(%s)"""
            for docente in docentes:
                cursor.execute(sqldisponibilidad, [docente['id'], hora_inicio,hora_inicio])
                del docente['id']
                disponibilidad = dictfetchall(cursor)
                if disponibilidad:
                    docente['disponibilidad'] = disponibilidad
                    resultado.append(docente)
        if buscarValidar == p11:
            sql1 = """select d.id,d.nombres,(d.apell_pat||' '||d.apell_mat) as apellido,d.nro_document as dni,d.celular from preferencia p
                                               join curso c on p.id_curso = c.id_curso
                                               join docente d on p.id_docente = d.id
                                               where lower(c.nom_curso) like '%""" + curso + """%'"""
            cursor.execute(sql1)
            docentes = dictfetchall(cursor)
            sqldisponibilidad = """select dis.id_disponibilidad as id,di.nom_dia as nombre,dis.hr_inicio as hinicio,dis.hr_fin as hfin from disponibilidad dis
                                                           join docente d on dis.id_docente = d.id
                                                           join dia di on dis.id_dia = di.id_dia
                                                           where dis.id_docente=(%s) 
                                                           and  NULLIF(dis.hr_fin, '')::int>=(%s)
                                                           and NULLIF(dis.hr_inicio, '')::int<(%s) """
            for docente in docentes:
                cursor.execute(sqldisponibilidad, [docente['id'], hora_fin,hora_fin])
                del docente['id']
                disponibilidad = dictfetchall(cursor)
                if disponibilidad:
                    docente['disponibilidad'] = disponibilidad
                    resultado.append(docente)
        if buscarValidar == p12:
            sql1="""select c.nom_ciclo as ciclo,dis.id_ciclo ,d.id,(d.nombres||' '|| d.apell_pat|| ' '|| d.apell_mat) as docente, d.email as correo,d.direccion,d.celular,d.mayor_grado as "mayor grado"
                        from docente d
                        join disponibilidad dis on d.id = dis.id_docente
                          join ciclo c on dis.id_ciclo = c.id_ciclo
                        where lower (d.nombres||' '||d.apell_pat||' '||d.apell_mat) like '%""" + curso + """%' 
                        group by d.mayor_grado,d.celular,d.direccion,d.email,d.id,dis.id_ciclo,c.nom_ciclo,docente
                        """
            cursor.execute(sql1)
            docentes = dictfetchall(cursor)
            sqldisponibilidad="""select dis.id_disponibilidad as id,di.nom_dia as nombre,dis.hr_inicio as hinicio,dis.hr_fin as hfin from disponibilidad dis
                                    join docente d on dis.id_docente = d.id
                                    join dia di on dis.id_dia = di.id_dia
                                    join ciclo c on dis.id_ciclo = c.id_ciclo
                                    where dis.id_docente=(%s) and dis.id_ciclo=(%s) and  NULLIF(dis.id_dia, '')::int=(%s)"""
            for docente in docentes:
                cursor.execute(sqldisponibilidad, [docente['id'],docente['id_ciclo'],dia])
                del docente['id']
                del docente['id_ciclo']
                disponibilidad = dictfetchall(cursor)
                if disponibilidad:
                    docente['disponibilidad'] = disponibilidad
                    resultado.append(docente)
        if buscarValidar == p13:
            sql1 = """select c.nom_ciclo as ciclo,dis.id_ciclo ,d.id,(d.nombres||' '|| d.apell_pat|| ' '|| d.apell_mat) as docente, d.email as correo,d.direccion,d.celular,d.mayor_grado as "mayor grado"
                                    from docente d
                                    join disponibilidad dis on d.id = dis.id_docente
                                      join ciclo c on dis.id_ciclo = c.id_ciclo
                                    where lower (d.nombres||' '||d.apell_pat||' '||d.apell_mat) like '%""" + curso + """%' 
                                    group by d.mayor_grado,d.celular,d.direccion,d.email,d.id,dis.id_ciclo,c.nom_ciclo,docente
                                    """
            cursor.execute(sql1)
            docentes = dictfetchall(cursor)
            print(docentes)
            sqldisponibilidad = """select dis.id_disponibilidad as id,di.nom_dia as nombre,dis.hr_inicio as hinicio,dis.hr_fin as hfin from disponibilidad dis
                                                join docente d on dis.id_docente = d.id
                                                join dia di on dis.id_dia = di.id_dia
                                                join ciclo c on dis.id_ciclo = c.id_ciclo
                                                where dis.id_docente=(%s)
                                                and dis.id_ciclo=(%s) 
                                                and  NULLIF(dis.hr_fin, '')::int>(%s)
                                                and NULLIF(dis.hr_inicio, '')::int<=(%s) """
            for docente in docentes:
                cursor.execute(sqldisponibilidad, [docente['id'], docente['id_ciclo'], hora_inicio,hora_inicio])
                del docente['id']
                del docente['id_ciclo']
                disponibilidad = dictfetchall(cursor)
                print(disponibilidad)
                if disponibilidad:
                    docente['disponibilidad'] = disponibilidad
                    resultado.append(docente)
        if buscarValidar == p14:
            sql1 = """select c.nom_ciclo as ciclo,dis.id_ciclo ,d.id,(d.nombres||' '|| d.apell_pat|| ' '|| d.apell_mat) as docente, d.email as correo,d.direccion,d.celular,d.mayor_grado as "mayor grado"
                                    from docente d
                                    join disponibilidad dis on d.id = dis.id_docente
                                      join ciclo c on dis.id_ciclo = c.id_ciclo
                                    where lower (d.nombres||' '||d.apell_pat||' '||d.apell_mat) like '%""" + curso + """%' 
                                    group by d.mayor_grado,d.celular,d.direccion,d.email,d.id,dis.id_ciclo,c.nom_ciclo,docente
                                    """
            cursor.execute(sql1)
            docentes = dictfetchall(cursor)
            print(docentes)
            sqldisponibilidad = """select dis.id_disponibilidad as id,di.nom_dia as nombre,dis.hr_inicio as hinicio,dis.hr_fin as hfin from disponibilidad dis
                                                join docente d on dis.id_docente = d.id
                                                join dia di on dis.id_dia = di.id_dia
                                                join ciclo c on dis.id_ciclo = c.id_ciclo
                                                where dis.id_docente=(%s)
                                                and dis.id_ciclo=(%s) 
                                               and  NULLIF(dis.hr_fin, '')::int>=(%s)
                                                and NULLIF(dis.hr_inicio, '')::int<(%s)"""
            for docente in docentes:
                cursor.execute(sqldisponibilidad, [docente['id'], docente['id_ciclo'], hora_fin,hora_fin])
                del docente['id']
                del docente['id_ciclo']
                disponibilidad = dictfetchall(cursor)
                print(disponibilidad)
                if disponibilidad:
                    docente['disponibilidad'] = disponibilidad
                    resultado.append(docente)
        if buscarValidar == p15:
            sql1 = """select c.nom_ciclo as ciclo,dis.id_ciclo ,d.id,(d.nombres||' '|| d.apell_pat|| ' '|| d.apell_mat) as docente, d.email as correo,d.direccion,d.celular,d.mayor_grado as "mayor grado"
                                           from docente d
                                           join disponibilidad dis on d.id = dis.id_docente
                                             join ciclo c on dis.id_ciclo = c.id_ciclo
                                           group by d.mayor_grado,d.celular,d.direccion,d.email,d.id,dis.id_ciclo,c.nom_ciclo,docente
                                           """
            cursor.execute(sql1)
            docentes = dictfetchall(cursor)
            print(docentes)
            sqldisponibilidad = """select dis.id_disponibilidad as id,di.nom_dia as nombre,dis.hr_inicio as hinicio,dis.hr_fin as hfin from disponibilidad dis
                                                       join docente d on dis.id_docente = d.id
                                                       join dia di on dis.id_dia = di.id_dia
                                                       join ciclo c on dis.id_ciclo = c.id_ciclo
                                                       where dis.id_docente=(%s)
                                                       and dis.id_ciclo=(%s) 
                                                       and NULLIF(dis.id_dia, '')::int=(%s)
                                                       and  NULLIF(dis.hr_fin, '')::int>(%s)
                                                       and NULLIF(dis.hr_inicio, '')::int<=(%s) """
            for docente in docentes:
                cursor.execute(sqldisponibilidad, [docente['id'], docente['id_ciclo'], dia,hora_inicio, hora_inicio])
                del docente['id']
                del docente['id_ciclo']
                disponibilidad = dictfetchall(cursor)
                print(disponibilidad)
                if disponibilidad:
                    docente['disponibilidad'] = disponibilidad
                    resultado.append(docente)
        if buscarValidar == p16:
            sql1 = """select c.nom_ciclo as ciclo,dis.id_ciclo ,d.id,(d.nombres||' '|| d.apell_pat|| ' '|| d.apell_mat) as docente, d.email as correo,d.direccion,d.celular,d.mayor_grado as "mayor grado"
                                    from docente d
                                    join disponibilidad dis on d.id = dis.id_docente
                                      join ciclo c on dis.id_ciclo = c.id_ciclo
                                    group by d.mayor_grado,d.celular,d.direccion,d.email,d.id,dis.id_ciclo,c.nom_ciclo,docente
                                    """
            cursor.execute(sql1)
            docentes = dictfetchall(cursor)
            print(docentes)
            sqldisponibilidad = """select dis.id_disponibilidad as id,di.nom_dia as nombre,dis.hr_inicio as hinicio,dis.hr_fin as hfin from disponibilidad dis
                                                join docente d on dis.id_docente = d.id
                                                join dia di on dis.id_dia = di.id_dia
                                                join ciclo c on dis.id_ciclo = c.id_ciclo
                                                where dis.id_docente=(%s)
                                                and dis.id_ciclo=(%s) 
                                                and NULLIF(dis.id_dia, '')::int=(%s)
                                               and  NULLIF(dis.hr_fin, '')::int>=(%s)
                                                and NULLIF(dis.hr_inicio, '')::int<(%s)"""
            for docente in docentes:
                cursor.execute(sqldisponibilidad, [docente['id'], docente['id_ciclo'],dia, hora_fin,hora_fin])
                del docente['id']
                del docente['id_ciclo']
                disponibilidad = dictfetchall(cursor)
                print(disponibilidad)
                if disponibilidad:
                    docente['disponibilidad'] = disponibilidad
                    resultado.append(docente)
        if buscarValidar == p17:
            print("docente filter")
            sql1 = """select c.nom_ciclo as ciclo,(d.nombres||' '|| d.apell_pat|| ' '|| d.apell_mat) as docente, d.email as correo,d.direccion,d.celular,d.mayor_grado as "mayor grado"
                                                from docente d
                                                join disponibilidad dis on d.id = dis.id_docente
                                                  join ciclo c on dis.id_ciclo = c.id_ciclo
                                                  where lower (d.nombres||' '||d.apell_pat||' '||d.apell_mat) like '%""" + docente + """%'
                                                group by d.mayor_grado,d.celular,d.direccion,d.email,d.id,dis.id_ciclo,c.nom_ciclo,docente  """
            cursor.execute(sql1)
            resultado = dictfetchall(cursor)
        if buscarValidar == p18:
            sql1 = """select d.id,(d.nombres||' '|| d.apell_pat|| ' '|| d.apell_mat) as docente, d.email as correo,d.direccion,d.celular,d.mayor_grado as "mayor grado"
                                    from docente d
                                    join disponibilidad dis on d.id = dis.id_docente group by d.mayor_grado,d.celular,d.direccion,d.email,d.id,docente"""
            cursor.execute(sql1)
            docentes = dictfetchall(cursor)
            sqldisponibilidad = """select dis.id_disponibilidad as id,di.nom_dia as nombre,dis.hr_inicio as hinicio,dis.hr_fin as hfin from disponibilidad dis
                                    join docente d on dis.id_docente = d.id
                                    join dia di on dis.id_dia = di.id_dia
                                    where   NULLIF(dis.id_dia, '')::int=(%s)
                                     and NULLIF(dis.hr_fin, '')::int>(%s)
                                     and NULLIF(dis.hr_inicio, '')::int<=(%s)
                                     and dis.id_ciclo=(%s) and d.id=(%s)"""
            for docente in docentes:
                cursor.execute(sqldisponibilidad, [dia,hora_inicio,hora_inicio,semestre, docente['id']])
                del docente['id']
                disponibilidad = dictfetchall(cursor)
                if disponibilidad:
                    docente['disponibilidad'] = disponibilidad
                    resultado.append(docente)
        if buscarValidar == p18:
            sql1 = """select d.id,(d.nombres||' '|| d.apell_pat|| ' '|| d.apell_mat) as docente, d.email as correo,d.direccion,d.celular,d.mayor_grado as "mayor grado"
                                    from docente d
                                    join disponibilidad dis on d.id = dis.id_docente group by d.mayor_grado,d.celular,d.direccion,d.email,d.id,docente"""
            cursor.execute(sql1)
            docentes = dictfetchall(cursor)
            sqldisponibilidad = """select dis.id_disponibilidad as id,di.nom_dia as nombre,dis.hr_inicio as hinicio,dis.hr_fin as hfin from disponibilidad dis
                                    join docente d on dis.id_docente = d.id
                                    join dia di on dis.id_dia = di.id_dia
                                    where   NULLIF(dis.id_dia, '')::int=(%s)
                                     and NULLIF(dis.hr_fin, '')::int>=(%s)
                                     and NULLIF(dis.hr_inicio, '')::int<(%s)
                                     and dis.id_ciclo=(%s) and d.id=(%s)"""
            for docente in docentes:
                cursor.execute(sqldisponibilidad, [dia,hora_inicio,hora_inicio,semestre, docente['id']])
                del docente['id']
                disponibilidad = dictfetchall(cursor)
                if disponibilidad:
                    docente['disponibilidad'] = disponibilidad
                    resultado.append(docente)
        if buscarValidar == p19:
            sql1 = """select d.id,(d.nombres||' '|| d.apell_pat|| ' '|| d.apell_mat) as docente, d.email as correo,d.direccion,d.celular,d.mayor_grado as "mayor grado"
                                    from docente d
                                    join disponibilidad dis on d.id = dis.id_docente group by d.mayor_grado,d.celular,d.direccion,d.email,d.id,docente"""
            cursor.execute(sql1)
            docentes = dictfetchall(cursor)
            sqldisponibilidad = """select dis.id_disponibilidad as id,di.nom_dia as nombre,dis.hr_inicio as hinicio,dis.hr_fin as hfin from disponibilidad dis
                                    join docente d on dis.id_docente = d.id
                                    join dia di on dis.id_dia = di.id_dia
                                    where   NULLIF(dis.id_dia, '')::int=(%s)
                                     and NULLIF(dis.hr_fin, '')::int>=(%s)
                                     and NULLIF(dis.hr_inicio, '')::int<(%s)
                                     and dis.id_ciclo=(%s) and d.id=(%s)"""
            for docente in docentes:
                cursor.execute(sqldisponibilidad, [dia,hora_fin,hora_fin,semestre, docente['id']])
                del docente['id']
                disponibilidad = dictfetchall(cursor)
                if disponibilidad:
                    docente['disponibilidad'] = disponibilidad
                    resultado.append(docente)
        if buscarValidar == p20:
            sql1 = """select d.id,(d.nombres||' '|| d.apell_pat|| ' '|| d.apell_mat) as docente, d.email as correo,d.direccion,d.celular,d.mayor_grado as "mayor grado"
                                           from docente d
                                           join disponibilidad dis on d.id = dis.id_docente group by d.mayor_grado,d.celular,d.direccion,d.email,d.id,docente"""
            cursor.execute(sql1)
            docentes = dictfetchall(cursor)
            sqldisponibilidad = """select dis.id_disponibilidad as id,di.nom_dia as nombre,dis.hr_inicio as hinicio,dis.hr_fin as hfin from disponibilidad dis
                                           join docente d on dis.id_docente = d.id
                                           join dia di on dis.id_dia = di.id_dia
                                           where   NULLIF(dis.id_dia, '')::int=(%s)
                                            and NULLIF(dis.hr_fin, '')::int>=(%s)
                                            and NULLIF(dis.hr_inicio, '')::int<=(%s)
                                            and (%s)<(%s)
                                            and dis.id_ciclo=(%s) and d.id=(%s)"""
            for docente in docentes:
                cursor.execute(sqldisponibilidad, [dia, hora_fin, hora_inicio,hora_fin,hora_inicio ,semestre, docente['id']])
                del docente['id']
                disponibilidad = dictfetchall(cursor)
                if disponibilidad:
                    docente['disponibilidad'] = disponibilidad
                    resultado.append(docente)
        if buscarValidar==p21:
            sql1 = """select c.nom_ciclo as ciclo,dis.id_ciclo ,d.id,(d.nombres||' '|| d.apell_pat|| ' '|| d.apell_mat) as docente, d.email as correo,d.direccion,d.celular,d.mayor_grado as "mayor grado"
                                                from docente d
                                                join disponibilidad dis on d.id = dis.id_docente
                                                  join ciclo c on dis.id_ciclo = c.id_ciclo
                                                group by d.mayor_grado,d.celular,d.direccion,d.email,d.id,dis.id_ciclo,c.nom_ciclo,docente
                                                """
            cursor.execute(sql1)
            docentes = dictfetchall(cursor)
            print(docentes)
            sqldisponibilidad = """select dis.id_disponibilidad as id,di.nom_dia as nombre,dis.hr_inicio as hinicio,dis.hr_fin as hfin from disponibilidad dis
                                                            join docente d on dis.id_docente = d.id
                                                            join dia di on dis.id_dia = di.id_dia
                                                            join ciclo c on dis.id_ciclo = c.id_ciclo
                                                            where dis.id_docente=(%s)
                                                            and dis.id_ciclo=(%s) 
                                                            and NULLIF(dis.id_dia, '')::int=(%s)
                                                            and NULLIF(dis.hr_fin, '')::int>=(%s)
                                                            and NULLIF(dis.hr_inicio, '')::int<=(%s)
                                                            and (%s)<(%s)"""
            for docente in docentes:
                cursor.execute(sqldisponibilidad, [docente['id'], docente['id_ciclo'], dia, hora_fin, hora_inicio,hora_inicio,hora_fin])
                del docente['id']
                del docente['id_ciclo']
                disponibilidad = dictfetchall(cursor)
                print(disponibilidad)
                if disponibilidad:
                    docente['disponibilidad'] = disponibilidad
                    resultado.append(docente)
        cursor.close()
        return Response(resultado)
        #preferencia=Preferencia.objects.filter(id_ciclo__nom_ciclo__contains=semestre,id_curso__nom_curso__contains=curso)

        #preferenciaSerializado=self.serializer_preferencia(preferencia,many=True)

        #for prefe in preferencia:
        #   print(prefe.id_curso.nom_curso)

        #return Response(preferenciaSerializado.data)