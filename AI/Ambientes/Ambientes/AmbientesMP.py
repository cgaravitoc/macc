import copy
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage, TextArea
from time import sleep
from IPython.display import clear_output
import numpy as np
import pandas as pd
import random as rd
from PIL import Image, ImageDraw, ImageFont
import networkx as nx
from itertools import product, permutations
from nltk import Tree

class Hannoi:
    '''
    @Autores: Daniel Ramirez y Jenny Rivera
    '''
    # Recibe como entrada el número de discos en la torre
    # En la inicialización está el estado inicial y el estado objetivo
    def __init__(self, num_disc = 3):
        self.num_disc = num_disc
        zeros = np.ones(self.num_disc).reshape(-1,1)*(self.num_disc +1)
        torre = (np.arange(self.num_disc)+1).reshape(-1,1)
        mtrx = np.hstack([torre, zeros, zeros])
        mtrx_final = np.hstack([zeros, zeros, torre])
        self.estado_inicial = mtrx
        self.estado_objetivo = mtrx_final

    def pintar_estado(self, estado):
        fig, axes = plt.subplots()
        #Cargando imagen de torre 1:inicial
        Torre1 = plt.imread("./Hanoi/Torre.jpg")
        imagebox = OffsetImage(Torre1, zoom=0.45)
        imagebox.image.axes = axes
        ab = AnnotationBbox( imagebox, [0.18, 0.45], frameon=False)
        axes.add_artist(ab)
        #Cargando imagen de torre 2:auxiliar
        Torre2 = plt.imread("./Hanoi/Torre.jpg")
        imagebox = OffsetImage(Torre2, zoom=0.45)
        imagebox.image.axes = axes
        ab = AnnotationBbox(imagebox, [0.5, 0.45], frameon=False)
        axes.add_artist(ab)
        #Cargando imagen de torre 3:Meta
        Torre3 = plt.imread("./Hanoi/Torre.jpg")
        imagebox = OffsetImage(Torre3, zoom=0.45)
        imagebox.image.axes = axes
        ab = AnnotationBbox(imagebox, [0.82, 0.45], frameon=False)
        axes.add_artist(ab)
        #Posiciones de imagenes para x y y
        y_offset = [0.41, 0.345, 0.28]
        x_offset = [0.18, 0.5, 0.82]
        #Encontrando las posiciones de cada barra según el estado
        pos_barra_3 = np.where(estado==3)
        pos_barra_3_x = pos_barra_3[1][0]
        pos_barra_3_y = pos_barra_3[0][0]
        pos_barra_2 = np.where(estado==2)
        pos_barra_2_x = pos_barra_2[1][0]
        pos_barra_2_y = pos_barra_2[0][0]
        pos_barra_1 = np.where(estado==1)
        pos_barra_1_x = pos_barra_1[1][0]
        pos_barra_1_y = pos_barra_1[0][0]

        #Pintar las barras en sus respectivas posiciones
        barra3 = plt.imread("./Hanoi/barra3.jpg")
        imagebox = OffsetImage(barra3, zoom=0.4)
        y_offsets = [0.15, y_offset[pos_barra_3_y], 0.5, 0.5]
        imagebox.image.axes = axes
        ab = AnnotationBbox( imagebox, [x_offset[pos_barra_3_x], y_offsets[2-1]], frameon=False )
        axes.add_artist(ab)

        barra2 = plt.imread("./Hanoi/barra2.jpg")
        imagebox = OffsetImage(barra2, zoom=0.4)
        y_offsets = [0.15, y_offset[pos_barra_2_y], 0.1, 0.1]
        imagebox.image.axes = axes
        ab = AnnotationBbox(imagebox, [x_offset[pos_barra_2_x], y_offsets[2-1]], frameon=False)
        axes.add_artist(ab)

        barra1 = plt.imread("./Hanoi/barra1.jpg")
        imagebox = OffsetImage(barra1, zoom=0.4)
        y_offsets = [0.15, y_offset[pos_barra_1_y], 0.1, 0.1]
        imagebox.image.axes = axes
        ab = AnnotationBbox(imagebox, [x_offset[pos_barra_1_x], y_offsets[2-1]], frameon=False)
        axes.add_artist(ab)        
        axes.axis('off')
        return axes

    def pintar_camino(self, camino):
        # Input: lista con el camino de los estados
        # Output: plot con la forma de resolver las torres
        for estado in camino:
            clear_output(wait=True)
            self.pintar_estado(estado)
            plt.show()
            sleep(.5)

    def acciones_aplicables(self, estado):
        # Input: Estado matriz
        # Output: lista con 3 componentes: 1 el radio de la ficha a mover,
        # 2 la fila a que se debe mover, 3 la columna
        # Me paro en una columna y miro sus posibles acciones, si no encuentra
        # un elemento en la columna se puede mover, si encuentro un elemento
        # chequeo si el radio es mayor, en caso de que si lo muestra.
        posibles = list([])
        for i in [0,1,2] :
            for j in  list(set([0,1,2]) - set([i])):
                if min(estado[:,i]) < self.num_disc + 1 :
                    if min(estado[:,j]) == self.num_disc + 1:
                        pos = np.array([min(estado[:,i]),self.num_disc -1 , j])
                        posibles.append(list(pos))
                    elif min(estado[:,i]) < min(estado[:,j]):
                        x = np.where(estado ==  min(estado [:,j]) )
                        pos  = np.array([min(estado[:,i]), x[0][0]-1 ,x[1][0]])
                        posibles.append(list(pos))
        return posibles

    def transicion(self, estado, accion):
        # Input : estado matriz,  accion lista de 3
        # Output: estado matriz actualizado
        s = copy.deepcopy(estado)
        changue = accion[0]
        x = np.where(s == changue )
        s[x[0][0], x[1][0]] = self.num_disc + 1
        s[int(accion[1]), int(accion[2])] = accion [0]
        return s

    def test_objetivo(self,estado):
        # Input: estado matriz
        # Output: Verdadero Falso
        # El objetivo es pasar todos los discos a la última columna
        if sum(sum (estado == self.estado_objetivo)) == 3*self.num_disc:
            return True
        else:
            return False

    def costo(self, estado, accion):
        # El costo es igual a uno para minimizar el número de acciones
        return 1

    def codigo(self, estado):
        return '-'.join([str(i) for i in estado.flatten()])

