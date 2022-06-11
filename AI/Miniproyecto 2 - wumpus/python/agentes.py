from logica import LPQuery

class Agente:

	def __init__(self):
		self.perceptos = []
		self.acciones = []
		self.tabla = {}
		self.reglas = []
		self.base = LPQuery([])
		self.turno = 1
		self.loc = (0,0)

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
