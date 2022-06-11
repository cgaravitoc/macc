import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage, TextArea
import numpy as np
from random import choice, sample

class Laberinto:
	'''
	Laberinto: Rejilla con muros y pasadizos.
	'''
	def __init__(self, salida=(0,0), pos_inicial=(11,11), dir_agente='oeste', laberinto=None):

		# laberinto, una matriz numpy con 1 en la casilla con muro
		if laberinto == None:
			self.laberinto = np.matrix([[0,0,0,1,0,0,0,0,0,0,0,0],\
							[0,1,0,1,0,0,0,0,0,0,0,0],\
							[0,1,0,1,0,0,0,1,0,0,0,0],\
							[0,0,0,1,1,1,0,0,0,0,0,0],\
							[0,0,0,1,0,0,0,0,0,1,1,1],\
							[0,0,0,0,0,1,1,1,0,1,0,0],\
							[0,0,0,1,1,0,0,0,0,1,1,0],\
							[0,1,0,1,0,0,1,0,0,1,0,0],\
							[0,1,0,0,0,1,0,0,0,1,0,1],\
							[0,0,0,0,0,0,0,0,0,1,0,0],\
							[0,1,0,0,0,0,1,1,1,1,1,0],\
							[0,1,0,0,0,0,0,0,0,0,0,0]])
		else:
			self.laberinto = laberinto
		self.agente = pos_inicial
		self.dir_agente = dir_agente
		self.max = self.laberinto.shape[0]
		self.salida = salida

	def truncar(self, x):
	    if x < 0:
	        return 0
	    elif x > self.max - 1:
	        return self.max - 1
	    else:
	        return x

	def matrix2lista(self, m):
		lista = np.where(m == 1)
		ran = list(range(len(lista[0])))
		return [(lista[1][i], self.max-1-lista[0][i]) for i in ran]

	def pintar(self):
		# Dibuja el laberinto
		estado = self.agente
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
		arr_img = plt.imread("../images/Laberinto/salida.png", format='png')
		image_salida = OffsetImage(arr_img, zoom=0.025)
		image_salida.image.axes = axes
		ab = AnnotationBbox(
		    image_salida,
		    [(X*step) + offsetX, (Y*step) + offsetY],
		    frameon=False)
		axes.add_artist(ab)
		#Poniendo robot
		X, Y = estado
		imagen_robot = "../images/Laberinto/robot_" + self.dir_agente + ".png"
		arr_img = plt.imread(imagen_robot, format='png')
		image_robot = OffsetImage(arr_img, zoom=0.125)
		image_robot.image.axes = axes
		ab = AnnotationBbox(
		    image_robot,
		    [(X*step) + offsetX, (Y*step) + offsetY],
		    frameon=False)
		axes.add_artist(ab)
		axes.axis('off')
		plt.show()

	def test_objetivo(self):
		# Devuelve True/False dependiendo si el agente está
		# en la salida
		return self.agente == self.salida

	def para_sentidos(self):
		# Devuelve una lista de muro o pasadizo dependiendo
		# de dónde está el agente
		# El orden de sensores es [derecha, arriba, izquierda, abajo]
		x, y = self.agente
		derecha = (x+1, y) if self.truncar(x+1) == x+1 else False
		arriba = (x, y+1) if self.truncar(y+1) == y+1 else False
		izquierda = (x-1, y) if self.truncar(x-1) == x-1 else False
		abajo = (x, y-1) if self.truncar(y-1) == y-1 else False
		if self.dir_agente == 'oeste':
			casillas = [izquierda, abajo, arriba, derecha]
		elif self.dir_agente == 'este':
			casillas = [derecha, arriba, abajo, izquierda]
		elif self.dir_agente == 'norte':
			casillas = [arriba, izquierda, derecha, abajo]
		elif self.dir_agente == 'sur':
			casillas = [abajo, derecha, izquierda, arriba]
		m = self.max - 1
		f = lambda c: self.laberinto[(m - c[1], c[0])]==1 if c != False else not c
		return [f(c) for c in casillas]

	def transicion(self, accion):
		x, y = self.agente
		m = self.max - 1
		direcciones = ['este', 'norte', 'oeste', 'sur']
		if accion == 'voltearIzquierda':
			ind_actual = direcciones.index(self.dir_agente)
			self.dir_agente = direcciones[(ind_actual + 1) % 4]
		elif accion == 'voltearDerecha':
			ind_actual = direcciones.index(self.dir_agente)
			self.dir_agente = direcciones[(ind_actual - 1) % 4]
		elif accion == 'adelante':
			if (self.dir_agente == 'oeste'):
				accion1 = 'izquierda'
			elif (self.dir_agente == 'este'):
				accion1 = 'derecha'
			elif (self.dir_agente == 'norte'):
				accion1 = 'arriba'
			elif (self.dir_agente == 'sur'):
				accion1 = 'abajo'
			if (accion1 == 'derecha'):
				if (self.truncar(x+1) == x+1):
					correccion = (m - y, x+1)
					if (self.laberinto[correccion] == 0):
						self.agente = (x+1, y)
			elif (accion1 == 'izquierda'):
				if (self.truncar(x-1) == x-1):
					correccion = (m - y, x-1)
					if (self.laberinto[correccion] == 0):
						self.agente = (x-1, y)
			elif (accion1 == 'arriba'):
				if (self.truncar(y+1) == y+1):
					correccion = (m - (y+1), x)
					if (self.laberinto[correccion] == 0):
						self.agente = (x, y+1)
			elif (accion1 == 'abajo'):
				if (self.truncar(y-1) == y-1):
					correccion = (m - (y-1), x)
					if (self.laberinto[correccion] == 0):
						self.agente = (x, y-1)
		else:
			raise Exception('¡Acción inválida:', accion)