class IndigenasEuropeos:
    '''
    @Autor: Germán Sarmiento Díaz
    '''
    def __init__(self, lado_1=None, lado_2=None, bote=None):
        if lado_1 is not None and lado_2 is not None:
            lado_1 = lado_1
            lado_2 = lado_2
        else:
            lado_1 = [-1, -1, -1, 1, 1, 1]
            lado_2 = []

        if bote is not None:
            bote = bote
        else:
            bote = [1, 0, 0]

        #Se crea un diccionario que representa el estado del problema, el cual consta de 3 listas.
        #1 lista que representa el lado 1.
        #1 lista que representa el lado 2.
        #1 lista que representa el lado/posición del bote y los pasajeros en el.
        self.estado_inicial = {
            'lado_1' : lado_1,
            'lado_2' : lado_2,
            'bote'   : bote
            }

    def acciones_aplicables(self, estado):
        # Devuelve una lista de los posibles movimientos a realizar a través del bote
		# desde el lado actual hacia el lado contrario
		# Input: estado. Diccionario con la representación del lado 1, lado 2 y el bote
		# Output: lista posibles valores que puede tomar el bote para realizar el movimiento.
        acciones = []
        estado_base = copy.deepcopy(estado) #Creamos un estado base el cual es una copia del estado actual.
                                    #Con esta copia armaremos las hipotesis de las acciones aplicables.

        lado_bote   = estado_base['bote'][0]
        bote = estado_base['bote']

        if lado_bote == 1:

            if bote[1] != 0:
                estado_base['lado_1'].append(bote[1]) #Suponemos que bajamos al lado 1 al pasajero del espacio 1.
                bote[1] = 0

            if bote[2] != 0:
                estado_base['lado_1'].append(bote[2]) #Suponemos que bajamos al lado 1 al pasajero del espacio 2.
                bote[2] = 0

            lado_1 = estado_base['lado_1']

            if 1 in lado_1 and -1 in lado_1:#Si existe al menos un Europeo y un Indígena
                accion = [2, 1, -1]
                if self.evaluar_accion(estado_base, accion):#Verificamos que la acción no cause que
                    #existan mas Europeos que Indígenas de cada lado al aplicarla, de ser verdadero, se agrega la accion.
                    acciones.append(accion)

            if 1 in lado_1:#Si existe un Indígena
                accion = [2, 1, 0]
                if self.evaluar_accion(estado_base, accion):
                    acciones.append(accion)

            if -1 in lado_1:#Si existe un Europeo
                accion = [2, -1, 0]
                if self.evaluar_accion(estado_base, accion):
                    acciones.append(accion)

            if lado_1.count(1) > 1:#Si existe mas de un Indígena
                accion = [2, 1, 1]
                if self.evaluar_accion(estado_base, accion):
                    acciones.append(accion)

            if lado_1.count(-1) > 1:#Si existe mas de un Europeo
                accion = [2, -1, -1]
                if self.evaluar_accion(estado_base, accion):
                    acciones.append(accion)
        else:

            if bote[1] != 0:
                estado_base['lado_2'].append(bote[1]) #Suponemos que bajamos al lado 2 al pasajero del espacio 1.
                bote[1] = 0

            if bote[2] != 0:
                estado_base['lado_2'].append(bote[2]) #Suponemos que bajamos al lado 2 al pasajero del espacio 2.
                bote[2] = 0

            lado_2 = estado_base['lado_2']

            if 1 in lado_2 and -1 in lado_2:#Si existe al menos un Europeo y un Indígena
                accion = [1, 1, -1]
                if self.evaluar_accion(estado_base, accion):#Verificamos que la acción no cause que
                    #existan mas Europeos que Indígenas de cada lado al aplicarla, de ser verdadero, se agrega la accion.
                    acciones.append(accion)

            if 1 in lado_2:#Si existe un Indígena
                accion = [1, 1, 0]
                if self.evaluar_accion(estado_base, accion):
                    acciones.append(accion)

            if -1 in lado_2:#Si existe un Europeo
                accion = [1, -1, 0]
                if self.evaluar_accion(estado_base, accion):
                    acciones.append(accion)

            if lado_2.count(1) > 1:#Si existe mas de un Indígena
                accion = [1, 1, 1]
                if self.evaluar_accion(estado_base, accion):
                    acciones.append(accion)

            if lado_2.count(-1) > 1:#Si existe mas de un Europeo
                accion = [1, -1, -1]
                if self.evaluar_accion(estado_base, accion):
                    acciones.append(accion)

            if len(estado_base['lado_1']) == 0:#Esta acción solo se da para bajare los posibles pasajeros del barco
                accion = [2, 0, 0]
                acciones.append(accion)

        return acciones

    def transicion(self, estado, accion):
        	# Devuelve el estado del problema con el lado 1 y lado 2 actualizado, aplicando la acción de entrada
		# Input: estado. Diccionario con la información del lado 1, lado2 my el bote
		#        accion. Dirección en la que se debe mover el bote y las personas que transporta
		# Output: accion, que es una casilla
        nuevo_estado = copy.deepcopy(estado)
        lado_1 = nuevo_estado['lado_1']
        lado_2 = nuevo_estado['lado_2']
        bote   = nuevo_estado['bote']

        if accion[0] == 1:#Se determina el lado en el que quedaría el bote
            #Se evaluan los dos puestos del bote para armar el estado hipotesis con sus respectivos lado_1 y lado_2
            if accion[1] == 1:#Si lleva un indígena en el puesto 1 del bote
                lado_2.pop(lado_2.index(1)) #Se extrae del lado 2
                lado_1.append(1)           #Se agrega al lado 1
            elif accion[1] == -1:#Si lleva un europeo en el puesto 1 del bote
                lado_2.pop(lado_2.index(-1)) #Se extrae del lado 2
                lado_1.append(-1)           #Se agrega al lado 1

            if accion[2] == 1:#Si lleva un indígena en el puesto 2 del bote
                lado_2.pop(lado_2.index(1)) #Se extrae del lado 2
                lado_1.append(1)           #Se agrega al lado 1
            elif accion[2] == -1:#Si lleva un europeo en el puesto 2 del bote
                lado_2.pop(lado_2.index(-1)) #Se extrae del lado 2
                lado_1.append(-1)           #Se agrega al lado 1
        else:
            #Se evaluan los dos puestos del bote para armar el estado hipotesis con sus respectivos lado_1 y lado_2
            if accion[1] == 1:#Si lleva un indígena en el puesto 1 del bote
                lado_1.pop(lado_1.index(1)) #Se extrae del lado 1
                lado_2.append(1)           #Se agrega al lado 2
            elif accion[1] == -1:#Si lleva un europeo en el puesto 1 del bote
                lado_1.pop(lado_1.index(-1)) #Se extrae del lado 1
                lado_2.append(-1)           #Se agrega al lado 2

            if accion[2] == 1:#Si lleva un indígena en el puesto 2 del bote
                lado_1.pop(lado_1.index(1)) #Se extrae del lado 1
                lado_2.append(1)           #Se agrega al lado 2
            elif accion[2] == -1:#Si lleva un europeo en el puesto 2 del bote
                lado_1.pop(lado_1.index(-1)) #Se extrae del lado 1
                lado_2.append(-1)           #Se agrega al lado 2

        lado_1.sort()
        lado_2.sort()
        bote[0] = accion[0]
        bote[1] = 0
        bote[2] = 0
        return nuevo_estado

    def test_objetivo(self, estado):
		# Devuelve True/False dependiendo si el estado resuelve el problema
		# Input: estado con la información del lado 1, lado 2 y el bote
		# Output: True/False
        lado_1_objetivo = []
        lado_2_objetivo = [-1, -1, -1, 1, 1, 1]
        bote_objetivo = [2, 0, 0]

        return (set(lado_1_objetivo) == set(estado['lado_1']) and
                set(lado_2_objetivo) == set(estado['lado_2']) and
                set(bote_objetivo)   == set(estado['bote'])
                )

    def costo(self, estado, accion):
        return 1

    def codigo(self, estado):
        s1 = 'L1<' + '/'.join(map(str, estado['lado_1'])) + '>'
        s2 = 'L2<' + '/'.join(map(str, estado['lado_2'])) + '>'
        s3 = 'B<'  + '/'.join(map(str, estado['bote']))   + '>'
        s4 = s1 + s2 + s3
        return s4

    def evaluar_accion(self, estado, accion):
        estado_hipotesis = copy.deepcopy(estado)
        lado_1 = estado_hipotesis['lado_1']
        lado_2 = estado_hipotesis['lado_2']
        suma_lado_1 = 0
        suma_lado_2 = 0
        if accion[0] == 1:#Se determina el lado en el que quedaría el bote
            #Se evaluan los dos puestos del bote para armar el estado hipotesis con sus respectivos lado_1 y lado_2
            if accion[1] == 1:#Si lleva un indígena en el puesto 1 del bote
                lado_2.pop(lado_2.index(1)) #Se extrae del lado 2
                lado_1.append(1)           #Se agrega al lado 1
            elif accion[1] == -1:#Si lleva un europeo en el puesto 1 del bote
                lado_2.pop(lado_2.index(-1)) #Se extrae del lado 2
                lado_1.append(-1)           #Se agrega al lado 1

            if accion[2] == 1:#Si lleva un indígena en el puesto 2 del bote
                lado_2.pop(lado_2.index(1)) #Se extrae del lado 2
                lado_1.append(1)           #Se agrega al lado 1
            elif accion[2] == -1:#Si lleva un europeo en el puesto 2 del bote
                lado_2.pop(lado_2.index(-1)) #Se extrae del lado 2
                lado_1.append(-1)           #Se agrega al lado 1
        else:
            #Se evaluan los dos puestos del bote para armar el estado hipotesis con sus respectivos lado_1 y lado_2
            if accion[1] == 1:#Si lleva un indígena en el puesto 1 del bote
                lado_1.pop(lado_1.index(1)) #Se extrae del lado 1
                lado_2.append(1)           #Se agrega al lado 2
            elif accion[1] == -1:#Si lleva un europeo en el puesto 1 del bote
                lado_1.pop(lado_1.index(-1)) #Se extrae del lado 1
                lado_2.append(-1)           #Se agrega al lado 2

            if accion[2] == 1:#Si lleva un indígena en el puesto 2 del bote
                lado_1.pop(lado_1.index(1)) #Se extrae del lado 1
                lado_2.append(1)           #Se agrega al lado 2
            elif accion[2] == -1:#Si lleva un europeo en el puesto 2 del bote
                lado_1.pop(lado_1.index(-1)) #Se extrae del lado 1
                lado_2.append(-1)           #Se agrega al lado 2

        #Se se evalua la regla restrictiva en cada lado si hay almenos un indígena en dicho lado.
        if 1 in lado_1:
            suma_lado_1 = sum(lado_1)

        if 1 in lado_2:
            suma_lado_2 = sum(lado_2)

        return suma_lado_1 >= 0 and suma_lado_2 >= 0

    def pintar_estado(self, estado):
        estado_actual = copy.deepcopy(estado)
        lado_1 = estado_actual['lado_1']
        lado_2 = estado_actual['lado_2']
        bote   = estado_actual['bote']

        fig, axes = plt.subplots(figsize=(9, 9))

        X, Y = (0.06,0)
        #Cargar imagen del bote
        arr_img = plt.imread("./Ind_y_Euro/bote.png", format='png')
        imagen_bote = OffsetImage(arr_img, zoom=0.15)
        imagen_bote.image.axes = axes
        #Cargar imagen de indígena
        arr_img = plt.imread("./Ind_y_Euro/indigena.png", format='png')
        imagen_indigena = OffsetImage(arr_img, zoom=0.30)
        imagen_indigena.image.axes = axes
        #Cargar imagen de europeo
        arr_img = plt.imread("./Ind_y_Euro/europeo.png", format='png')
        imagen_europeo = OffsetImage(arr_img, zoom=0.30)
        imagen_europeo.image.axes = axes
        #Cargar rio
        arr_img = plt.imread("./Ind_y_Euro/rio.png", format='png')
        imagen_rio = OffsetImage(arr_img, zoom=0.11)
        imagen_rio.image.axes = axes

        x = 0.03
        y = 0.30
        avance_y = 0.09
        #Pintar lado 1
        for l in lado_1:
            if l == 1:
                ab = AnnotationBbox(
		             imagen_indigena,
		             [x, y],
		             frameon=False)
                axes.add_artist(ab)
                y += avance_y
            else:
                ab = AnnotationBbox(
		             imagen_europeo,
		             [x, y],
		             frameon=False)
                axes.add_artist(ab)
                y += avance_y

        x = 0.97
        y = 0.30
        avance_y = 0.09
        #Pintar lado 2
        for l in lado_2:
            if l == 1:
                ab = AnnotationBbox(
		             imagen_indigena,
		             [x, y],
		             frameon=False)
                axes.add_artist(ab)
                y += avance_y
            else:
                ab = AnnotationBbox(
		             imagen_europeo,
		             [x, y],
		             frameon=False)
                axes.add_artist(ab)
                y += avance_y

        #Pintar bote
        if bote[0] == 1:
            x = 0.06
            y = 0.18
            ab = AnnotationBbox(
 		         imagen_bote,
 		         [x, y],
 		         frameon=False)
            axes.add_artist(ab)
        else:
            x = 0.94
            y = 0.18
            ab = AnnotationBbox(
 		         imagen_bote,
 		         [x, y],
 		         frameon=False)
            axes.add_artist(ab)

        #Pintar rio
        #Segmento 1
        x = 0.16
        y = 0.15
        ab = AnnotationBbox(
 		     imagen_rio,
 		     [x, y],
 		     frameon=False)
        axes.add_artist(ab)
        #--
        x = 0.20
        y = 0.10
        ab = AnnotationBbox(
 		     imagen_rio,
 		     [x, y],
 		     frameon=False)
        axes.add_artist(ab)
        #--
        x = 0.16
        y = 0.05
        ab = AnnotationBbox(
 		     imagen_rio,
 		     [x, y],
 		     frameon=False)
        axes.add_artist(ab)
        #--
        #Segmento 2
        x = 0.51
        y = 0.15
        ab = AnnotationBbox(
 		     imagen_rio,
 		     [x, y],
 		     frameon=False)
        axes.add_artist(ab)
        #--
        x = 0.55
        y = 0.10
        ab = AnnotationBbox(
 		     imagen_rio,
 		     [x, y],
 		     frameon=False)
        axes.add_artist(ab)
        #--
        x = 0.51
        y = 0.05
        ab = AnnotationBbox(
 		     imagen_rio,
 		     [x, y],
 		     frameon=False)
        axes.add_artist(ab)
        #--
        #Segmento 3
        x = 0.81
        y = 0.15
        ab = AnnotationBbox(
 		     imagen_rio,
 		     [x, y],
 		     frameon=False)
        axes.add_artist(ab)
        #--
        x = 0.85
        y = 0.10
        ab = AnnotationBbox(
 		     imagen_rio,
 		     [x, y],
 		     frameon=False)
        axes.add_artist(ab)
        #--
        x = 0.81
        y = 0.05
        ab = AnnotationBbox(
 		     imagen_rio,
 		     [x, y],
 		     frameon=False)
        axes.add_artist(ab)
        axes.axis('off')
        return axes

    def pintar_transicion(self, estado, accion):
        estado_actual = copy.deepcopy(estado)
        lado_1 = estado_actual['lado_1']
        lado_2 = estado_actual['lado_2']
        bote   = estado_actual['bote']
        if accion[0] == 1:#Se determina el lado en el que quedaría el bote
            #Se evaluan los dos puestos del bote para armar el estado hipotesis con sus respectivos lado_1 y lado_2
            if accion[1] == 1:#Si lleva un indígena en el puesto 1 del bote
                lado_2.pop(lado_2.index(1)) #Se extrae del lado 2
            elif accion[1] == -1:#Si lleva un europeo en el puesto 1 del bote
                lado_2.pop(lado_2.index(-1)) #Se extrae del lado 2

            if accion[2] == 1:#Si lleva un indígena en el puesto 2 del bote
                lado_2.pop(lado_2.index(1)) #Se extrae del lado 2
            elif accion[2] == -1:#Si lleva un europeo en el puesto 2 del bote
                lado_2.pop(lado_2.index(-1)) #Se extrae del lado 2
        else:
            #Se evaluan los dos puestos del bote para armar el estado hipotesis con sus respectivos lado_1 y lado_2
            if accion[1] == 1:#Si lleva un indígena en el puesto 1 del bote
                lado_1.pop(lado_1.index(1)) #Se extrae del lado 1
            elif accion[1] == -1:#Si lleva un europeo en el puesto 1 del bote
                lado_1.pop(lado_1.index(-1)) #Se extrae del lado 1

            if accion[2] == 1:#Si lleva un indígena en el puesto 2 del bote
                lado_1.pop(lado_1.index(1)) #Se extrae del lado 1
            elif accion[2] == -1:#Si lleva un europeo en el puesto 2 del bote
                lado_1.pop(lado_1.index(-1)) #Se extrae del lado 1

        paso = (0.84 - 0.16) / 10.0
        x_b = 0.0
        y_b = 0.18
        hacer_recorrido = True
        if bote[0] == 1 and accion[0] == 2:#Si el bote está en lado 1 y va al lado 2
            x_b = 0.16
        elif bote[0] == 2 and accion[0] == 1:#Si el bote está en el lado 2 y va al lado 1
            x_b = 0.84
            paso *= -1
        else:
            hacer_recorrido = False
        if hacer_recorrido:
            for i in range(10):
                clear_output(wait=True)
                fig, axes = plt.subplots(figsize=(9, 9))
                #Cargar imagen del bote
                arr_img = plt.imread("./Ind_y_Euro/bote.png", format='png')
                imagen_bote = OffsetImage(arr_img, zoom=0.15)
                imagen_bote.image.axes = axes
                #Cargar imagen de indígena
                arr_img = plt.imread("./Ind_y_Euro/indigena.png", format='png')
                imagen_indigena = OffsetImage(arr_img, zoom=0.30)
                imagen_indigena.image.axes = axes
                #Cargar imagen de europeo
                arr_img = plt.imread("./Ind_y_Euro/europeo.png", format='png')
                imagen_europeo = OffsetImage(arr_img, zoom=0.30)
                imagen_europeo.image.axes = axes
                #Cargar rio
                arr_img = plt.imread("./Ind_y_Euro/rio.png", format='png')
                imagen_rio = OffsetImage(arr_img, zoom=0.11)
                imagen_rio.image.axes = axes
                #Pintar rios
                #Pintar rio
                #Segmento 1
                x = 0.16
                y = 0.15
                ab = AnnotationBbox(
         		     imagen_rio,
         		     [x, y],
         		     frameon=False)
                axes.add_artist(ab)
                #--
                x = 0.20
                y = 0.10
                ab = AnnotationBbox(
         		     imagen_rio,
         		     [x, y],
         		     frameon=False)
                axes.add_artist(ab)
                #--
                x = 0.16
                y = 0.05
                ab = AnnotationBbox(
         		     imagen_rio,
         		     [x, y],
         		     frameon=False)
                axes.add_artist(ab)
                #--
                #Segmento 2
                x = 0.51
                y = 0.15
                ab = AnnotationBbox(
         		     imagen_rio,
         		     [x, y],
         		     frameon=False)
                axes.add_artist(ab)
                #--
                x = 0.55
                y = 0.10
                ab = AnnotationBbox(
         		     imagen_rio,
         		     [x, y],
         		     frameon=False)
                axes.add_artist(ab)
                #--
                x = 0.51
                y = 0.05
                ab = AnnotationBbox(
         		     imagen_rio,
         		     [x, y],
         		     frameon=False)
                axes.add_artist(ab)
                #--
                #Segmento 3
                x = 0.81
                y = 0.15
                ab = AnnotationBbox(
         		     imagen_rio,
         		     [x, y],
         		     frameon=False)
                axes.add_artist(ab)
                #--
                x = 0.85
                y = 0.10
                ab = AnnotationBbox(
         		     imagen_rio,
         		     [x, y],
         		     frameon=False)
                axes.add_artist(ab)
                #--
                x = 0.81
                y = 0.05
                ab = AnnotationBbox(
         		     imagen_rio,
         		     [x, y],
         		     frameon=False)
                axes.add_artist(ab)
                #Pintar lados:
                x = 0.03
                y = 0.30
                avance_y = 0.09
                #Pintar lado 1
                for l in lado_1:
                    if l == 1:
                        ab = AnnotationBbox(
        		             imagen_indigena,
        		             [x, y],
        		             frameon=False)
                        axes.add_artist(ab)
                        y += avance_y
                    else:
                        ab = AnnotationBbox(
        		             imagen_europeo,
        		             [x, y],
        		             frameon=False)
                        axes.add_artist(ab)
                        y += avance_y

                x = 0.97
                y = 0.30
                avance_y = 0.09
                #Pintar lado 2
                for l in lado_2:
                    if l == 1:
                        ab = AnnotationBbox(
        		             imagen_indigena,
        		             [x, y],
        		             frameon=False)
                        axes.add_artist(ab)
                        y += avance_y
                    else:
                        ab = AnnotationBbox(
        		             imagen_europeo,
        		             [x, y],
        		             frameon=False)
                        axes.add_artist(ab)
                        y += avance_y
                #Bote

                if accion[1] == 1:
                    ab = AnnotationBbox(
    		         imagen_indigena,
 	     	         [x_b - 0.03, y_b + 0.05],
 		             frameon=False)
                    axes.add_artist(ab)
                elif accion[1] == -1:
                    ab = AnnotationBbox(
    		         imagen_europeo,
 	     	         [x_b - 0.03, y_b + 0.05],
 		             frameon=False)
                    axes.add_artist(ab)

                if accion[2] == 1:
                    ab = AnnotationBbox(
    		         imagen_indigena,
 	     	         [x_b + 0.03, y_b + 0.05],
 		             frameon=False)
                    axes.add_artist(ab)
                elif accion[2] == -1:
                    ab = AnnotationBbox(
    		         imagen_europeo,
 	     	         [x_b + 0.03, y_b + 0.05],
 		             frameon=False)
                    axes.add_artist(ab)

                ab = AnnotationBbox(
 		         imagen_bote,
 		         [x_b, y_b],
 		         frameon=False)
                axes.add_artist(ab)

                x_b += paso
                axes.axis('off')
                plt.show()
                sleep(.05)
        else:
            x = 0.00
            y = 0.30
            avance_y = 0.09
            #Pintar lado 1
            for l in lado_1:
                if l == 1:
                    ab = AnnotationBbox(
    		             imagen_indigena,
    		             [x, y],
    		             frameon=False)
                    axes.add_artist(ab)
                    y += avance_y
                else:
                    ab = AnnotationBbox(
    		             imagen_europeo,
    		             [x, y],
    		             frameon=False)
                    axes.add_artist(ab)
                    y += avance_y

            x = 1.00
            y = 0.30
            avance_y = 0.09
            #Pintar lado 2
            for l in lado_2:
                if l == 1:
                    ab = AnnotationBbox(
    		             imagen_indigena,
    		             [x, y],
    		             frameon=False)
                    axes.add_artist(ab)
                    y += avance_y
                else:
                    ab = AnnotationBbox(
    		             imagen_europeo,
    		             [x, y],
    		             frameon=False)
                    axes.add_artist(ab)
                    y += avance_y

        axes.axis('off')
        return axes

    def pintar_camino(self, estados, acciones):
        na = len(acciones)
        i = 0
        for e in estados:
            clear_output(wait=True)
            self.pintar_estado(e)
            plt.show()
            sleep(.25)
            if na > 0:
                clear_output(wait=True)
                self.pintar_transicion(e, acciones[i])
                i += 1
                na -= 1

