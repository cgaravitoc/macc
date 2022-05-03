notebook 4

ejercicio 3
l = breadth_first_search(viaje)
if l is not None:
  camino = [viaje.estado_inicial] + solucion(l)
  print("La soluciòn encontrada es: ", camino)
  print("La cantidad de kilometros es: ", l.costo_camino)
else:
  print("No hay solucion")
  
 def piezas_mal_puestas(self, estado, accion):
    resultado = self.transicion(estado, accion)
    return len(np.where(resultado != self.objetivo)[0]) - 1

def manhattan(self, estado, accion):
    resultado = self.transicion(estado, accion)
    distancia = 0
    for i in range(1, 9): 
        y1, x1 = np.where(resultado == i)
        y2, x2 = np.where(self.objetivo == i)
        distancia += np.abs(x1 - x2) + np.abs(y1 - y2)
    return distancia[0]
    
 ejercicio 8
 %%time
puz = Rompecabezas()
S = np.matrix([[0, 6, 1], [4, 8, 7], [5, 2, 3]])
puz.estado_inicial = S
l = best_first_search(puz, manhattan) #the second argument must be the heuristic function
if l is not None:
    camino = solucion(l)
    print("La solución encontrada es: ", camino)
    print("La cantidad de movimientos es: ", len(camino))
else:
    print("No hay solución!")
