import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage, TextArea
import numpy as np
import copy
from time import sleep
from IPython.display import clear_output
import chess
import re

class OchoReinas:
	'''
	Problema de las ocho reinas, el cual consiste en poner ocho reinas en un tablero de ajerdez de tal manera que ninguna pueda atacar a las demás.
	Estado inicial: Tablero vacío.
	Posibles acciones: Dado un estado con k reinas (k<8), las acciones aplicables son poner una reina en una de las casillas vacías que no es atacada por ninguna de las otras reinas.
	Función de transiciones: Toma un tablero con k reinas (k<8) y devuelve un tablero con k+1 reinas.
	Prueba de satisfacción del objetivo: Verificar la condición de si un tablero dado contiene ocho reinas en el cual niguna puede atacar a otra.
	Función de costo: Cantidad de acciones realizadas (siempre devolverá el valor de 8 en cualquier solución).
	'''
	def __init__(self):
		self.estado_inicial = np.matrix([[0]*8]*8)

	def pintar_estado(self, estado):
		# Dibuja el tablero correspondiente al estado
		# Input: estado, que es una 8-lista de 8-listas
		fig, axes = plt.subplots()

		# Dibujo el tablero
		step = 1./8
		offset = 0.001
		tangulos = []

		# Borde del tablero
		tangulos.append(patches.Rectangle((0,0),0.998,0.998,\
		facecolor='cornsilk',\
		edgecolor='black',\
		linewidth=2))

		# Creo los cuadrados oscuros en el tablero
		for i in range(4):
			for j in range(4):
				tangulos.append(
				patches.Rectangle(
				(2 * i * step, 2 * j * step), \
				step - offset, \
				step,\
				facecolor='lightslategrey')\
				)
				tangulos.append(
				patches.Rectangle(
				(step + 2 * i * step, (2 * j + 1) * step), \
				step - offset, \
				step,\
				facecolor='lightslategrey')\
				)

		# Creo las líneas del tablero
		for j in range(8):
			locacion = j * step
			# Crea linea horizontal en el rectangulo
			tangulos.append(patches.Rectangle(*[(0, locacion), 1, 0.008],\
			facecolor='black'))
			# Crea linea vertical en el rectangulo
			tangulos.append(patches.Rectangle(*[(locacion, 0), 0.008, 1],\
			facecolor='black'))

		for t in tangulos:
			axes.add_patch(t)

		# Cargando imagen de la reina
		arr_img = plt.imread("./imagenes/8Reinas/reina.png", format='png')
		imagebox = OffsetImage(arr_img, zoom=0.048)
		imagebox.image.axes = axes

		offsetX = 0.065
		offsetY = 0.065
		for i in range(8):
			for j in range(8):
				if estado[j, i] == 1:
					# print("Reina en (" + str(i) + ", " + str(j) + ")")
					Y = 7 - j
					X = i
					# print("(" + str(X) + ", " + str(Y) + ")")
					ab = AnnotationBbox(
					imagebox,
					[(X*step) + offsetX, (Y*step) + offsetY],
					frameon=False)
					axes.add_artist(ab)

		axes.axis('off')
		return axes

	def acciones_aplicables(self, estado):
		# Devuelve una lista de parejas que representan
		# las casillas vacías en las que es permitido
		# poner una reina adicional
		# Input: estado, que es una np.matrix(8x8)
		# Output: lista de indices (x,y)
		indices = [(x, y) for x in range(8) for y in range(8)]
		indices_bloqueados = []
		# Chequeamos primero que haya menos de ocho reinas
		if estado.sum() >= 8:
			return []
		else:
			# Bloqueamos índices por cada reina encontrada
			for x in range(8):
				for y in range(8):
					if estado[y, x]==1:
						#print("Reina encontrada en", x, y)
						# Encuentra una reina
						# Elimina la fila
						#print("Bloqueando filas...")
						indices_bloqueados += [(i, y) for i in range(8)]
						# Elimina la columna
						#print("Bloqueando columnas...")
						indices_bloqueados += [(x, i) for i in range(8)]
						# Elimina las diagonales \
						# print("\nBloqueando diagonales...")
						dif = np.abs(x-y)
						offset_x = 0
						offset_y = 0
						for i in range(1, 8 - dif):
							if (y + i) == 8:
								offset_x = - (x + i)
								offset_y = dif
							if (x + i) == 8:
								offset_x = dif
								offset_y = - (y + i)
								xB = (x + i + offset_x) % 8
								yB = (y + i + offset_y) % 8
								# print("(" + str(xB) + ", " + str(yB) + ")", end="")
								indices_bloqueados.append((xB, yB))
						# Elimina las transversales /
						# print("\nBloqueando transversales...")
						dif1 = np.abs((7-x)-y)
						# print("\n Dif", dif1)
						offset_x = 0
						offset_y = 0
						for i in range(1, 8 - dif1):
							xB = (x + i + offset_x) % 8
							yB = (y - i + offset_y) % 8
							# print("(" + str(xB) + ", " + str(yB) + ")", end="")
							indices_bloqueados.append((xB, yB))
							if yB == 0:
								offset_x = - (x + i + 1)
								offset_y = x + i + 1
							if xB == 7:
								offset_x = y - (i + 1) - 7
								offset_y = 8 - (y - i)

		return list(set(indices) - set(indices_bloqueados))

	def transicion(self, estado, indices):
		# Devuelve el tablero incluyendo una reina en el indice
		# Input: estado, que es una np.matrix(8x8)
		#        indice, de la forma (x,y)
		# Output: estado, que es una np.matrix(8x8)

		s = copy.deepcopy(estado)
		x = indices[0]
		y = indices[1]
		s[y, x] = 1
		return s

	def test_objetivo(self, estado):
		# Devuelve True/False dependiendo si el estado
		# resuelve el problema
		# Input: estado, que es una np.matrix(8x8)
		# Output: True/False
		# print("Determinando si hay exactamente ocho reinas...")
		num_reinas = estado.sum()
		if num_reinas != 8:
			# print("Numero incorrecto de reinas!")
			return False
		else:
			# print("Determinando si las reinas no se atacan...")
			# print("Buscando reina por fila...")
			filas = [i[0] for i in estado.sum(axis=1).tolist()]
			if any(i>1 for i in filas):
				# print("Dos reinas en la misma fila!")
				return False
			else:
				# print("Buscando reina por columna...")
				columnas = estado.sum(axis=0).tolist()[0]
				if any(j>1 for j in columnas):
					# print("Dos reinas en la misma columna!")
					return False
				else:
					for x in range(8):
						for y in range(8):
							if estado[y, x]==1:
								# print("Reina encontrada en (" + str(x) + ", " + str(y) + ")")
								# print("Buscando otra reina en la misma diagonal...")
								dif = np.abs(x-y)
								offset_x = 0
								offset_y = 0
								for i in range(1, 8 - dif):
									if (y + i) == 8:
										offset_x = - (x + i)
										offset_y = dif
									if (x + i) == 8:
										offset_x = dif
										offset_y = - (y + i)
									xB = (x + i + offset_x) % 8
									yB = (y + i + offset_y) % 8
									if estado[yB, xB] == 1:
										#print("Dos reinas en la misma diagonal!")
										return False

								# print("Buscando otra reina en la misma transversal...")
								dif1 = np.abs((7-x)-y)
								# print("\n Dif", dif1)
								offset_x = 0
								offset_y = 0
								for i in range(1, 8 - dif1):
									xB = (x + i + offset_x) % 8
									yB = (y - i + offset_y) % 8
									# print("(" + str(xB) + ", " + str(yB) + ")", end="")
									if estado[yB, xB]==1:
										# print("Dos reinas en la misma transversal!")
										return False
									if yB == 0:
										offset_x = - (x + i + 1)
										offset_y = x + i + 1
									if xB == 7:
										offset_x = y - (i + 1) - 7
										offset_y = 8 - (y - i)

		return True

	def costo(self, estado, accion):
		return 1