class nsquare_horses:
    '''
    @Autores: Oscar Velazco y Juan David Rojas
    '''

    def __init__(self, n = 8, m = 8, pos = None):
        self.n = n
        self.m = m
        if(pos == None):
            fil = rd.randint(1, self.n)
            col = rd.randint(1, self.m)
            pos = (fil, col)
        self.estado_inicial = np.matrix([[0] * self.m] * self.n)
        self.estado_inicial[pos[0] - 1, pos[1] - 1] = 1
        self.pos_inicial = pos


    def pintar_estado(self, estado):
        fig, axes = plt.subplots()
        fig.set_size_inches(self.m, self.n)
        step = 1. / self.n
        offset = 0.001
        tangulos = []
        a = 0.998 if(self.n == self.m) else min([self.n, self.m]) / max([self.n, self.m]) - 0.002
        tangulos.append(patches.Rectangle((0, 0), a, 0.998, \
        facecolor = 'cornsilk', edgecolor = 'black', linewidth = 2))
        u = self.n // 2 if self.n % 2 == 0 else self.n // 2 + 1 # Filas par o impar
        v = self.m // 2 if self.m % 2 == 0 else self.m // 2 + 1 # Columnas par o impar
        for i in range(u):
            for j in range(v):
                tangulos.append(patches.Rectangle((2 * i * step, 2 * j * step), \
                                                  step - offset, step, \
                                                  facecolor = 'lightslategrey', \
                                                  ec = 'k', lw = 3))
                tangulos.append(patches.Rectangle((step + 2 * i * step, (2 * j + 1) * step), \
                                                  step - offset, step, \
                                                  facecolor = 'lightslategrey', \
                                                  ec = 'k', lw = 3))
        for t in tangulos:
            axes.add_patch(t)
        #arr_img = plt.imread('caballo.png', format = 'png')
        #zooms = []
        #imagebox = OffsetImage(arr_img, zoom = 0.1)
        #imagebox.image.axes = axes
        offsetX = 0.065
        offsetY = 0.065
        for i in range(1, self.m + 1):
            for j in range(1, self.n + 1):
                if(estado[j - 1, i - 1] >= 1):
                    Y = self.n - j
                    X = i - 1
                    axes.text(X * step + step / 2, Y * step + step / 2, estado[j - 1, i - 1], \
                              ha = "center", va = "center", size = 30, c = 'k')
        axes.set_xlim(0, a + 0.002)
        axes.set_ylim(0, 1)
        axes.axis('off')
        # axes.set_zorder(1)
        # fig.savefig("tablero" + str(self.n) + "x" + str(self.m) + ".png")
        return axes

    def pintar_camino(self, camino):
        # Input: lista con el camino de los estados
        # Output: plot con la forma de resolver las torres
        for estado in camino:
            clear_output(wait=True)
            self.pintar_estado(estado)
            plt.show()
            sleep(.5)

    def valida(self, posicion, estado):
        if (posicion[0] > -1) & (posicion[0] < self.n) & (posicion[1] > -1) & (posicion[1] < self.m):
            if(estado[posicion[0], posicion[1]] == 0):
                return True
        return False

    def acciones_aplicables(self, estado):
        # Devuelve una lista con las posiciones en las cuales se puede mover
        # Input: estado, que es una np.matrix(nxn)
        # Output: lista de parejas (x1,y1) donde puede hacer el siguiente movimiento el caballo
        # posición del último caballo
        i,j = np.unravel_index(np.argmax(estado, axis=None), estado.shape)
        # recorrer todas las direcciones posibles y ver si no se han recorrido
        direcciones = np.array([[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [-1, 2], [1, -2], [-1, -2]])
        acciones = [(posicion[0], posicion[1]) for posicion in direcciones + [i, j] if self.valida(posicion, estado)]
        return acciones

    def transicion(self, estado, indice):
        # Devuelve el tablero colocando el caballo en la posición dada por indice
        # Input: estado, que es una np.matrix(nxn)
        #        indice, de la forma (x1,y1)
        # Output: estado, que es una np.matrix(nxn)
        s = copy.deepcopy(estado)
        s[indice[0], indice[1]] = np.max(estado) + 1
        return s

    def test_objetivo(self, estado):
        # Devuelve True/False dependiendo si el estado
        # resuelve el problema
        # Input: estado, que es una np.matrix(nxn)
        # Output: True/False
        # Decide si las entradas en la matriz son n*m números diferentes de 0.




        return len(set(np.array(np.unique((np.array(estado)).reshape(-1)))).difference({0})) == (self.n * self.m)

    def costo(self, estado, accion):
        s = copy.deepcopy(estado)
        s[accion[0], accion[1]] = np.max(estado) + 1
        return len(self.acciones_aplicables(s))

    def codigo(self, estado):
        return str(estado)

class BlockWorld:
    '''
    @Autores: Santiago Álvarez y María Fernanda Palacio
    '''
    def __init__(self, num_de_blocks=5, default=True):
        assert(num_de_blocks <= 10)
        self.num_de_blocks = num_de_blocks
        s = np.matrix([[0] * num_de_blocks] * num_de_blocks)
        u = np.matrix([[0] * num_de_blocks] * num_de_blocks)
        if default:
            s = self.transicion_inicial(s, (0, 4), 4)
            s = self.transicion_inicial(s, (0, 3), 1)
            s = self.transicion_inicial(s, (3, 4), 2)
            s = self.transicion_inicial(s, (2, 4), 3)
            s = self.transicion_inicial(s, (2, 3), 5)
            u = self.transicion_final(u, (0, 4), 3)
            u = self.transicion_final(u, (1, 4), 1)
            u = self.transicion_final(u, (0, 3), 2)
            u = self.transicion_final(u, (0, 2), 5)
            u = self.transicion_final(u, (4, 4), 4)
        self.estado_inicial = s
        self.estado_final = u

    def pintar_estado(self, estado):
        # Dibuja el mundo correspondiente al estado
        # Input: estado, que es una num_de_blocks-lista de num_de_blocks-listas
        n = len(estado)
        fig, axes = plt.subplots()

        # Dibujo el tablero
        step = 1.0 / n
        offset = 0.001
        tangulos = []

        # Borde del tablero
        tangulos.append(
            patches.Rectangle(
                (0, 0),
                0.998,
                0.998,
                facecolor="white",
                edgecolor="white",
                linewidth=2,
            )
        )

        # Creo las líneas del tablero, AL FINAL ESTO PODRIA ELIMINARSE
        for j in range(n):
            locacion = 0.0
            # Crea linea horizontal en el rectangulo
            tangulos.append(
                patches.Rectangle(*[(0, locacion), 1, 0.008], facecolor="black")
            )

        for t in tangulos:
            axes.add_patch(t)

        # Cargando imagenes de los bloques
        arr_img = Image.open("./BlockWorld/BloqueA.png")
        arr_img_2 = Image.open("./BlockWorld/BloqueB.png")
        arr_img_3 = Image.open("./BlockWorld/BloqueC.png")
        arr_img_4 = Image.open("./BlockWorld/BloqueD.png")
        arr_img_5 = Image.open("./BlockWorld/BloqueE.png")
        arr_img_6 = Image.open("./BlockWorld/BloqueF.png")
        arr_img_7 = Image.open("./BlockWorld/BloqueG.png")
        arr_img_8 = Image.open("./BlockWorld/BloqueH.png")
        arr_img_9 = Image.open("./BlockWorld/BloqueI.png")
        arr_img_10 = Image.open("./BlockWorld/BloqueJ.png")
        base_x = 335
        base_y = 220
        arr_img = arr_img.resize((int(base_x / n), int(base_y / n)))
        arr_img_2 = arr_img_2.resize((int(base_x / n), int(base_y / n)))
        arr_img_3 = arr_img_3.resize((int(base_x / n), int(base_y / n)))
        arr_img_4 = arr_img_4.resize((int(base_x / n), int(base_y / n)))
        arr_img_5 = arr_img_5.resize((int(base_x / n), int(base_y / n)))
        arr_img_6 = arr_img_6.resize((int(base_x / n), int(base_y / n)))
        arr_img_7 = arr_img_7.resize((int(base_x / n), int(base_y / n)))
        arr_img_8 = arr_img_8.resize((int(base_x / n), int(base_y / n)))
        arr_img_9 = arr_img_9.resize((int(base_x / n), int(base_y / n)))
        arr_img_10 = arr_img_10.resize((int(base_x / n), int(base_y / n)))
        imagebox = OffsetImage(arr_img)
        imagebox2 = OffsetImage(arr_img_2)
        imagebox3 = OffsetImage(arr_img_3)
        imagebox4 = OffsetImage(arr_img_4)
        imagebox5 = OffsetImage(arr_img_5)
        imagebox6 = OffsetImage(arr_img_6)
        imagebox7 = OffsetImage(arr_img_7)
        imagebox8 = OffsetImage(arr_img_8)
        imagebox9 = OffsetImage(arr_img_9)
        imagebox10 = OffsetImage(arr_img_10)
        imagebox.image.axes = axes
        imagebox2.image.axes = axes
        imagebox3.image.axes = axes
        imagebox4.image.axes = axes
        imagebox5.image.axes = axes
        imagebox6.image.axes = axes
        imagebox7.image.axes = axes
        imagebox8.image.axes = axes
        imagebox9.image.axes = axes
        imagebox10.image.axes = axes
        offsetX = step / 1.975
        offsetY = step / 1.975
        for i in range(n):
            for j in range(n):
                if estado[j, i] == 1:
                    Y = (n - 1) - j
                    X = i
                    ab = AnnotationBbox(
                        imagebox,
                        [(X * step) + offsetX, (Y * step) + offsetY],
                        frameon=False,
                    )
                    axes.add_artist(ab)
                elif estado[j, i] == 2:
                    Y = (n - 1) - j
                    X = i
                    ab = AnnotationBbox(
                        imagebox2,
                        [(X * step) + offsetX, (Y * step) + offsetY],
                        frameon=False,
                    )
                    axes.add_artist(ab)
                elif estado[j, i] == 3:
                    Y = (n - 1) - j
                    X = i
                    ab = AnnotationBbox(
                        imagebox3,
                        [(X * step) + offsetX, (Y * step) + offsetY],
                        frameon=False,
                    )
                    axes.add_artist(ab)
                elif estado[j, i] == 4:
                    Y = (n - 1) - j
                    X = i
                    ab = AnnotationBbox(
                        imagebox4,
                        [(X * step) + offsetX, (Y * step) + offsetY],
                        frameon=False,
                    )
                    axes.add_artist(ab)
                elif estado[j, i] == 5:
                    Y = (n - 1) - j
                    X = i
                    ab = AnnotationBbox(
                        imagebox5,
                        [(X * step) + offsetX, (Y * step) + offsetY],
                        frameon=False,
                    )
                    axes.add_artist(ab)
                elif estado[j, i] == 6:
                    Y = (n - 1) - j
                    X = i
                    ab = AnnotationBbox(
                        imagebox6,
                        [(X * step) + offsetX, (Y * step) + offsetY],
                        frameon=False,
                    )
                    axes.add_artist(ab)
                elif estado[j, i] == 7:
                    Y = (n - 1) - j
                    X = i
                    ab = AnnotationBbox(
                        imagebox7,
                        [(X * step) + offsetX, (Y * step) + offsetY],
                        frameon=False,
                    )
                    axes.add_artist(ab)
                elif estado[j, i] == 8:
                    Y = (n - 1) - j
                    X = i
                    ab = AnnotationBbox(
                        imagebox8,
                        [(X * step) + offsetX, (Y * step) + offsetY],
                        frameon=False,
                    )
                    axes.add_artist(ab)
                elif estado[j, i] == 9:
                    Y = (n - 1) - j
                    X = i
                    ab = AnnotationBbox(
                        imagebox9,
                        [(X * step) + offsetX, (Y * step) + offsetY],
                        frameon=False,
                    )
                    axes.add_artist(ab)
                elif estado[j, i] == 10:
                    Y = (n - 1) - j
                    X = i
                    ab = AnnotationBbox(
                        imagebox10,
                        [(X * step) + offsetX, (Y * step) + offsetY],
                        frameon=False,
                    )
                    axes.add_artist(ab)

        axes.axis("off")
        return axes

    def pintar_camino(self, camino):
        # Input: lista con el camino de los estados
        # Output: plot con la forma de resolver las torres
        for estado in camino:
            clear_output(wait=True)
            self.pintar_estado(estado)
            plt.show()
            sleep(.5)

    def acciones_aplicables(self, estado):
        # Devuelve una lista de parejas que representan
        # las casillas vacías en las que es permitido
        # poner un bloque.
        # Input: estado, que es una np.matrix(8x8)
        # Output: lista de indices (x,y),(z,w) es decir,
        # el bloque en la posicion (x,y) puede moverse a la posición (z,w)
        # print("--- IN ACCIONES_APLICABLES ---")
        n = len(estado)
        indices_bloqueados = []
        for x in range(n):
            for y in range(n):
                if estado[y, x] != 0:
                    indices_bloqueados.append((x, y))
        casillas_piso = []
        for i in range(n):
            casillas_piso.append((i, n - 1))
        casillas_libres = []
        for i in indices_bloqueados:
            casillas_libres.append((i[0], i[1] - 1))
        # casillas_libres.remove((block[0], block[1] - 1))

        for i in casillas_piso:
            casillas_libres.append(i)

        casillas_libres = [x for x in casillas_libres if x not in indices_bloqueados]
        for i in casillas_libres:
            if i < (0, 0):
                casillas_libres.remove(i)

        casillas_encerradas = []
        for i in indices_bloqueados:
            if (i[0], i[1] - 1) in indices_bloqueados:
                casillas_encerradas.append(i)

        bloques_validos = [
            x for x in indices_bloqueados if x not in casillas_encerradas
        ]

        new_pos = []
        for i in bloques_validos:
            for j in casillas_libres:
                if j != (i[0], i[1] - 1):
                    new_pos.append((i, j))

        return new_pos

    def transicion(self, estado, indices):
        # Devuelve el tablero incluyendo un bloque en el indice
        # Input: estado, que es una np.matrix(8x8)
        #        indice, de la forma (x,y)
        # Output: estado, que es una np.matrix(8x8)
        # print("--- IN TRANSICION ---")
        s = copy.deepcopy(estado)
        x1, y1 = indices[0]
        x2, y2 = indices[1]
        s[y2, x2] = estado[y1, x1]
        s[y1, x1] = 0
        return s

    def transicion_inicial(self, estado, indices, valor):
        # Devuelve el tablero incluyendo una reina en el indice
        # Input: estado, que es una np.matrix(8x8)
        #        indice, de la forma (x,y)
        #        valor, valor numerico que representa el peso del bloque (A:1,B:2,C:3 etc.)
        # Output: estado, que es una np.matrix(8x8)
        # print("--- IN TRANSICION INICIAL---")
        n = len(estado)
        s = copy.deepcopy(estado)
        x = indices[0]
        y = indices[1]

        piso = []
        for i in range(n):
            piso.append((i, n - 1))

        if indices in piso:
            s[y, x] = valor
        elif s[y + 1, x] != 0:
            s[y, x] = valor
        else:
            raise ValueError("No se puede poner un bloque aqui!")
        return s

    def transicion_final(self, estado, indices, valor):
        # Devuelve el tablero incluyendo un bloque en el indice
        # Input: estado, que es una np.matrix(8x8)
        #        indice, de la forma (x,y)
        #        valor, valor numerico que representa el peso del bloque (A:1,B:2,C:3 etc.)
        # Output: estado, que es una np.matrix(8x8)
        # print("--- IN TRANSICION FINAL---")
        n = len(estado)
        s = copy.deepcopy(estado)
        x = indices[0]
        y = indices[1]

        piso = []
        for i in range(n):
            piso.append((i, n - 1))

        if indices in piso:
            s[y, x] = valor
        elif s[y + 1, x] != 0:
            s[y, x] = valor
        else:
            raise ValueError("No se puede poner un bloque aqui!")
        return s

    def test_objetivo(self, estado):
        # Devuelve True/False dependiendo si el estado
        # resuelve el problema o si no
        # Input: estado, que es una np.matrix(8x8)
        # Output: True/False
        # print("--- IN TEST_OBJETIVO ---")
        # print("Determinando si los bloques estan en forma del estado final")
        return (estado == self.estado_final).all()

    def codigo(self, estado):
        inicial = True
        for i in estado:
            for j in i:
                if inicial:
                    cadena = str(j)
                    inicial = False
                else:
                    cadena += "-" + str(j)
        return cadena

    def costo(self, estado, accion):
        return 1

class Vendedor:
    '''
    @Autores: Daniel Forero y Andres Felipe Florián
    '''
    """ Clase Vendedor representa las posibles acciones que puede realizar el vendedor y
        si el objetivo se cumplió o no
            Atributos: -estado_inicial: Localidad de partida
                       -rutas: Diccionario con el peso entre cada desplazamiento entre localidades.
                       -localidades
                       -G: Objeto de networkx para graficar la representacion inicial
    """
    def __init__(self, localidad):
        self.estado_inicial = [localidad]
        self.rutas = {'Usaquen':{'Chapinero':7.5, 'Santa Fe':11.6, 'San Cristobal':23, 'Usme':30, 'Tunjuelito':22.2, 'Bosa':24.8, 'Kennedy':21.1, 'Fontibon':21.1, 'Engativa':10.9, 'Suba':7.1, 'Barrios Unidos':8.8},\
                    'Chapinero':{'Usaquen':7.5, 'Santa Fe':6.2, 'San Cristobal':13.9, 'Usme':26.2, 'Tunjuelito':18.1, 'Bosa':20.3, 'Kennedy':14.8, 'Fontibon':15.2, 'Engativa':10.5, 'Suba':9.8, 'Barrios Unidos':4.6},\
                    'Santa Fe':{'Chapinero':6.2, 'Usaquen':11.6, 'San Cristobal':7.7, 'Usme':18.3, 'Tunjuelito':12, 'Bosa':14.6, 'Kennedy':10.3, 'Fontibon':12.1, 'Engativa':18.4, 'Suba':15.6, 'Barrios Unidos':9.3},\
                    'San Cristobal':{'Chapinero':13.9, 'Usaquen':23, 'Santa Fe':7.7, 'Usme':10.2, 'Tunjuelito':9.4, 'Bosa':13.9, 'Kennedy':11.2, 'Fontibon':17.4, 'Engativa':23.6, 'Suba':22.8, 'Barrios Unidos':15.6},\
                    'Usme':{'Chapinero':26.2, 'Usaquen':30, 'Santa Fe':18.3, 'San Cristobal':10.2, 'Tunjuelito':10.3, 'Bosa':16.1, 'Kennedy':15, 'Fontibon':21.5, 'Engativa':28.7, 'Suba':27.8, 'Barrios Unidos':24.4},\
                    'Tunjuelito':{'Chapinero':18.1, 'Usaquen':22.2, 'Santa Fe':12, 'San Cristobal':9.4, 'Usme':10.3, 'Bosa':7.7, 'Kennedy':7.4, 'Fontibon':13.9, 'Engativa':21.1, 'Suba':20.2, 'Barrios Unidos':16},\
                    'Bosa':{'Chapinero':20.3, 'Usaquen':24.8, 'Santa Fe':14.6, 'San Cristobal':13.9, 'Usme':16.1, 'Tunjuelito':7.7, 'Kennedy':7, 'Fontibon':11.1, 'Engativa':20.1, 'Suba':19.1, 'Barrios Unidos':16.8},\
                    'Kennedy':{'Chapinero':14.8, 'Usaquen':21.1, 'Santa Fe':10.3, 'San Cristobal':11.2, 'Usme':15, 'Tunjuelito':7.4, 'Bosa':7, 'Fontibon':6.5, 'Engativa':13.8, 'Suba':12.8, 'Barrios Unidos':11.3},\
                    'Fontibon':{'Chapinero':15.2, 'Usaquen':21.1, 'Santa Fe':12.1, 'San Cristobal':17.4, 'Usme':21.5, 'Tunjuelito':13.9, 'Bosa':11.1, 'Kennedy':6.5, 'Engativa':11, 'Suba':14.5, 'Barrios Unidos':13.1},\
                    'Engativa':{'Chapinero':10.5, 'Usaquen':10.9, 'Santa Fe':18.4, 'San Cristobal':23.6, 'Usme':28.7, 'Tunjuelito':21.1, 'Bosa':20.1, 'Kennedy':13.8, 'Fontibon':11, 'Suba':7, 'Barrios Unidos':6.9},\
                    'Suba':{'Chapinero':9.8, 'Usaquen':7.1, 'Santa Fe':15.6, 'San Cristobal':22.8, 'Usme':27.8, 'Tunjuelito':20.2, 'Bosa':19.1, 'Kennedy':12.8, 'Fontibon':14.5, 'Engativa':7, 'Barrios Unidos':10.4},\
                    'Barrios Unidos':{'Chapinero':4.6, 'Usaquen':8.8, 'Santa Fe':9.3, 'San Cristobal':15.6, 'Usme':24.4, 'Tunjuelito':16, 'Bosa':16.8, 'Kennedy':11.3, 'Fontibon':13.1, 'Engativa':6.9, 'Suba':10.4}}
        self.coords = {'Usaquen':(1,14), 'Chapinero':(6,13), 'Santa Fe':(8,16), 'San Cristobal':(10,11), 'Usme':(15,8), 'Tunjuelito':(9,3), 'Bosa':(7,0), 'Kennedy':(6,2), 'Fontibon':(4,4), 'Engativa':(3,6), 'Suba':(0,10), 'Barrios Unidos':(5,11)}
        self.localidades = list(self.rutas.keys())
        self.G = None

    def pintar_estado(self, estado):
        """ Creacion y plot del grafo como vertices las localidades y pesos el valor de la distancia entre cada para de localidades """
        self.G = nx.Graph()
        n = len(estado)
        for i in range(n):
            x, y = self.coords[estado[i]]
            self.G.add_node(estado[i], pos = (x,y))
        for i in range(n-1):
            self.G.add_edge(estado[i], estado[i+1], weight = self.rutas[estado[i]][estado[i+1]])
        pos = nx.get_node_attributes(self.G, 'pos')
        pesos = nx.get_edge_attributes(self.G,'weight')
        plt.figure(figsize=(12,12))
        nx.draw_networkx(self.G, pos)
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels = pesos)
        plt.show()

    def pintar_camino(self, camino):
        # Input: lista con el camino de los estados
        # Output: plot con la forma de resolver las torres
        for estado in camino:
            clear_output(wait=True)
            self.pintar_estado(estado)
            plt.show()
            sleep(.5)

    def acciones_aplicables(self, estado):
        """ Retorna las posibles acciones dado el estado
            Input: estado (localidad)
            Output: Lista con las localidades no visitadas
        """
        return [x for x in self.localidades if x not in estado]

    def transicion(self, estado, accion):
        """ Retorna la lista actualizada con la accion realizada
            Input: estado (lista con el camino en el momento)
                   accion (desplazamiento)
            Output: Copia de la lista estado actualizada """
        lista = copy.deepcopy(estado)
        lista.append(accion)
        return lista

    def test_objetivo(self, estado):
        """ Verifica si ya fueron visitadas todas las localidades
            Input: estado (lista con el camino)
            Output: Boolean """
        return set(self.localidades) == set(estado)

    def codigo(self, estado):
        """ Actualiza el codigo
            Input: estado (lista con el camino)
            Output: cadena """
        cad = ""
        for i in estado:
            cad = cad + " - " + i
        return cad

    def costo(self, estado1, estado2):
        """ Peso entre el estado y la accion
            Input: estado (camino actual)
                   accion (desplazamiento)
            Output: Int """
        loc = self.rutas[estado1[-1]]
        return loc[estado2]

    def obtener_peso(self, estado1, estado2):
        """ Retorna el peso entre dos localidades
            Input: estado1, estado2, localidades
            Output: Int, distancia entre ambas localidades"""
        loc = self.rutas[estado1]
        return loc[estado2]

