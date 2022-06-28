from logica import LPQuery, ASK

class Agente:

	def __init__(self):
		self.perceptos = []
		self.acciones = []
		self.tabla = {}
		self.reglas = []
		self.base = LPQuery([])
		self.turno = 1
		self.loc = (0,0)
		self.direccion = 'este'
		self.oro = False

	def reaccionar(self, DEB=False):
		if len(self.acciones) == 0:
			self.programa(DEB)
		a = self.acciones.pop(0)
		self.turno += 1
		return a

	def interp_percepto(self, mundo):
		if mundo == 'laberinto':
			orden = ['frn_bloq_', 'izq_bloq_', 'der_bloq_', 'atr_bloq_']
		elif mundo == 'wumpus':
			orden = ['hedor_', 'brisa_', 'brillo_', 'batacazo_', 'grito_']
		f = ''
		inicial = True
		for i, p in enumerate(self.perceptos):
			if p:
				if inicial:
					f = orden[i]+str(self.turno)
					inicial = False
				else:
					f = f + 'Y' + orden[i]+str(self.turno)
			else:
				if inicial:
					f = '-' + orden[i]+str(self.turno)
					inicial = False
				else:
					f = f + 'Y-' + orden[i]+str(self.turno)
		return f

	def fluentes_mapa_mental(self):
	    turno = self.turno
	    x, y = self.loc
	    formulas = [
	        f'en({x},{y})_{turno}Ymirando_o_{turno}Yadelante_{turno}>en({x-1},{y})_{turno+1}',
	        f'en({x},{y})_{turno}Ymirando_e_{turno}Yadelante_{turno}>en({x+1},{y})_{turno+1}',
	        f'en({x},{y})_{turno}Ymirando_s_{turno}Yadelante_{turno}>en({x},{y-1})_{turno+1}',
	        f'en({x},{y})_{turno}Ymirando_n_{turno}Yadelante_{turno}>en({x},{y+1})_{turno+1}',
	        f'en({x},{y})_{turno}YvoltearIzquierda_{turno}>en({x},{y})_{turno+1}',
	        f'en({x},{y})_{turno}YvoltearDerecha_{turno}>en({x},{y})_{turno+1}',
	        f'en({x},{y})_{turno}Yagarrar_{turno}>en({x},{y})_{turno+1}',
	        f'mirando_o_{turno}Yadelante_{turno}>mirando_o_{turno+1}',
	        f'mirando_s_{turno}Yadelante_{turno}>mirando_s_{turno+1}',
	        f'mirando_e_{turno}Yadelante_{turno}>mirando_e_{turno+1}',
	        f'mirando_n_{turno}Yadelante_{turno}>mirando_n_{turno+1}',
	        f'mirando_o_{turno}Yagarrar_{turno}>mirando_o_{turno+1}',
	        f'mirando_s_{turno}Yagarrar_{turno}>mirando_s_{turno+1}',
	        f'mirando_e_{turno}Yagarrar_{turno}>mirando_e_{turno+1}',
	        f'mirando_n_{turno}Yagarrar_{turno}>mirando_n_{turno+1}',
	        f'mirando_o_{turno}YvoltearIzquierda_{turno}>mirando_s_{turno+1}',
	        f'mirando_s_{turno}YvoltearIzquierda_{turno}>mirando_e_{turno+1}',
	        f'mirando_e_{turno}YvoltearIzquierda_{turno}>mirando_n_{turno+1}',
	        f'mirando_n_{turno}YvoltearIzquierda_{turno}>mirando_o_{turno+1}',
	        f'mirando_o_{turno}YvoltearDerecha_{turno}>mirando_n_{turno+1}',
	        f'mirando_n_{turno}YvoltearDerecha_{turno}>mirando_e_{turno+1}',
	        f'mirando_e_{turno}YvoltearDerecha_{turno}>mirando_s_{turno+1}',
	        f'mirando_s_{turno}YvoltearDerecha_{turno}>mirando_o_{turno+1}',
	    ]
	    casillas = [(x,y) for x in range(12) for y in range(12)]
	    for c in casillas:
	        x, y = c
	        formulas += [
	            f'en({x},{y})_{turno}>visitada({x},{y})_{turno}',
	            f'visitada({x},{y})_{turno}>visitada({x},{y})_{turno+1}',
	        ]
	    return formulas

	def nueva_posicion(self):

	    def truncar(x):
	        if x < 0:
	            return 0
	        elif x > 3:
	            return 3
	        else:
	            return x

	    def adyacentes(casilla):
	        x, y = casilla
	        adyacentes = [
	            (truncar(x - 1), y), (truncar(x + 1), y),
	            (x, truncar(y - 1)), (x, truncar(y + 1))
	        ]
	        adyacentes = [c for c in adyacentes if c != casilla]
	        return adyacentes

	    casillas = [self.loc] + adyacentes(self.loc)
	    for c in casillas:
	        x, y = c
	        pos = f'en({x},{y})_{self.turno}'
	        evaluacion = ASK(pos, 'success', self.base)
	        if evaluacion:
	            self.loc = (x,y)
	            return pos
	    raise Exception('¡No se encontró posición!')

	def nueva_direccion(self):
	    direcciones = ['o', 'e', 's', 'n']
	    for d in direcciones:
	        direccion = f'mirando_{d}_{self.turno}'
	        evaluacion = ASK(direccion, 'success', self.base)
	        if evaluacion:
	            return direccion
	    raise Exception('¡No se encontró dirección!')

	def estimar_estado(self, W):
	    nueva_dir = self.nueva_direccion()
	    self.base.TELL(nueva_dir)
	    nueva_pos = self.nueva_posicion()
	    self.base.TELL(nueva_pos)
	    formulas = [d for d in self.base.datos if f'_{self.turno}' in d]
	    formulas += self.fluentes_mapa_mental()
	    self.direccion = self.solo_direccion()
	    self.perceptos = W.para_sentidos()
	    formulas += [self.interp_percepto(mundo='wumpus')]
	    self.base = LPQuery(formulas)

	def solo_direccion(self):
	    direcciones = ['o', 'e', 's', 'n']
	    dir_direcciones = {'o':'oeste', 'e':'este', 's':'sur', 'n':'norte'}
	    for d in direcciones:
	        direccion = f'mirando_{d}_{self.turno}'
	        if direccion in self.base.datos:
	            return dir_direcciones[d]
	    raise Exception('¡No se encontró dirección!')