class JarrasAgua:

	'''
	Problema de las jarras de agua: Suponga que usted cuenta con dos jarras de agua, una de tres litros y otra de cuatro, y que también cuenta con acceso a una llave de agua para llenar las jarras. ¿Cómo puede obtener exáctamente dos litros de agua en la jarra de cuatro litros?
	'''
	def __init__(self):
		self.estado_inicial = (0,0)

	def pintar_estado(self, estado):
		# Dibuja el estado de las jarras
		# Input: estado, que es una pareja (x,y)
		fig, axes = plt.subplots()

		x, y = estado

		# Cargando imagen de la jarra de 4 litros
		jarra4 = plt.imread("./imagenes/Agua/jarra.png")
		imagebox = OffsetImage(jarra4, zoom=0.8)
		imagebox.image.axes = axes
		ab = AnnotationBbox(
		imagebox,
		[0.2, 0.45],
		frameon=False
		)
		axes.add_artist(ab)
		offsetbox = TextArea(str(x), textprops={'fontsize':'x-large'})
		ab = AnnotationBbox(offsetbox, (0.2,0))
		axes.add_artist(ab)

		# Cargando imagen de la jarra de 3 litros
		jarra3 = plt.imread("./imagenes/Agua/jarra.png")
		imagebox = OffsetImage(jarra3, zoom=0.7)
		imagebox.image.axes = axes
		ab = AnnotationBbox(
		imagebox,
		[0.7, 0.42],
		frameon=False
		)
		axes.add_artist(ab)
		offsetbox = TextArea(str(y), textprops={'fontsize':'x-large'})
		ab = AnnotationBbox(offsetbox, (0.7,0))
		axes.add_artist(ab)

		if x>0:
			# Llenando la jarra de 4 litros
			aguaX = plt.imread("./imagenes/Agua/agua" + str(x) + ".png")
			imagebox = OffsetImage(aguaX, zoom=0.4)
			y_offsets = [0.25, 0.32, 0.39, 0.45]
			imagebox.image.axes = axes
			ab = AnnotationBbox(
			imagebox,
			[0.2, y_offsets[x-1]],
			frameon=False
			)
			axes.add_artist(ab)

		if y>0:
			# Llenando la jarra de 3 litros
			aguaY = plt.imread("./imagenes/Agua/agua" + str(y) + ".png")
			imagebox = OffsetImage(aguaY, zoom=0.34)
			y_offsets = [0.3, 0.36, 0.41]
			imagebox.image.axes = axes
			ab = AnnotationBbox(
			imagebox,
			[0.7, y_offsets[y-1]],
			frameon=False
			)
			axes.add_artist(ab)

		axes.axis('off')
		return axes

	def pintar_accion(self, estado, accion):
		# Dibuja el estado de las jarras
		# Input: estado, que es una pareja (x,y)
		fig, axes = plt.subplots()

		x, y = estado

		# Cargando imagen de la jarra de 4 litros
		jarra4 = plt.imread("./imagenes/Agua/jarra.png")
		imagebox = OffsetImage(jarra4, zoom=0.8)
		imagebox.image.axes = axes
		ab = AnnotationBbox(
		imagebox,
		[0.2, 0.45],
		frameon=False
		)
		axes.add_artist(ab)
		offsetbox = TextArea(str(x), textprops={'fontsize':'x-large'})
		ab = AnnotationBbox(offsetbox, (0.2,0))
		axes.add_artist(ab)

		# Cargando imagen de la jarra de 3 litros
		jarra3 = plt.imread("./imagenes/Agua/jarra.png")
		imagebox = OffsetImage(jarra3, zoom=0.7)
		imagebox.image.axes = axes
		ab = AnnotationBbox(
		imagebox,
		[0.7, 0.42],
		frameon=False
		)
		axes.add_artist(ab)
		offsetbox = TextArea(str(y), textprops={'fontsize':'x-large'})
		ab = AnnotationBbox(offsetbox, (0.7,0))
		axes.add_artist(ab)

		if x>0:
			# Llenando la jarra de 4 litros
			aguaX = plt.imread("./imagenes/Agua/agua" + str(x) + ".png")
			imagebox = OffsetImage(aguaX, zoom=0.4)
			y_offsets = [0.25, 0.32, 0.39, 0.45]
			imagebox.image.axes = axes
			ab = AnnotationBbox(
			imagebox,
			[0.2, y_offsets[x-1]],
			frameon=False
			)
			axes.add_artist(ab)

		if y>0:
			# Llenando la jarra de 3 litros
			aguaY = plt.imread("./imagenes/Agua/agua" + str(y) + ".png")
			imagebox = OffsetImage(aguaY, zoom=0.34)
			y_offsets = [0.3, 0.36, 0.41]
			imagebox.image.axes = axes
			ab = AnnotationBbox(
			imagebox,
			[0.7, y_offsets[y-1]],
			frameon=False
			)
			axes.add_artist(ab)

		if accion == 1:
			imagen = "./imagenes/Agua/flecha_derecha.png"
			xy = [0.1, 0.97]

		if accion == 2:
			imagen = "./imagenes/Agua/flecha_izquierda.png"
			xy = [0.8, 0.95]

		if accion == 3:
			imagen = "./imagenes/Agua/flecha_izquierda.png"
			xy = [0, 0.97]

		if accion == 4:
			imagen = "./imagenes/Agua/flecha_derecha.png"
			xy = [0.85, 0.9]

		if accion == 5:
			imagen = "./imagenes/Agua/flecha_derecha.png"
			xy = [0.55, 0.9]

		if accion == 6:
			imagen = "./imagenes/Agua/flecha_izquierda.png"
			xy = [0.35, 0.97]

		# Pintando flecha
		flecha = plt.imread(imagen)
		imagebox = OffsetImage(flecha, zoom=0.1)
		imagebox.image.axes = axes
		ab = AnnotationBbox(
		imagebox,
		xy,
		frameon=False
		)
		axes.add_artist(ab)

		axes.axis('off')

		return axes

	def pintar_transicion(self, estado, accion):
		clear_output(wait=True)
		self.pintar_estado(estado)
		plt.show()
		sleep(.5)
		clear_output(wait=True)
		self.pintar_accion(estado, accion)
		plt.show()
		sleep(.5)
		clear_output(wait=True)
		estado = self.transicion(estado, accion)
		self.pintar_estado(estado)
		plt.show()
		sleep(.5)

	def acciones_aplicables(self, estado):
		# Devuelve una lista de números que representan
		# la acción permitida, de acuerdo a la codificación
		# presentada en al formalización del problema más arriba.
		# Input: estado, que es una pareja (x,y)
		# Output: lista de indices (x,y)
		x, y = estado
		acciones = [1, 2, 3, 4, 5, 6]
		if x == 0:
			acciones.remove(3)
			acciones.remove(5)
		if y == 0:
			acciones.remove(4)
			acciones.remove(6)
		if x == 4:
			acciones.remove(1)
		if y == 3:
			acciones.remove(2)
		return acciones

	def transicion(self, estado, accion):
		# Devuelve el estado correspondiente
		# Input: estado, que es una pareja (x,y)
		#        accion, entero de 1 a 6
		# Output: estado, que es una pareja (x,y)
		x, y = estado
		if accion == 1:
			return (4,y)
		if accion == 2:
			return (x,3)
		if accion == 3:
			return (0,y)
		if accion == 4:
			return (x,0)
		if accion == 5:
			d = x if y+x < 3 else 3-y
			return (x-d,y+d)
		if accion == 6:
			d = y if y+x < 4 else 4-x
			return (x+d,y-d)

	def test_objetivo(self, estado):
		# Devuelve True/False dependiendo si el estado
		# resuelve el problema
		# Input: estado, que es una np.matrix(8x8)
		# Output: True/False
		# print("Determinando si hay exactamente ocho reinas...")
		x, y = estado
		return x == 2

	def costo(self, estado, accion):
		return 1

	def codigo(self, estado):
		x, y = estado
		return f"{x}-{y}"

