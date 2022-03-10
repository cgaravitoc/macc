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
