import numpy as np

class Descriptor :

    '''
    Codifica un descriptor de N argumentos mediante un solo caracter
    Input:  args_lista, lista con el total de opciones para cada
                     argumento del descriptor
            chrInit, entero que determina el comienzo de la codificación chr()
    Output: str de longitud 1
    '''

    def __init__ (self,args_lista,chrInit=256) :
        self.args_lista = args_lista
        assert(len(args_lista) > 0), "Debe haber por lo menos un argumento"
        self.chrInit = chrInit
        self.rango = [chrInit, chrInit + np.prod(self.args_lista)]

    def check_lista_valores(self,lista_valores) :
        for i, v in enumerate(lista_valores) :
            assert(v >= 0), "Valores deben ser no negativos"
            assert(v < self.args_lista[i]), f"Valor debe ser menor a máximo {self.args_lista[i]}"

    def codifica(self,lista_valores) :
        self.check_lista_valores(lista_valores)
        cod = lista_valores[0]
        n_columnas = 1
        for i in range(0, len(lista_valores) - 1) :
            n_columnas = n_columnas * self.args_lista[i]
            cod = n_columnas * lista_valores[i+1] + cod
        return cod

    def decodifica(self,n) :
        decods = []
        if len(self.args_lista) > 1:
            for i in range(0, len(self.args_lista) - 1) :
                n_columnas = np.prod(self.args_lista[:-(i+1)])
                decods.insert(0, int(n / n_columnas))
                n = n % n_columnas
        decods.insert(0, n % self.args_lista[0])
        return decods

    def P(self,lista_valores) :
        codigo = self.codifica(lista_valores)
        return chr(self.chrInit+codigo)

    def inv(self,codigo) :
        n = ord(codigo)-self.chrInit
        return self.decodifica(n)

class ClausulaDefinida :
    '''
    Implementación de las cláusulas definidas
    Input: clausula, que es una cadena de la forma p1 Y ... Y pn > q
    '''

    def __init__(self, clausula) :
        self.nombre = clausula
        indice_conectivo = clausula.find('>')
        if indice_conectivo > 0:
            cuerpo = clausula[:indice_conectivo].split('Y')
            cabeza = clausula[indice_conectivo + 1:]
        else:
            cuerpo = clausula.split('Y')
            cabeza = ''
        self.cuerpo = cuerpo
        self.cabeza = cabeza

class LPQuery:

    '''
    Implementación de una base de conocimiento.
    Input:  base_conocimiento_lista, que es una lista de cláusulas definidas
                de la forma p1 Y ... Y pn > q
            cods, un objeto de clase Descriptor
    '''

    def __init__(self, base_conocimiento_lista) :
        self.datos = []
        self.reglas = []
        self.atomos = []
        for formula in base_conocimiento_lista:
            self.TELL(formula)

    def __str__(self) :
        cadena = 'Datos:\n'
        for dato in self.datos:
            cadena += dato + '\n'
        cadena += '\nReglas:\n'
        for regla in self.reglas:
            cadena += regla.nombre + '\n'
        return cadena

    def reglas_aplicables(self, head):
        return [r for r in self.reglas if r.cabeza == head]

    def test_objetivo(self, literal):
        return literal in self.datos

    def TELL(self, formula):
        indice_conectivo = formula.find('>')
        if indice_conectivo > 0:
            clausula = ClausulaDefinida(formula)
            self.reglas.append(clausula)
            for a in clausula.cuerpo:
            	if '-' in a:
            		atomo = a[1:]
            	else:
                	atomo = a
            	if atomo not in self.atomos:
            		self.atomos.append(a)
            if '-' in clausula.cabeza:
            	atomo = clausula.cabeza[1:]
            else:
            	atomo = clausula.cabeza
            if atomo not in self.atomos:
            	self.atomos.append(atomo)
        elif formula not in self.datos:
            self.datos.append(formula)
            if '-' in formula:
            	atomo = formula[1:]
            else:
            	atomo = formula
            if atomo not in self.atomos:
            	self.atomos.append(atomo)