class ViajeRumania:

	'''
	Problema del viaje a Rumania: Planear el camino más corto de una ciudad inicial a una ciudad final.
	'''
	def __init__(self, inicial, final):
		self.estado_inicial = inicial
		self.ciudad_objetivo = final
		self.rutas = {'Oradea':{'Zerind':71, 'Sibiu':151},\
		'Zerind':{'Arad':75, 'Oradea':71},\
		'Arad':{'Timisoara':118, 'Sibiu':140, 'Zerind':71},\
		'Timisoara':{'Lugoj':111, 'Arad':118},\
		'Lugoj':{'Mehadia':70, 'Timisoara':111},\
		'Mehadia':{'Drobeta':75, 'Lugoj':70},\
		'Drobeta':{'Craiova':120, 'Mehadia':75},\
		'Sibiu':{'Fagaras':99, 'Rimnicu Vilcea':80, 'Arad':140, 'Oradea':151},\
		'Rimnicu Vilcea':{'Craiova':146, 'Pitesti':97, 'Sibiu':80},\
		'Craiova':{'Pitesti':138, 'Drobeta':120, 'Rimnicu Vilcea':146},\
		'Fagaras':{'Bucharest':211, 'Sibiu':99},\
		'Pitesti':{'Bucharest':101, 'Craiova':138, 'Rimnicu Vilcea':97},\
		'Bucharest':{'Giurgiu':90, 'Urziceni':85, 'Fagaras':211, 'Pitesti':101},\
		'Giurgiu':{'Bucharest':90},\
		'Urziceni':{'Vaslui':142, 'Hirsova':98, 'Bucharest':85},\
		'Vaslui':{'Iasi':92, 'Urziceni':142},\
		'Iasi':{'Neamt':87, 'Vaslui':92},\
		'Neamt':{'Iasi':87},\
		'Hirsova':{'Eforie':86, 'Urziceni':98},\
		'Eforie':{'Hirsova':86}
		}

	def pintar_estado(self, estado):
		pass

	def acciones_aplicables(self, estado):
		# Devuelve una lista de ciudades a las que se puede llegar
		# desde la ciudad descrita en estado
		# Input: estado, nombre de una ciudad
		# Output: lista de ciudades
		return self.rutas[estado].keys()

	def transicion(self, estado, accion):
		# Devuelve la ciudad a la que se va
		# Input: estado, que es una ciudad
		#        accion, que es una ciudad
		# Output: accion, que es una ciudad
		return accion

	def test_objetivo(self, estado):
		# Devuelve True/False dependiendo si el estado
		# resuelve el problema
		# Input: estado, que es una ciudad
		# Output: True/False
		return estado == self.ciudad_objetivo

	def costo(self, estado, accion):
		return self.rutas[estado][accion]

	def codigo(self, estado):
		return estado

