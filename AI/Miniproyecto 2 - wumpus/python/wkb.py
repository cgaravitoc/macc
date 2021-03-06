from logica import LPQuery
from logica import *
from entornos import *

class Agente_wkb:

	def __init__(self):
		self.perceptos = []
		self.acciones = []
		self.tabla = {}
		self.reglas = []
		self.base = LPQuery([])
		self.turno = 1
		self.loc = (0,0)
		self.alertas = [] # new

	def reaccionar_wkb(self, DEB=False):
		if len(self.acciones) == 0:
			self.programa(DEB)
		a = self.acciones.pop(0)
		self.turno += 1
		return a

	def interp_percepto_wkb(self, mundo):
		if mundo == 'laberinto': # no necesario (carlos)
			orden = ['frn_bloq_', 'izq_bloq_', 'der_bloq_', 'atr_bloq_'] # no necesario (carlos)
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

	'''
	*******************************
	base de conocimiento del wumpus
	*******************************
	'''
	def brisa_pozo_wkb(self):
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
		
		turno = self.turno
		casillas = adyacentes(self.loc)
		x, y = self.loc
		formulas = []
		for c in casillas:
			x1, y1 = c
			formulas += [
				f'en({x},{y})_{turno}Y-brisa_{turno}>-pozo({x1},{y1})',                
			]
		return formulas

	def hedor_wumpus_wkb(self):
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
		
		formulas = []
		# AQU?? COMENZA SU C??DIGO
		turno = self.turno
		casillas = adyacentes(self.loc)
		x, y = self.loc
		for c in casillas:
			x1, y1 = c
			formulas += [
				f'en({x},{y})_{turno}Y-hedor_{turno}>-wumpus({x1},{y1})',                
			]
		# AQU?? TERMINA SU C??DIGO
		
		return formulas	

	def casilla_segura_wkb(self):
		formulas = []
		# AQU?? COMENZA SU C??DIGO
		casillas = [ f'({i},{j})' for i in range(0,4) for j in range(0,4)]
		for casilla in casillas: 
			formulas += [(f'-pozo{casilla}Y-wumpus{casilla}>segura{casilla}')]
		# AQU?? TERMINA SU C??DIGO
		return formulas

	def fluentes_mapa_mental_wkb(self):
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
	
	def adyacentes_seguras_wkb(self):
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
	
		casillas_seguras = []
		# AQU?? COMIENZA SU C??DIGO
		casillas = adyacentes(self.loc)
		for c in casillas: 
			d = str(c).replace(" ", "")
			objetivo = f'segura{d}'
			#print("-->", "Objetivo:", objetivo)
			#print()
			#print("Datos:", self.base.datos)
			#print()
			#print("Reglas aplicables para el objetivo:")
			#reglas_objeto = self.base.reglas_aplicables(objetivo)
			#for r in reglas_objeto:
			#    print(' Y '.join(r.cuerpo), ">", r.cabeza, "\n")
			res = ASK(objetivo, 'success', self.base)
			if res: 
				casillas_seguras.append(c)
			#else: 
			#    print('??no seguro! \n')
		# AQU?? TERMINA SU C??DIGO
		return casillas_seguras

	def estimar_estado_wkb(self, W):
		self.base.TELL(f'segura({self.loc[0]},{self.loc[1]})')
		cas_seguras = self.adyacentes_seguras_wkb()
		self.base.TELL('Y'.join([f'segura({c[0]},{c[1]})' for c in cas_seguras]))
		nueva_dir = self.nueva_direccion_wkb()
		self.base.TELL(nueva_dir)
		nueva_pos = self.nueva_posicion_wkb()
		self.base.TELL(nueva_pos)
		formulas = [d for d in self.base.datos if f'_{self.turno}' in d]
		formulas += [s for s in self.base.datos if 'segura' in s]
		formulas += self.fluentes_mapa_mental_wkb()
		formulas += self.brisa_pozo_wkb()
		formulas += self.hedor_wumpus_wkb()
		formulas += self.casilla_segura_wkb()
		formulas += self.casillas_visitadas_wkb()
		self.perceptos = W.para_sentidos()
		formulas += [self.interp_percepto_wkb(mundo='wumpus')]
		self.base = LPQuery(formulas)

	def casillas_visitadas_wkb(self):
		turno = self.turno
		# Guardamos las casillas visitadas
		visitadas = []
		casillas = [(x,y) for x in range(4) for y in range(4)]
		for c in casillas:
			x, y = c
			consulta = ASK(f'visitada({x},{y})_{turno}', 'success', self.base)
			if consulta:
				visitadas.append(f'visitada({x},{y})_{turno}')
		return visitadas

	def nueva_posicion_wkb(self):
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
		raise Exception('??No se encontr?? posici??n!')
	
	def nueva_direccion_wkb(self):
		direcciones = ['o', 'e', 's', 'n']
		for d in direcciones:
			direccion = f'mirando_{d}_{self.turno}'
			evaluacion = ASK(direccion, 'success', self.base)
			if evaluacion:
				return direccion
		raise Exception('??No se encontr?? direcci??n!')

	def solo_direccion_wkb(self):
		direcciones = ['o', 'e', 's', 'n']
		dir_direcciones = {'o':'oeste', 'e':'este', 's':'sur', 'n':'norte'}
		for d in direcciones:
			direccion = f'mirando_{d}_{self.turno}'
			if direccion in self.base.datos:
				return dir_direcciones[d]
		raise Exception('??No se encontr?? direcci??n!')
	
	def cache_wkb(self):
		turno = self.turno
		casilla_actual = self.loc
		direccion = self.solo_direccion_wkb()
		cas_seguras = self.adyacentes_seguras_wkb()
		cas_seguras = [c for c in cas_seguras if c != casilla_actual]
		cas_visitadas = self.casillas_visitadas_wkb()
		cas_visitadas = [tuple([int(s[9]),int(s[11])]) for s in cas_visitadas]
		return turno, casilla_actual, direccion, cas_seguras, cas_visitadas

	def todas_seguras_wkb(self):
		casillas_seguras = []
		for x in range(4):
			for y in range(4):
				objetivo = f'segura({x},{y})'  
				resultado = ASK(objetivo, 'success', self.base)
				if resultado:
					casillas_seguras.append((x,y))
		return casillas_seguras
