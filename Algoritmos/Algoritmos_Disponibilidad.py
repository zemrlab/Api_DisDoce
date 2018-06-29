import json
from apps.disponibilidad.models import Disponibilidad
from django.db.models import Count,Sum

def Descifrar_disponibilidad(jsonDescifrar,row,col,hora_inicial,clave):
	valores=json.loads(jsonDescifrar)
	diccionario_intervalos={}
	L=valores[clave]
	row = row #7
	col = col #14
	M = [L[col*i : col*(i+1)] for i in range(row)]
	lista_intervalos=[]
	hora=hora_inicial #8
	dia=1
	for fila in M:
		lista=[]
		cantidad=len(fila)
		i=0
		while(i<cantidad):
			while(i<cantidad and fila[i]==True):
				lista.append(hora)
				i=i+1
				hora=hora+1
			if(len(lista)>0):
				lista_nueva=[lista[0],lista.pop()+1]
				lista_intervalos.append(lista_nueva)
				lista=[]
			i=i+1
			hora=hora+1
		diccionario_intervalos[dia]=lista_intervalos
		lista_intervalos=[]
		dia=dia+1
		hora=8

	return diccionario_intervalos

def devolver_disponibilidad(horarios_intervalos,hora_inicio,horas_del_dia): #jsoncifrar disccionario de dias
	dia=1
	i_horario=0
	horarios=[]
	while(dia<8):
		hora=hora_inicio #8
		horario_seleccionado=False
		for i in range(horas_del_dia): #14
			try:
				if(dia==int((horarios_intervalos[i_horario])['id_dia_id']) and hora==int((horarios_intervalos[i_horario])['hr_inicio'])):
						horario_seleccionado=True
				if(dia==int((horarios_intervalos[i_horario])['id_dia_id']) and hora==int((horarios_intervalos[i_horario])['hr_fin'])):
					horario_seleccionado=False
					i_horario=i_horario+1
			except IndexError:
				horario_seleccionado = False
			if(horario_seleccionado):
				horarios.append(True)
			else:
				horarios.append(False)
			hora=hora+1
		if(horario_seleccionado):
			i_horario=i_horario+1
		dia=dia+1
	return horarios

def docente_dias_disponibilidad(idDocente,idCiclo):
	dias_disponibles = Disponibilidad.objects.filter(id_docente=idDocente,id_ciclo=idCiclo).values('id_dia_id').annotate(dcount=Count('id_dia_id')).count()
	return dias_disponibles

def docente_horas_disponibilidad(idDocente,idCiclo):
	query_horas_disponibles = Disponibilidad.objects.filter(id_docente=idDocente,id_ciclo=idCiclo).values()
	horas_disponibles=0
	for x in query_horas_disponibles:
		horas_disponibles=horas_disponibles+int(x['tot_hrs'])

	return horas_disponibles