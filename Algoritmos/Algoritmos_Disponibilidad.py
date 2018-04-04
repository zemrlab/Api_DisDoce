import json

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
			while(i<cantidad and fila[i]=='1'):
				lista.append(hora)
				i=i+1
				hora=hora+1
			if(len(lista)>0):
				lista_nueva=[lista.pop(0),lista.pop()+1]
				lista_intervalos.append(lista_nueva)
				lista=[]
			i=i+1
			hora=hora+1
		diccionario_intervalos[dia]=lista_intervalos
		lista_intervalos=[]
		dia=dia+1
		hora=8

	return diccionario_intervalos