class Laberinto:

	'''
	Problema del laberinto: Planear el camino para salir del laberinto.
	'''
	def __init__(self, inicial,\
	laberinto=np.matrix([[0,0,0,1,0,0,0,0,0,0,0,0],\
	                     [0,1,0,1,0,0,0,0,0,0,0,0],\
						 [0,1,0,1,0,0,0,1,0,0,0,0],\
						 [0,0,0,1,1,1,0,0,0,0,0,0],\
						 [0,0,0,1,0,0,0,0,0,1,0,1],\
						 [0,0,0,0,0,1,0,1,0,0,0,0],\
						 [0,0,0,1,1,0,1,1,0,1,1,0],\
						 [0,1,0,0,0,0,0,0,0,1,0,0],\
						 [0,1,0,0,1,0,0,0,0,1,0,1],\
						 [0,0,0,0,0,0,0,1,0,1,0,0],\
						 [0,1,0,0,0,1,0,1,0,1,1,0],\
						 [0,1,0,0,0,0,0,0,0,0,0,0]
	# laberinto=np.matrix([[0,0,0,1,0,0,0,0,0,0,0,0],\
	#                      [0,1,0,1,0,1,1,1,0,1,0,0],\
	# 					 [0,1,0,1,0,0,0,1,0,1,1,0],\
	# 					 [0,1,0,1,1,1,0,1,0,1,0,0],\
	# 					 [0,1,0,1,0,0,0,1,0,1,0,1],\
	# 					 [0,1,0,0,0,1,0,1,0,1,0,0],\
	# 					 [0,1,0,1,1,1,1,1,0,1,1,0],\
	# 					 [0,1,0,1,0,0,0,1,0,1,0,0],\
	# 					 [0,1,0,1,1,1,0,1,0,1,0,1],\
	# 					 [0,1,0,1,0,0,0,1,0,1,0,0],\
	# 					 [0,1,0,1,0,1,1,1,0,1,1,0],\
	# 					 [0,1,0,0,0,0,0,0,0,0,0,0]
	])):
		# laberinto, una matriz numpy con 1 en la casilla con muro
		self.estado_inicial = inicial
		self.laberinto = laberinto
		self.max = laberinto.shape[0]

	def truncar(self, x):
	    if x < 0:
	        return 0
	    elif x > self.max - 1:
	        return self.max - 1
	    else:
	        return x

	def adyacentes(self, casilla):
	    x, y = casilla
	    adyacentes = [
	        (self.truncar(x - 1), y), (self.truncar(x + 1), y),
	        (x, self.truncar(y - 1)), (x, self.truncar(y + 1))
	    ]
	    adyacentes = [c for c in adyacentes if c != casilla]
	    return adyacentes

	def matrix2lista(self, m):
		lista = np.where(m == 1)
		ran = list(range(len(lista[0])))
		return [(lista[1][i], self.max-1-lista[0][i]) for i in ran]

	def pintar_estado(self, estado):
		# Dibuja el tablero correspondiente al estado
		fig, axes = plt.subplots(figsize=(8, 8))
		# Dibujo el tablero
		step = 1./self.max
		offset = 0.001
		tangulos = []
		# Borde del tablero
		tangulos.append(patches.Rectangle((0,0),0.998,0.998,\
                                          facecolor='cornsilk',\
                                         edgecolor='black',\
                                         linewidth=2))
		# Creo los muros
		muros = self.matrix2lista(self.laberinto)
		for m in muros:
			x, y = m
			tangulos.append(patches.Rectangle(*[(x*step,y*step), step,step],\
                    facecolor='black'))
		for t in tangulos:
			axes.add_patch(t)
		offsetX = 0.045
		offsetY = 0.04
		#Poniendo salida
		X, Y = (0,0)
		arr_img = plt.imread("./imagenes/Laberinto/salida.png", format='png')
		image_salida = OffsetImage(arr_img, zoom=0.025)
		image_salida.image.axes = axes
		ab = AnnotationBbox(
		    image_salida,
		    [(X*step) + offsetX, (Y*step) + offsetY],
		    frameon=False)
		axes.add_artist(ab)
		#Poniendo robot
		X, Y = estado
		arr_img = plt.imread("./imagenes/Laberinto/robot.png", format='png')
		image_robot = OffsetImage(arr_img, zoom=0.125)
		image_robot.image.axes = axes
		ab = AnnotationBbox(
		    image_robot,
		    [(X*step) + offsetX, (Y*step) + offsetY],
		    frameon=False)
		axes.add_artist(ab)
		axes.axis('off')
		return axes

	def pintar_camino(self, camino):
		for casilla in camino:
			clear_output(wait=True)
			self.pintar_estado(casilla)
			plt.show()
			sleep(.25)

	def acciones_aplicables(self, estado):
		# Devuelve una lista de casillas a las que se puede llegar
		# desde la casilla descrita en estado
		# Input: estado, una casilla
		# Output: lista de casillas
		casillas = self.adyacentes(estado)
		casillas = [c for c in casillas if self.laberinto[self.max-1-c[1], c[0]] != 1]
		return casillas

	def transicion(self, estado, accion):
		# Devuelve la casilla a la que se va
		# Input: estado, que es una casilla
		#        accion, que es una casilla
		# Output: accion, que es una casilla
		return accion

	def test_objetivo(self, estado):
		# Devuelve True/False dependiendo si el estado
		# resuelve el problema
		# Input: estado, que es una ciudad
		# Output: True/False
		return estado == (0,0)

	def costo(self, estado, accion):
		return 1

	def codigo(self, estado):
		x, y = estado
		return f"{x}-{y}"