class CriptoAritmetica():
    '''
    @Autores: Jessenia Piza y Laura Zalazar
    '''
    def __init__(self, lista_palabras):
        self.palabras = lista_palabras
        self.lista_letras = [letra for palabra in self.palabras for letra in palabra ]
        self.lista_letras = list(set(self.lista_letras))
        self.estado_inicial = {letra:None for letra in self.lista_letras}
        self.letras_iniciales = list(set(palabra[0] for palabra in self.palabras))

    def pintar_estado(self, estado):
        # Dibuja el problema inicial, el estado del que se habla (ya sea la solución o no) y devuelve el resultado de la operación.
        # Input: Estado - diccionario con el estado de las letras del problema.
        fig, axes = plt.subplots(figsize=(5,len(self.palabras)))
        white = np.ones((100, 100), dtype=np.float)
        list_len = [len(palabra) for palabra in self.palabras]

        plt.text(0.2, 1.5, 'Problema inicial', fontsize = 20, color = 'blue')
        plt.text(1.5, 1.5, 'Estado', fontsize = 20, color = 'blue')
        plt.text(2.5, 1.5, 'Resultado', fontsize = 20, color = 'blue')
        plt.text(0, 1.3, '----------------------------------------------------------------------------------------------------------------------------', fontsize = 20, color = 'blue')

        for i in range(len(self.palabras)):
            if i == len(self.palabras) - 2:
                plt.text(0.2, (len(self.palabras)-i)/len(self.palabras), f"+      {self.palabras[i]}", fontsize = 20)
                plt.text(0.2, 3/2*1/len(self.palabras), '----------------', fontsize = 20)
            else:
                plt.text(0.4, (len(self.palabras)-i)/len(self.palabras), self.palabras[i], fontsize = 20)

        q = 0
        for est in estado:
            plt.text(1.4, (len(estado)-q)/len(estado), '|', fontsize = 20, color = 'blue')
            plt.text(1.5, (len(estado)-q)/len(estado), est, fontsize = 20)
            plt.text(1.6, (len(estado)-q)/len(estado), '|', fontsize = 20, color = 'blue')
            plt.text(1.8, (len(estado)-q)/len(estado), '|', fontsize = 20, color = 'blue')
            if estado[est] == None:
                plt.text(1.7, (len(estado)-q)/len(estado), '-', fontsize = 20)
            else:
                plt.text(1.7, (len(estado)-q)/len(estado), str(estado[est]), fontsize = 20)
            q += 1

        if self.test_objetivo(estado):
            for i in range(len(self.palabras_sol)):
                if i == len(self.palabras_sol) - 2:
                    plt.text(2.5, (len(self.palabras_sol)-i)/len(self.palabras_sol), f"+      {self.palabras_sol[i]}", fontsize = 20)
                    plt.text(2.5, 3/2*1/len(self.palabras_sol), '----------------', fontsize = 20)
                else:
                    plt.text(2.7, (len(self.palabras_sol)-i)/len(self.palabras_sol), str(self.palabras_sol[i]), fontsize = 20)
        else:
            plt.text(2.5, 1, "El estado no es", fontsize = 20)
            plt.text(2.3, 0.7, "una solución al problema.", fontsize = 20)

        axes.axis('off')

        return axes

    def pintar_camino(self, camino):
        # Input: lista con el camino de los estados
        # Output: plot con la forma de resolver las torres
        for estado in camino:
            clear_output(wait=True)
            self.pintar_estado(estado)
            plt.show()
            sleep(.5)

    def transicion(self, estado, accion):
        # Dada una acción se cambia el estado del problema.
        # Input: acción - Dupla con la letra y el valor que se desea cambiar en el diccionario.
        # Output: Estado que es un diccionario.
        estado_copy = copy.deepcopy(estado)
        estado_copy[accion[0]] = accion[1]
        return estado_copy

    def acciones_aplicables(self, estado):
        # Devuelve una lista de tuplas que representan
        # la acción permitida, de acuerdo a la codificación
        # presentada en al formalización del problema más arriba.
        # Input: Estado - diccionario con el estado de las letras del problema.
        # Output: acciones - Lista de tuplas.
        digitos_disponibles = [d for d in range(10) if d not in estado.values()]
        letras_disponibles = [d for d in self.lista_letras if estado[d] == None]
        acciones = list(product(letras_disponibles, digitos_disponibles))
        for letra in self.letras_iniciales:
            if (letra, 0) in acciones:
                acciones.remove((letra, 0))
        return acciones

    def test_objetivo(self, estado):
        # Devuelve True/False dependiendo si el estado
        # resuelve el problema
        # Input: estado - diccionario de las letras con sus respectivos valores.
        # Output: True/False

        self.palabras_sol = []
        for palabra in self.palabras:
            for letra in palabra:
                palabra = palabra.replace(letra, str(estado[letra]))
            try:
                num_palabra = int(palabra)
                self.palabras_sol.append(num_palabra)
            except:
                return False
        return np.sum(self.palabras_sol[:-1]) == self.palabras_sol[-1]

    def sol_algoritmo(self):
        # Resuelve el problema criptoaritmético tomando todas las posibles permutaciones
        # que tienen los digitos del 0 al 9 con las letras del problema.
        # Output: solucion si existe, else None.
        digitos = range(10)
        for permutacion in permutations(digitos, len(self.lista_letras)):
            solucion = dict(zip(self.lista_letras, permutacion))
            if any(solucion[letra]==0 for letra in self.letras_iniciales):
                continue
            if self.test_objetivo(solucion):
                return solucion
        return None

    def codigo(self, estado):
        str_codigo = ""
        for i in estado:
            if estado[i] != None:
                str_codigo += f"{i}-{estado[i]} "
        return str_codigo

    def costo(self, estado, accion):
        return 0

