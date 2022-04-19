import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols
import numpy as np
import types
from time import time


def depth(estado): 
    '''
    Computes the depth of the solution
    '''
    camino = []
    camino.append(estado.codigo)

    while estado.madre is not None: 
        estado_madre = estado.madre
        camino.append(estado_madre.codigo)
        estado = estado_madre

    return len(camino) - 1

def is_cycle(estado):

    camino = []
    camino.append(estado.codigo)

    while estado.madre is not None: 
        estado_madre = estado.madre
        camino.append(estado_madre.codigo)
        estado = estado_madre

    counter = {i:camino.count(i) for i in camino}

    repetidos = 0
    caminos_repetidos = []
    for camino, conteo in counter.items():
        if conteo > 1:
            repetidos += 1
            caminos_repetidos.append({camino : conteo})
    
    return True if repetidos > 0 else False

def depth_limited_search(prob, l):
    nodo = Nodo(prob.estado_inicial, None, None, 0, prob.codigo(prob.estado_inicial))
    frontera = [nodo] # LIFO list
    resultado = "Fail"
    
    while len(frontera) > 0: 
        nodo = frontera.pop()
        
        if prob.test_objetivo(nodo.estado): 
            return nodo
        
        if depth(nodo) >= l: 
            resultado = "cutoff"

        elif not is_cycle(nodo): 
            for hijo in Expand(prob, nodo):
                frontera.append(hijo)
    return resultado

def Expand(prob, nodo): 
    s = nodo.estado
    nodos = []
    for accion in prob.acciones_aplicables(s):
        hijo = nodo_hijo(prob, nodo, accion)
        nodos.append(hijo)
    return nodos

def iterative_deepening_search(prob, l_max):
    for depth in range(0, l_max):
        #print("depth: ", depth)
        resultado = depth_limited_search(prob, depth)
        
        if resultado != "cutoff":
            #return my_caminio(resultado) # return the path to the solution
            return resultado # uncomment to see the pseudocode result 

    return "Fail"

def my_caminio(estado): 

    camino = []
    camino.append(estado.codigo)

    while estado.madre is not None: 
        estado_madre = estado.madre
        camino.append(estado_madre.codigo)
        estado = estado_madre

    return camino

def my_camino2(estado): 

    camino = []
    camino.append(estado.estado)

    while estado.madre is not None: 
        estado_madre = estado.madre
        camino.append(estado_madre.estado)
        estado = estado_madre

    camino.reverse()
    return camino

def obtiene_tiempos(fun, args, num_it=100):
    tiempos_fun = []
    for i in range(num_it):
        arranca = time()
        x = fun(*args)
        para = time()
        tiempos_fun.append(para - arranca)
    return tiempos_fun

def compara_funciones(funs, arg, nombres, N=30):
    nms = []
    ts = []
    for i, fun in enumerate(funs):
        nms += [nombres[i] for x in range(N)]
        ts += obtiene_tiempos(fun, [arg], N)
    data = pd.DataFrame({'Función':nms, 'Tiempo':ts})
    # Graficando
    fig, ax = plt.subplots(1,1, figsize=(3*len(funs),3), tight_layout=True)
    sns.boxplot(data=data, x='Función', y='Tiempo')
    sns.swarmplot(data=data, x='Función', y='Tiempo', color='black', alpha = 0.5, ax=ax);
    # Anova diferencia de medias
    model = ols('Tiempo ~ C(Función)', data=data).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print(anova_table)

class ListaPrioritaria():
    
    def __init__(self):
        self.diccionario = {}
        
    def __str__(self):
        cadena = '['
        inicial = True
        for costo in self.diccionario:
            elementos = self.diccionario[costo]
            for elemento in elementos:
                if inicial:
                    cadena += '(' + str(elemento) + ',' + str(costo) + ')'
                    inicial = False
                else:
                    cadena += ', (' + str(elemento) + ',' + str(costo) + ')'

        return cadena + ']'
    
    def push(self, elemento, costo):
        try:
            self.diccionario[costo].append(elemento)
        except:
            self.diccionario[costo] = [elemento]
            
    def pop(self):
        min_costo = np.min(np.array(list(self.diccionario.keys())))
        candidatos = self.diccionario[min_costo]
        elemento = candidatos.pop()
        if len(candidatos) == 0:
            del self.diccionario[min_costo]
        return elemento
    
    def is_empty(self):
        return len(self.diccionario) == 0
  