class Rompecabezas:

    def __init__(self, inicial=np.reshape(np.random.choice(9, 9, replace=False), (3,3)), objetivo=np.matrix([[6,7,8], [3,4,5], [0,1,2]]).T):
        self.estado_inicial = inicial
        self.objetivo = objetivo

    def pintar_estado(self, estado):
        # Dibuja el tablero correspondiente al estado
        # Input: estado, que es una np.matrix
        fig, axes = plt.subplots()
        # Dibujo el tablero
        step = 1./3
        offset = 0.001
        tangulos = []
        # Borde del tablero
        tangulos.append(patches.Rectangle((0,0),0.998,0.998,\
            facecolor='cornsilk',\
            edgecolor='black',\
            linewidth=2))
        # Creo las lÃ­neas del tablero
        for j in range(8):
            locacion = j * step
            # Crea linea horizontal en el rectangulo
            tangulos.append(patches.Rectangle(*[(0, locacion), 1, 0.008],\
            facecolor='black'))
            # Crea linea vertical en el rectangulo
            tangulos.append(patches.Rectangle(*[(locacion, 0), 0.008, 1],\
            facecolor='black'))
        for t in tangulos:
            axes.add_patch(t)
        # Cargando numeros
        offsetX = 0.135
        offsetY = 0.11
        for i in range(1,9):
            x, y = np.where(estado == i)
            X = x[0]
            Y = y[0]
            axes.text(X*step+offsetX, Y*step+offsetY, str(i), fontsize=42)
            axes.axis('off')
        return axes

    def pintar_camino(self, camino):
        estados = [self.estado_inicial]
        for transicion in camino:
        	estados.append(self.transicion(estados[-1], transicion))
        for estado in estados:
        	clear_output(wait=True)
        	self.pintar_estado(estado)
        	plt.show()
        	sleep(1)

    def acciones_aplicables(self, estado):
        # Devuelve una lista de fichas que es posible mover
        # y en qué dirección
        # Input: estado, que es una np.matrix(8x8)
        # Output: lista de parejas ((x1,y1), (x2,y2))
        # Es decir, la ficha en la posición (x1,y1) puede moverse a (x2,y2)
        y, x = np.where(estado == 0)
        y = y[0]
        x = x[0]
        if x == 0:
            if y == 0:
                return [((x + 1, y), (x, y)),
                        ((x, y + 1), (x, y))
                       ]
            elif y == 2:
                return [((x + 1, y), (x, y)),
                        ((x, y - 1), (x, y))
                       ]
            else:
                return [((x + 1, y), (x, y)),
                        ((x, y + 1), (x, y)),
                        ((x, y - 1), (x, y))
                       ]
        if x == 2:
            if y == 0:
                return [((x - 1, y), (x, y)),
                        ((x, y + 1), (x, y))
                       ]
            elif y == 2:
                return [((x - 1, y), (x, y)),
                        ((x, y - 1), (x, y))
                       ]
            else:
                return [((x - 1, y), (x, y)),
                        ((x, y + 1), (x, y)),
                        ((x, y - 1), (x, y))
                       ]
        else:
            if y == 0:
                return [((x - 1, y), (x, y)),
                        ((x + 1, y), (x, y)),
                        ((x, y + 1), (x, y))
                       ]
            elif y == 2:
                return [((x - 1, y), (x, y)),
                        ((x + 1, y), (x, y)),
                        ((x, y - 1), (x, y))
                       ]
            else:
                return [((x - 1, y), (x, y)),
                        ((x + 1, y), (x, y)),
                        ((x, y + 1), (x, y)),
                        ((x, y - 1), (x, y))
                       ]

    def transicion(self, estado, indices):
        # Devuelve el tablero moviendo la ficha en indice
        # Input: estado, que es una np.matrix(8x8)
        #        indice, de la forma ((x1,y1), (x2,y2))
        # Output: estado, que es una np.matrix(8x8)

        s = copy.deepcopy(estado)
        x1, y1 = indices[0]
        x2, y2 = indices[1]
        s[y2, x2] = estado[y1, x1]
        s[y1, x1] = 0
        return s

    def test_objetivo(self, estado):
        # Devuelve True/False dependiendo si el estado
        # resuelve el problema
        # Input: estado, que es una np.matrix(8x8)
        # Output: True/False
        k = list(np.reshape(estado, (9,1)))
        k = [x[0] for x in k]
        o = list(np.reshape(self.objetivo, (9,1)))
        o = [x[0] for x in o]
        return (k == o)

    def costo(self, estado, accion):
        return 1

    def codigo(self, estado):
        inicial = True
        for fila in estado:
            for simbolo in fila:
            	if inicial:
            		cadena = str(simbolo)
            		inicial = False
            	else:
            		cadena += "-" + str(simbolo)
        return cadena

