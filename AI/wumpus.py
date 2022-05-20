# ejercicio 2
W = Wumpus(wumpus=(3,3), oro=(2,2), pozos=[(1,0), (3,1)])
W.pintar_casilla()
agente = Agente()
agente.perceptos = W.para_sentidos()
print(agente.perceptos)

W.transicion('voltearIzquierda')
W.transicion('adelante')
W.pintar_casilla()
agente.perceptos = W.para_sentidos()
print(agente.perceptos)

W.transicion('voltearDerecha')
W.transicion('adelante')
W.pintar_casilla()
agente.perceptos = W.para_sentidos()
print(agente.perceptos)

W.transicion('adelante')
W.pintar_casilla()
agente.perceptos = W.para_sentidos()
print(agente.perceptos)

W.transicion('voltearIzquierda')
W.transicion('adelante')
W.pintar_casilla()
agente.perceptos = W.para_sentidos()
print(agente.perceptos)

# ejercicio 4
def hedor_wumpus(self):
    
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
    # AQUÍ COMENZA SU CÓDIGO
    turno = agente.turno
    casillas = adyacentes(agente.loc)
    x, y = agente.loc
    for c in casillas:
        x1, y1 = c
        formulas += [
            f'en({x},{y})_{turno}Y-hedor_{turno}>-wumpus({x1},{y1})',                
        ]
    # AQUÍ TERMINA SU CÓDIGO
    
    return formulas

setattr(Agente, 'hedor_wumpus', hedor_wumpus)

agente = Agente()
agente.hedor_wumpus()

# ejercicio 5
def casilla_segura(self):
    formulas = []
    
    # AQUÍ COMENZA SU CÓDIGO

    
    turno = agente.turno
    x, y = agente.loc
    

    for x in range(0,4):
        for y in range(0,4):

            formulas += [
                f'en({x},{y})_{turno}Y-wumpus_{turno}>segura({x},{y})',]   
    
    # AQUÍ TERMINA SU CÓDIGO
    return formulas

setattr(Agente, 'casilla_segura', casilla_segura)

agente = Agente()
agente.casilla_segura()