class Wumpus:

    def __init__(self, wumpus=None, oro=None, pozos=None):
        casillas = [(x, y) for x in range(4) for y in range(4)]
        casillas_sin_inicial = [casilla for casilla in casillas if casilla != (0,0)]
        if wumpus is None:
            self.wumpus = choice(casillas_sin_inicial)
        else:
            self.wumpus = wumpus
        self.wumpus_vivo = True
        self.hedor = self.adyacentes(self.wumpus)
        if oro is None:
            self.oro = choice(casillas)
        else:
            self.oro = oro
        self.oro_tomado = False
        if pozos is None:
            self.pozos = sample(casillas_sin_inicial, int(len(casillas_sin_inicial)*0.2))
        else:
            self.pozos = pozos
        aux = []
        for c in self.pozos:
            aux += self.adyacentes(c)
        self.brisa = aux
        self.heroe = (0, 0)
        self.flecha = True
        self.dir_agente = 'este'
        self.puntaje = 0
        self.juego_activo = True
        self.grito = False # para determinar cuándo el wumpus grita de agonía
        self.bump = False # para determinar cuándo el agente golpea un muro
        self.mensaje = ''

    def truncar(self, x):
        if x < 0:
            return 0
        elif x > 3:
            return 3
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

    def pintar_todo(self):
        # Dibuja el tablero correspondiente al estado
        fig, axes = plt.subplots(figsize=(8, 8))

        # Dibujo el tablero
        step = 1./4
        offset = 0.001
        tangulos = []

        # Borde del tablero
        tangulos.append(patches.Rectangle((0,0),0.998,0.998,\
                                          facecolor='cornsilk',\
                                         edgecolor='black',\
                                         linewidth=2))

        # Creo las líneas del tablero
        for j in range(4):
            locacion = j * step
            # Crea linea horizontal en el rectangulo
            tangulos.append(patches.Rectangle(*[(0, locacion), 1, 0.008],\
                    facecolor='black'))
            # Crea linea vertical en el rectangulo
            tangulos.append(patches.Rectangle(*[(locacion, 0), 0.008, 1],\
                    facecolor='black'))

        for t in tangulos:
            axes.add_patch(t)

        # Cargando imagen del heroe
        arr_img_hero = plt.imread("../images/hero_" + self.dir_agente + ".png", format='png')
        image_hero = OffsetImage(arr_img_hero, zoom=0.3)
        image_hero.image.axes = axes

        # Cargando imagen del Wumpus
        arr_img_wumpus = plt.imread("../images/wumpus.png", format='png')
        image_wumpus = OffsetImage(arr_img_wumpus, zoom=0.45)
        image_wumpus.image.axes = axes

        # Cargando imagen del hedor
        arr_img_stench = plt.imread("../images/stench.png", format='png')
        image_stench = OffsetImage(arr_img_stench, zoom=0.35)
        image_stench.image.axes = axes

        # Cargando imagen del oro
        arr_img_gold = plt.imread("../images/gold.png", format='png')
        image_gold = OffsetImage(arr_img_gold, zoom=0.25)
        image_gold.image.axes = axes

        # Cargando imagen del pozo
        arr_img_pit = plt.imread("../images/pit.png", format='png')
        image_pit = OffsetImage(arr_img_pit, zoom=0.35)
        image_pit.image.axes = axes

        # Cargando imagen de la brisa
        arr_img_breeze = plt.imread("../images/breeze.png", format='png')
        image_breeze = OffsetImage(arr_img_breeze, zoom=0.35)
        image_breeze.image.axes = axes

        offsetX = 0.125
        offsetY = 0.125

        for casilla in self.pozos:
            # Pintando un pozo
            X, Y = casilla
            ab = AnnotationBbox(
                image_pit,
                [(X*step) + offsetX, (Y*step) + offsetY],
                frameon=False)
            axes.add_artist(ab)

        for casilla in self.hedor:
            # Pintando el hedor
            X, Y = casilla
            ab = AnnotationBbox(
                image_stench,
                [(X*step) + offsetX, (Y*step) + offsetY - 0.075],
                frameon=False)
            axes.add_artist(ab)

        for casilla in self.brisa:
            # Pintando la brisa
            X, Y = casilla
            ab = AnnotationBbox(
                image_breeze,
                [(X*step) + offsetX, (Y*step) + offsetY + 0.075],
                frameon=False)
            axes.add_artist(ab)

        # Pintando el wumpus
        X, Y = self.wumpus
        ab = AnnotationBbox(
            image_wumpus,
            [(X*step) + offsetX, (Y*step) + offsetY],
            frameon=False)
        axes.add_artist(ab)

        # Pintando el heroe
        X, Y = self.heroe
        ab = AnnotationBbox(
            image_hero,
            [(X*step) + offsetX, (Y*step) + offsetY],
            frameon=False)
        axes.add_artist(ab)

        # Pintando el oro
        if not self.oro_tomado:
            X, Y = self.oro
            ab = AnnotationBbox(
                image_gold,
                [(X*step) + offsetX, (Y*step) + offsetY],
                frameon=False)
            axes.add_artist(ab)

        axes.axis('off')
        return axes

    def pintar_casilla(self):
        if self.juego_activo:
            # Dibuja el tablero correspondiente al estado
            fig, axes = plt.subplots(figsize=(8, 8))

            # Dibujo el tablero
            step = 1./4
            offset = 0.001
            tangulos = []

            # Borde del tablero
            tangulos.append(patches.Rectangle((0,0),0.998,0.998,\
                                              facecolor='cornsilk',\
                                             edgecolor='black',\
                                             linewidth=2))

            # Creo las líneas del tablero
            for j in range(4):
                locacion = j * step
                # Crea linea horizontal en el rectangulo
                tangulos.append(patches.Rectangle(*[(0, locacion), 1, 0.008],\
                        facecolor='black'))
                # Crea linea vertical en el rectangulo
                tangulos.append(patches.Rectangle(*[(locacion, 0), 0.008, 1],\
                        facecolor='black'))

            for t in tangulos:
                axes.add_patch(t)

            # Cargando imagen del heroe
            arr_img_hero = plt.imread("../images/hero_" + self.dir_agente + ".png", format='png')
            image_hero = OffsetImage(arr_img_hero, zoom=0.3)
            image_hero.image.axes = axes

            # Cargando imagen del Wumpus
            arr_img_wumpus = plt.imread("../images/wumpus.png", format='png')
            image_wumpus = OffsetImage(arr_img_wumpus, zoom=0.45)
            image_wumpus.image.axes = axes

            # Cargando imagen del hedor
            arr_img_stench = plt.imread("../images/stench.png", format='png')
            image_stench = OffsetImage(arr_img_stench, zoom=0.35)
            image_stench.image.axes = axes

            # Cargando imagen del oro
            arr_img_gold = plt.imread("../images/gold.png", format='png')
            image_gold = OffsetImage(arr_img_gold, zoom=0.25)
            image_gold.image.axes = axes

            # Cargando imagen del pozo
            arr_img_pit = plt.imread("../images/pit.png", format='png')
            image_pit = OffsetImage(arr_img_pit, zoom=0.35)
            image_pit.image.axes = axes

            # Cargando imagen de la brisa
            arr_img_breeze = plt.imread("../images/breeze.png", format='png')
            image_breeze = OffsetImage(arr_img_breeze, zoom=0.35)
            image_breeze.image.axes = axes

            offsetX = 0.125
            offsetY = 0.125

            casilla = self.heroe

            if casilla in self.pozos:
                # Pintando un pozo
                X, Y = casilla
                ab = AnnotationBbox(
                    image_pit,
                    [(X*step) + offsetX, (Y*step) + offsetY],
                    frameon=False)
                axes.add_artist(ab)

            if casilla in self.hedor:
                # Pintando el hedor
                X, Y = casilla
                ab = AnnotationBbox(
                    image_stench,
                    [(X*step) + offsetX, (Y*step) + offsetY - 0.075],
                    frameon=False)
                axes.add_artist(ab)

            if casilla in self.brisa:
                # Pintando la brisa
                X, Y = casilla
                ab = AnnotationBbox(
                    image_breeze,
                    [(X*step) + offsetX, (Y*step) + offsetY + 0.075],
                    frameon=False)
                axes.add_artist(ab)

            if casilla == self.wumpus:
                # Pintando el wumpus
                X, Y = self.wumpus
                ab = AnnotationBbox(
                    image_wumpus,
                    [(X*step) + offsetX, (Y*step) + offsetY],
                    frameon=False)
                axes.add_artist(ab)

            # Pintando el heroe
            X, Y = casilla
            ab = AnnotationBbox(
                image_hero,
                [(X*step) + offsetX, (Y*step) + offsetY],
                frameon=False)
            axes.add_artist(ab)

            if casilla == self.oro:
                # Pintando el oro
                if not self.oro_tomado:
                    X, Y = self.oro
                    ab = AnnotationBbox(
                        image_gold,
                        [(X*step) + offsetX, (Y*step) + offsetY],
                        frameon=False)
                    axes.add_artist(ab)

            axes.axis('off')
            return axes
        else:
            return None

    def transicion(self, accion):
        if self.juego_activo:
            self.grito = False
            self.bump = False
            self.puntaje -= 1
            if accion == 'agarrar':
                if (self.oro == self.heroe) and (self.oro_tomado == False):
                    self.puntaje += 1000
                    self.oro_tomado = True
            elif accion == 'adelante':
                x, y = self.heroe
                if self.dir_agente == 'este':
                    self.heroe = (self.truncar(x + 1), y)
                    self.bump = True if self.truncar(x + 1) == x else False
                if self.dir_agente == 'oeste':
                    self.heroe = (self.truncar(x - 1), y)
                    self.bump = True if self.truncar(x - 1) == x else False
                if self.dir_agente == 'norte':
                    self.heroe = (x, self.truncar(y + 1))
                    self.bump = True if self.truncar(y + 1) == y else False
                if self.dir_agente == 'sur':
                    self.heroe = (x, self.truncar(y - 1))
                    self.bump = True if self.truncar(y - 1) == y else False
            elif accion == 'salir':
                if self.heroe == (0, 0):
                    self.juego_activo = False
                    print("¡Juego terminado!")
                    print("Puntaje:", self.puntaje)
                    self.mensaje = "Juego terminado!\n Puntaje: " + str(self.puntaje)
                    self.pintar_todo()
            elif accion == 'voltearIzquierda':
                if self.dir_agente == 'este':
                    self.dir_agente = 'norte'
                elif self.dir_agente == 'oeste':
                    self.dir_agente = 'sur'
                elif self.dir_agente == 'norte':
                    self.dir_agente = 'oeste'
                elif self.dir_agente == 'sur':
                    self.dir_agente = 'este'
            elif accion == 'voltearDerecha':
                if self.dir_agente == 'este':
                    self.dir_agente = 'sur'
                elif self.dir_agente == 'oeste':
                    self.dir_agente = 'norte'
                elif self.dir_agente == 'norte':
                    self.dir_agente = 'este'
                elif self.dir_agente == 'sur':
                    self.dir_agente = 'oeste'
            elif accion == 'disparar':
                if self.flecha:
                    self.flecha = False
                    if self.wumpus_vivo:
                        x_wumpus, y_wumpus = self.wumpus
                        x_heroe, y_heroe = self.heroe
                        if (self.dir_agente == 'este') and ((x_heroe < x_wumpus) and (y_heroe == y_wumpus)):
                            self.wumpus_vivo = False
                            self.grito = True
                            print("¡El wumpus ha caido!") # imprime aviso impacto al wumpus (carlos)
                        if (self.dir_agente == 'oeste') and ((x_heroe > x_wumpus) and (y_heroe == y_wumpus)):
                            self.wumpus_vivo = False
                            self.grito = True
                            print("¡El wumpus ha caido!") # imprime aviso impacto al wumpus (carlos)
                        if (self.dir_agente == 'norte') and ((y_heroe < y_wumpus) and (x_heroe == x_wumpus)):
                            self.wumpus_vivo = False
                            self.grito = True
                            print("¡El wumpus ha caido!") # imprime aviso impacto al wumpus (carlos)
                        if (self.dir_agente == 'sur') and ((y_heroe > y_wumpus) and (x_heroe == x_wumpus)):
                            self.wumpus_vivo = False
                            self.grito = True
                            print("¡El wumpus ha caido!") # imprime aviso impacto al wumpus (carlos)
            else:
                print('¡Acción incorrecta!', accion)
            if self.heroe in self.pozos:
                self.puntaje -= 1000
                self.juego_activo = False
                self.mensaje = "¡Juego terminado!\n" + "El héroe a caido en un pozo\n" + "Puntaje: " + str(self.puntaje)
                print("¡Juego terminado!")
                print("El héroe a caido en un pozo")
                print("Puntaje:", self.puntaje)
                self.pintar_todo()
            elif (self.heroe == self.wumpus) and self.wumpus_vivo:
                self.puntaje -= 1000
                self.juego_activo = False
                self.mensaje = "¡Juego terminado!\n" + "El héroe ha sido devorado por el Wumpus\n" + "Puntaje: " + str(self.puntaje)
                print("¡Juego terminado!")
                print("El héroe ha sido devorado por el Wumpus")
                print("Puntaje:", self.puntaje)
                self.pintar_todo()
        else:
            print("El juego ha terminado.")

    def para_sentidos(self):
        # Lista de sensores [hedor, brisa, brillo, batacazo, grito]
        hedor = 'hedor' if self.heroe in self.hedor else None
        brisa = 'brisa' if self.heroe in self.brisa else None
        brillo = 'brillo' if ((self.heroe == self.oro) and not self.oro_tomado) else None
        batacazo = 'batacazo' if self.bump else None
        grito = 'grito' if self.grito else None
        return [hedor, brisa, brillo, batacazo, grito]

