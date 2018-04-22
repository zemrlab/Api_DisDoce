from reportlab.lib import colors
from PIL import Image
from reportlab.lib.pagesizes import letter
import os
from reportlab.lib.units import cm, mm, inch, pica

def texto(canvas, texto, x, y, tipo_letra, tamaño_letra, color=colors.black):
    textobject = canvas.beginText(x, y)
    textobject.setFont(tipo_letra, tamaño_letra)
    textobject.setFillColor(color)
    textobject.textLine(text=texto)
    return textobject

def titulo_texto(p,
           text,
           x_titulo,
           y_titulo,
           tipo_letra_titulo,
           tamanio_letra_titulo,
           padding_titulo_left_right,
           padding_titulo_bottom_top,
           cantidad_pixeles_titulo):
    titulo = texto(p, text, x_titulo, y_titulo, tipo_letra_titulo, tamanio_letra_titulo)
    p.rect(x_titulo - padding_titulo_left_right,
           y_titulo - padding_titulo_bottom_top,
           cantidad_pixeles_titulo + padding_titulo_left_right * 2,
           tamanio_letra_titulo + padding_titulo_bottom_top*2)
    p.drawText(titulo)

def dibujar_imagen(canvas, foto, x, y, ancho_porcentaje=None, alto_porcentaje=None):
    #if foto :
    imagen=Image.open(foto)
    width, height=imagen.size
    width_total = None if ancho_porcentaje == None else width * (ancho_porcentaje / 100)
    height_total = None if alto_porcentaje == None else height * (alto_porcentaje / 100)
    #else:
     #   width_total,height_total=None,None
    canvas.drawImage(foto, x, y,width_total,height_total)

#Funciones del formulario
def titulo(p,dic):
    titulo=texto(p,dic['text'],dic['x'],dic['y'],dic['tipo_letra'],dic['tamanio_letra'])
    p.drawText(titulo)

def titulo_medio(p,dic):
    titulo=texto(p,dic['text'],dic['x_medio']-dic['cantidad_espacio_texto']/2,dic['y'],dic['tipo_letra'],dic['tamanio_letra'])
    p.drawText(titulo)

def campo(p,dic):
    titulo(p,dic)

def radio(p,dic):
    if(dic['Marcado'])[dic['text']]:
        marcado=1
    else:
        marcado=0
    p.circle(dic['x'],dic['y'],dic['radio'],1,marcado)
    palabra=texto(p,dic['text'],dic['x']+dic['radio']+dic['espacio_nombre'],dic['y']-dic['radio'],dic['tipo_letra'],dic['tamanio_letra'])
    p.drawText(palabra)

def linea(p,dic):
    p.line(dic['x_inicio_linea'],dic['y'],dic['x_inicio_linea']+dic['x_ancho_linea'],dic['y'])


"""

    'tipo_letra':Tipo de letra
    'tamanio_letra': El tamaño de la letra en pixeles
    'text': El texto que se escribira
    'radio':Radio del circulo del campo radio
    'espacio_nombre': El espacio que habra entre el circulo y el nombre del tipo de campo radio


    'titulo': {'text': 'Cursos',
               'tipo_letra': titulo_tipo_letra_form,
               'tamanio_letra': titulo_tamanio_letra_form},
    'campo': {'text': 'Curso2', 
               'tipo_letra': campo_tipo_letra_form,
               'tamanio_letra': campo_tamanio_letra_form}
    'campo_radio': {'text': 'Sexo',
                     'tipo_letra': campo_radio_tipo_letra_form,
                     'tamanio_letra':campo_radio_tamanio_letra_form}
    'radio': {'text': 'Femenino',
               'tipo_letra': radio_tipo_letra_form,
               'radio': radio_longitud_radio,
               'espacio_nombre': radio_espacio_nombre,
               'tamanio_letra': radio_tamanio_letra_form}
    {'linea': {'x_inicio_linea': x_marcos,
               'x_ancho_linea': ancho_marcos}},
    {'valor': {'text': docente_Grado.get('Especialidad', 'NO TIENE'),
               'tipo_letra': valor_tipo_letra_form,
               'tamanio_letra': valor_tamanio_letra_form}},

"""

def formulario(p,x,y,lista_form,switcher_formulario,switcher_salto_linea,switcher_padding_left):
    for valores in lista_form:
        for key,value in valores.items():
            espacio=switcher_salto_linea.get(key,0)
            aumentar=switcher_padding_left.get(key,0)
            value['x']=x+aumentar
            value['y']=y
            y=y-espacio

    for valor in lista_form:
        for key,value in valor.items():
            func=switcher_formulario.get(key,'No existe')
            if func!='No existe':
                func(p,value)
    return y