class Triqui:

    def __init__(self):
        self.estado_inicial = np.matrix([[0]*3]*3)

    def pintar_estado(self, estado):
        # Dibuja el tablero correspondiente al estado
        # Input: estado, que es una 3-lista de 3-listas
        fig, axes = plt.subplots()

        # Dibujo el tablero
        step = 1./3
        offset = 0.001
        tangulos = []

        # Borde del tablero
        tangulos.append(patches.Rectangle((0,0),0.998,0.998,\
                                          facecolor='cornsilk',\
                                         edgecolor='black',\
                                         linewidth=2))

        # Creo las líneas del tablero
        for j in range(3):
            locacion = j * step
            # Crea linea horizontal en el rectangulo
            tangulos.append(patches.Rectangle(*[(0, locacion), 1, 0.008],\
                    facecolor='black'))
            # Crea linea vertical en el rectangulo
            tangulos.append(patches.Rectangle(*[(locacion, 0), 0.008, 1],\
                    facecolor='black'))

        for t in tangulos:
            axes.add_patch(t)

        # Cargando imagen de O
        arr_img_O = plt.imread("./imagenes/Triqui/O.png", format='png')
        image_O = OffsetImage(arr_img_O, zoom=0.14)
        image_O.image.axes = axes

        # Cargando imagen de X
        arr_img_X = plt.imread("./imagenes/Triqui/X.png", format='png')
        image_X = OffsetImage(arr_img_X, zoom=0.14)
        image_X.image.axes = axes

        offsetX = 0.15
        offsetY = 0.15

        # ASUMO QUE LAS O SE REPRESENTAN CON 1 EN LA MATRIZ
        # Y QUE LAS X SE REPRESENTAN CON 2
        for i in range(3):
            for j in range(3):
                if estado[j, i] == 1:
                    # print("O en (" + str(i) + ", " + str(j) + ")")
                    Y = j
                    X = i
                    # print("(" + str(X) + ", " + str(Y) + ")")
                    ab = AnnotationBbox(
                        image_O,
                        [(X*step) + offsetX, (Y*step) + offsetY],
                        frameon=False)
                    axes.add_artist(ab)
                if estado[j, i] == 2:
                    # print("X en (" + str(i) + ", " + str(j) + ")")
                    Y = j
                    X = i
                    # print("(" + str(X) + ", " + str(Y) + ")")
                    ab = AnnotationBbox(
                        image_X,
                        [(X*step) + offsetX, (Y*step) + offsetY],
                        frameon=False)
                    axes.add_artist(ab)

        axes.axis('off')
        return axes

    def a_jugar(self, estado):
        # Devuelve el número del jugador a quien corresponde el turno
        # 1 para las O
        # 2 para las X
        num_Os = np.count_nonzero(estado==1)
        num_Xs = np.count_nonzero(estado==2)
        # print("Cantidad O:", num_Os, " Cantidad X:", num_Xs)
        if num_Os < num_Xs:
            return 1
        else:
            return 2

    def acciones(self, estado):
        # Devuelve una lista de parejas que representan las casillas vacías
        # Input: estado, que es una np.matrix(3x3)
        # Output: lista de índices (x,y)
        indices = []
        if np.count_nonzero(estado==0)>0:
            for x in range(3):
                for y in range(3):
                    if estado[y, x] == 0:
                        indices.append((x, y))

        return indices

    def resultado(self, estado, indice):
        # Devuelve el tablero incluyendo una O o X en el indice,
        # dependiendo del jugador que tiene el turno
        # Input: estado, que es una np.matrix(3x3)
        #        indice, de la forma (x,y)
        # Output: estado, que es una np.matrix(3x3)

        s = copy.deepcopy(estado)
        x = indice[0]
        y = indice[1]
        s[y, x] = self.a_jugar(estado)

        return s

    def es_terminal(self, estado):
        # Devuelve True/False dependiendo si el juego se acabó
        # Input: estado, que es una np.matrix(3x3)
        # Output: objetivo, True/False
        # print("Determinando si no hay casillas vacías...")
        if np.count_nonzero(estado==0)==0:
            return True
        else:
            # print("Buscando triqui horizontal...")
            for y in range(3):
                num_Os = np.count_nonzero(estado[y,:]==1)
                num_Xs = np.count_nonzero(estado[y,:]==2)
                # print("Cantidad O:", num_Os, " Cantidad X:", num_Xs)
                if (num_Os==3) or (num_Xs==3):
                    return True

            # print("Buscando triqui vertical...")
            for x in range(3):
                num_Os = np.count_nonzero(estado[:,x]==1)
                num_Xs = np.count_nonzero(estado[:,x]==2)
                # print("Cantidad O:", num_Os, " Cantidad X:", num_Xs)
                if (num_Os==3) or (num_Xs==3):
                    return True

            # print("Buscando triqui diagonal...")
            if (estado[0,0]==1) and (estado[1,1]==1) and (estado[2,2]==1):
                return True
            elif (estado[0,0]==2) and (estado[1,1]==2) and (estado[2,2]==2):
                return True

            # print("Buscando triqui transversal...")
            if (estado[2,0]==1) and (estado[1,1]==1) and (estado[0,2]==1):
                return True
            elif (estado[2,0]==2) and (estado[1,1]==2) and (estado[0,2]==2):
                return True

        return False

    def utilidad(self, estado, jugador):
        # Devuelve la utilidad del estado donde termina el juego
        # Input: estado, que es una np.matrix(3x3)
        # Output: utilidad, que es un valor -1, 0, 1
        ob = self.es_terminal(estado)
        if ob:
            # Determina quién ganó la partida o si hay empate
            if np.count_nonzero(estado==0)==0:
                return 0
            else:
                if jugador == 1: # Acaba de jugar X
                    return 1
                if jugador == 2: # Acaba de jugar O
                    return -1

        return None

