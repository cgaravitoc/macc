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