def solucion(n):
    if n.madre == None:
        return []
    else:
        return solucion(n.madre) + [n.accion]

def best_first_search(prob, f):
    prob.costo = types.MethodType(f, prob)
    s = prob.estado_inicial
    cod = prob.codigo(s)
    nodo =  Nodo(s, None, None, 0, prob.codigo(s))
    frontera = ListaPrioritaria()
    frontera.push(nodo, 0)
    explorados = {cod : 0}

    while len(frontera.diccionario) > 0:
        nodo = frontera.pop()
        if prob.test_objetivo(nodo.estado): 
            return nodo
        
        for hijo in Expand(prob, nodo):
            s = hijo.estado
            cod = prob.codigo(s)
            c = hijo.costo_camino

            if cod not in explorados.keys() or c < explorados[cod]:
                frontera.push(hijo,c)
                explorados[cod] = c

    return "Fail"

class Nodo:

    # Clase para crear los nodos

    def __init__(self, estado, madre, accion, costo_camino, codigo):
        self.estado = estado
        self.madre = madre
        self.accion = accion
        self.costo_camino = costo_camino
        self.codigo = codigo

def nodo_hijo(problema, madre, accion):

    # Función para crear un nuevo nodo
    # Input: problema, que es un objeto de clase ocho_reinas
    #        madre, que es un nodo,
    #        accion, que es una acción que da lugar al estado del nuevo nodo
    # Output: nodo

    estado = problema.transicion(madre.estado, accion)
    costo_camino = madre.costo_camino + problema.costo(madre.estado, accion)
    codigo = problema.codigo(estado)
    return Nodo(estado, madre, accion, costo_camino, codigo)

def solucion(n):
    if n.madre == None:
        return []
    else:
        return solucion(n.madre) + [n.accion]

def backtracking_search(problema, estado):

    '''Función de búsqueda recursiva de backtracking'''

    if problema.test_objetivo(estado):
            return estado
    acciones = problema.acciones_aplicables(estado)
    for a in acciones:
        hijo = problema.transicion(estado, a)
        resultado = backtracking_search(problema, hijo)
        if resultado is not None:
            return resultado
    return None

def breadth_first_search(problema):

    '''Función de búsqueda breadth-first'''

    nodo = Nodo(problema.estado_inicial, None, None, 0, problema.codigo(problema.estado_inicial))
    if problema.test_objetivo(nodo.estado):
            return nodo
    frontera = [nodo]
    explorados = []
    while len(frontera) > 0:
        nodo = frontera.pop(0)
        explorados.append(nodo.codigo)
        acciones = problema.acciones_aplicables(nodo.estado)
        for a in acciones:
            hijo = nodo_hijo(problema, nodo, a)
            if problema.test_objetivo(hijo.estado):
                return hijo
            if hijo.codigo not in explorados:
                frontera.append(hijo)
    return None

def depth_first_search(problema):

    '''Función de búsqueda depth-first'''

    nodo = Nodo(problema.estado_inicial, None, None, 0, problema.codigo(problema.estado_inicial))
    if problema.test_objetivo(nodo.estado):
            return nodo
    frontera = [nodo]
    explorados = []
    while len(frontera) > 0:
        nodo = frontera.pop()
        explorados.append(nodo.codigo)
        acciones = problema.acciones_aplicables(nodo.estado)
        for a in acciones:
            hijo = nodo_hijo(problema, nodo, a)
            if problema.test_objetivo(hijo.estado):
                return hijo
            if hijo.codigo not in explorados:
                frontera.append(hijo)
    return None