def voltear(direccion_inicial, direccion_final):
    acciones = []
    if direccion_inicial == direccion_final:
        return acciones
    else:
        if direccion_final == 'este':
            if direccion_inicial == 'norte':
                acciones.append('voltearDerecha')
            elif direccion_inicial == 'sur':
                acciones.append('voltearIzquierda')
            elif direccion_inicial == 'oeste':
                acciones.append('voltearDerecha')
                acciones.append('voltearDerecha')
        elif direccion_final == 'norte':
            if direccion_inicial == 'este':
                acciones.append('voltearIzquierda')
            elif direccion_inicial == 'sur':
                acciones.append('voltearIzquierda')
                acciones.append('voltearIzquierda')
            elif direccion_inicial == 'oeste':
                acciones.append('voltearDerecha')
        elif direccion_final == 'oeste':
            if direccion_inicial == 'este':
                acciones.append('voltearIzquierda')
                acciones.append('voltearIzquierda')
            elif direccion_inicial == 'sur':
                acciones.append('voltearDerecha')
            elif direccion_inicial == 'norte':
                acciones.append('voltearIzquierda')
        elif direccion_final == 'sur':
            if direccion_inicial == 'este':
                acciones.append('voltearDerecha')
            elif direccion_inicial == 'norte':
                acciones.append('voltearDerecha')
                acciones.append('voltearDerecha')
            elif direccion_inicial == 'oeste':
                acciones.append('voltearIzquierda')
    return acciones

def acciones_camino(camino, direccion):
    acciones = []
    for i in range(len(camino) - 1):
        x1, y1 = camino[i]
        x2, y2 = camino[i + 1]
        diferencia_x = x2 - x1
        diferencia_y = y2 - y1
        if (diferencia_x != 0) and (diferencia_y != 0):
            print("Camino incorrecto!: No debe incluir diagonales.")
            return None
        elif diferencia_x > 0:
            acciones += voltear(direccion, 'este')
            direccion = 'este'
        elif diferencia_x < 0:
            acciones += voltear(direccion, 'oeste')
            direccion = 'oeste'
        elif diferencia_y > 0:
            acciones += voltear(direccion, 'norte')
            direccion = 'norte'
        elif diferencia_y < 0:
            acciones += voltear(direccion, 'sur')
            direccion = 'sur'
        acciones.append('adelante')
    return acciones

def vis(agente):
    for d in agente.base.datos:
        if 'en(' in d:
            print(d)    
    for d in agente.base.datos:
        if 'mirando' in d:
            print(d)    
    for d in agente.base.datos:
        if 'visitada(' in d:
            print(d)