class ReyTorreRey:

    '''
    Usa la librería python-chess
    Documentación en https://python-chess.readthedocs.io/en/latest/index.html
    '''

    def __init__(self, jugador='negras', tablero_inicial=1):
        if jugador == 'blancas':
            pl = ' w'
        elif jugador == 'negras':
            pl = ' b'
        else:
            raise NameError('¡Jugador incorrecto! Debe ser \'blancas\' o \'negras\'.' )
        dict_tableros = {1:chess.Board("2R5/8/8/8/8/8/k1K5/8" + pl),\
						 2:chess.Board("2R5/8/8/8/8/8/1k1K4/8" + pl),\
						 3:chess.Board("8/8/8/8/8/2R5/1k1K4/8" + pl),\
						 4:chess.Board("8/8/8/8/8/8/1k1K4/2R5" + pl),\
						 5:chess.Board("8/8/8/3k4/8/8/6K1/7R" + pl)}
        self.estado_inicial = dict_tableros[tablero_inicial]

    def pintar_estado(self, board):
        # Dibuja el tablero correspondiente al estado
        # Input: estado
        return board

    def a_jugar(self, board):
        # Devuelve el jugador a quien corresponde el turno
        if board.turn:
            return 'blancas'
        else:
            return 'negras'

    def acciones(self, board):
        # Devuelve una lista de acciones legales en el tablero
        # Input: estado
        # Output: lista de jugadas en notación algebráica estándar (SAN)
        return list(board.legal_moves)

    def jugada_manual(self, board, accion):
        if board.parse_san(accion) in board.legal_moves:
            board_copy = copy.deepcopy(board)
            board_copy.push_san(accion)
            return board_copy
        else:
            raise NameError('Formato de acción incorrecta. Debe estar en notación algebráica estándar.')

    def resultado(self, board, accion):
        # Devuelve el tablero resultado de la jugada,
        # dependiendo del jugador que tiene el turno
        # Input: estado
        #        accion
        # Output: estado
        board_copy = copy.deepcopy(board)
#        print(board_copy)
        board_copy.push(accion)
        return board_copy

    def es_terminal(self, board):
        # Devuelve True/False dependiendo si el juego se acabó
        # Input: estado, que es una np.matrix(3x3)
        # Output: objetivo, True/False
        # print("Determinando si no hay casillas vacías...")
        if board.outcome() is not None:
            return True
        else:
            return False

    def utilidad(self, board, jugador):
        # Devuelve la utilidad del estado donde termina el juego
        # Input: estado, que es una np.matrix(3x3)
        # Output: utilidad, que es un valor -1, 0, 1
        if board.outcome() is not None:
            fin = str(board.outcome().termination)
            if 'CHECK' in fin:
                if board.turn:
                    return -1000
                else:
                    return 1000
            else:
                return 0
        else:
            return None

    def casilla_pieza(self, board, pieza):
        tablero = str(board).split('\n')
        fila = [i for i in range(len(tablero)) if pieza in tablero[i]][0]
        columna = tablero[fila].replace(' ', '').find(pieza)
        return (fila, columna)