class Parser:
    '''
    @Autor: Samuel Pérez
    '''
    def __init__(self, gramatica=None, w=None):
        if gramatica is None:
            raise RuntimeError('¡Se necesita una gramática!')
        self.gramatica = gramatica
        self.estado_inicial = {0:(gramatica[0][0], [])}
        self.w = w

    def arbol(self, t, estado):
        rotulo = estado[t][0]
        hijos = estado[t][1]
        if len(hijos) > 0:
            return Tree(rotulo, [self.arbol(i, estado) for i in hijos])
        else:
            return rotulo

    def pintar_estado(self, estado):
        arb = self.arbol(0, estado)
        if type(arb) == str:
            print(arb)
        else:
            arb.pretty_print()

    def pintar_camino(self, camino):
        # Input: lista con el camino de los estados
        # Output: plot con la forma de resolver las torres
        for estado in camino:
            clear_output(wait=True)
            self.pintar_estado(estado)
            plt.show()
            sleep(.5)

    def ulti(self, estado):
        return [x for x in estado if not estado[x][1]]

    def reescritura_nodo(self, u_esta, estado):
        simbolo = estado[u_esta][0]
        nonterminal = set([a_tuple[0] for a_tuple in self.gramatica])
        if simbolo not in nonterminal:
            return []
        reescritura = [a_tuple[1] for a_tuple in self.gramatica if a_tuple[0] == simbolo]
        return reescritura

    def acciones_aplicables(self, estado):
        acciones = []
        ultis = self.ulti(estado)
        for u_esta in ultis:
            print(u_esta)
            reescritura = self.reescritura_nodo(u_esta, estado)
            for sim in reescritura:
                acciones.append((u_esta, sim))
        return acciones

    def transicion(self, estado, accion):
        es_accion = copy.deepcopy(estado)
        es_accion[accion[0]][1].clear()
        for sim in list(accion[1]):
            keys_estados = list(es_accion.keys())
            new_est = keys_estados[-1] + 1
            es_accion[accion[0]][1].append(new_est)
            es_accion[new_est] = (sim, [])
        keys_estados = list(copy.deepcopy(estado).keys())
        u_esta = keys_estados[-1]
        return es_accion

    def constructor(self, estado, ind, nonterminal, list_final):
        simb = estado[ind][0]
        if simb not in nonterminal:
            list_final.append(simb)
            return list_final
        else:
            list_temp = []
            for i in estado[ind][1]:
               list_temp = self.constructor(estado, i, nonterminal, list_final)
            return list_temp

    def test_objetivo(self, estado):
#        print(estado)
        nonterminal = set([a_tuple[0] for a_tuple in self.gramatica])
        list_final = []
        construct = self.constructor(estado, 0, nonterminal, list_final)
#        print(construct)
#        print(self.w)
        w_l = list(self.w)
        return construct == w_l

    def costo(self, estado, accion):
        return 1
