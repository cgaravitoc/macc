notebook 4

ejercicio 3
l = breadth_first_search(viaje)
if l is not None:
  camino = [viaje.estado_inicial] + solucion(l)
  print("La soluciòn encontrada es: ", camino)
  print("La cantidad de kilometros es: ", l.costo_camino)
else:
  print("No hay solucion")