class Rejilla:
	'''
	Problema del tr??nsito por la rejilla
	desde donde est?? el h??roe hasta una
	casilla objetivo
	Par??metros:
		- inicial, una casilla de la forma (x,y)
		- objetivo, una casilla de la forma (x,y)
		- seguras, una lista de casillas que restringen
					las acciones aplicables
	'''
	
	def __init__(self, inicial, objetivo, seguras):
		self.estado_inicial = inicial
		self.estado_objetivo = objetivo
		self.casillas_seguras = seguras
	
	def adyacentes(self, casilla):
		def truncar(x):
			if x < 0:
				return 0
			elif x > 3:
				return 3
			else:
				return x
		x, y = casilla
		adyacentes = [
			(truncar(x - 1), y), (truncar(x + 1), y),
			(x, truncar(y - 1)), (x, truncar(y + 1))
		]
		adyacentes = [c for c in adyacentes if c != casilla]
		return adyacentes
	
	def acciones_aplicables(self, estado):
		return [casilla for casilla in self.adyacentes(estado) if casilla in self.casillas_seguras]
	
	def transicion(self, estado, accion):
		return accion
	
	def test_objetivo(self, estado):
		return estado == self.estado_objetivo
	
	def costo(self, estado, accion):
		x1, y1 = estado
		x2, y2 = self.transicion(estado, accion)
		return abs(x1 - x2) + abs(y1 - y2)
	
	def codigo(self, estado):
		x, y = estado
		return f"{x}-{y}"
