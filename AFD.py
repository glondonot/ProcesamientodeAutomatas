import random

class Alfabeto:
    def __init__(self, simbolos):
        self.simbolos = simbolos
    def generarCadenaAleatoria(self, n):
        cadena = ""
        for i in range(n):
            cadena += random.choice(self.simbolos)
        return cadena

abc = Alfabeto(['a', 'b', 'c'])

class clasePrueba:
    def __init__(self):
        pass
    def crearAFD(sigma, numeroEstados, numeroEstadosFinales):
        #llenar estados
        estados = []
        for x in range(0,numeroEstados):
            estados.append('q'+str(x))

        estadoInicial = estados[0]

        #llenar estados finales
        estadosFinales = []
        def llenarFinales():
            if len(estadosFinales) < numeroEstadosFinales:
                estado = random.choice(estados)
                if estado not in estadosFinales:
                    estadosFinales.append(estado)
                llenarFinales()
        llenarFinales()

        #llenar delta
        delta = {}
        for x in estados:
            delta[x] = {}
            for y in sigma:
                delta[x][y] = random.choice(estados)

        #Sigma, Q , q0, F, delta, estadosLimbo, estadosInaccesibles
        afd0 = AFD(sigma, estados, estadoInicial, estadosFinales, delta, [], [])
        afd0.verificarCorregirCompletitudAFD()
        afd0.hallarEstadosLimbo()
        afd0.hallarEstadosInaccesibles()
        return afd0
    


    def probarAFD(sigma, numeroEstados, numeroEstadosFinales, cadena, detalles, nombreArchivo, imprimirPantalla):
        afd0 = clasePrueba.crearAFD(sigma, numeroEstados, numeroEstadosFinales)
        if type(cadena) == str:
            if not detalles:
                afd0.procesarCadena(cadena)
            elif detalles:
                afd0.procesarCadenaConDetalles(cadena)
        elif type(cadena) == list:
            afd0.procesarListaCadenas(cadena, nombreArchivo, imprimirPantalla)
        return afd0
    
    def probarComplemento(sigma, numeroEstados, numeroEstadosFinales):
        afd0 = clasePrueba.crearAFD(sigma, numeroEstados, numeroEstadosFinales)
        afd0Complemento = afd0.hallarComplemento(afd0)
        print('AFD dado: ')
        afd0.imprimirAFDSimplificado()
        print('Complemento del AFD dado: ')
        afd0Complemento.imprimirAFDSimplificado()
        return afd0Complemento  

    def probarProductoCarteciano(sigma, numeroEstados1, numeroEstadosFinales1, numeroEstados2, numeroEstadosFinales2, operacion):
        afd1 = clasePrueba.crearAFD(sigma, numeroEstados1, numeroEstadosFinales1)
        afd2 = clasePrueba.crearAFD(sigma, numeroEstados2, numeroEstadosFinales2)
        afdProductoCartesiano = afd1.hallarProductoCartesiano(afd1, afd2, operacion)
        print("el primer AFD es: ")
        afd1.imprimirAFDSimplificado()
        print("el primer AFD es: ")
        afd2.imprimirAFDSimplificado()
        print('el producto carteciano es: ')
        afdProductoCartesiano.imprimirAFDSimplificado()
        return afdProductoCartesiano

    def probarSimplificación(sigma, numeroEstados, numeroEstadosFinales, numeroPruebas):
        afd0 = clasePrueba.crearAFD(sigma, numeroEstados, numeroEstadosFinales)
        print('proceso de simplificacion: ')
        afdSimplificado = afd0.simplificarAFD(afd0)
        alfabeto = Alfabeto(sigma)
        for x in range (0,numeroPruebas):
            cadena = alfabeto.generarCadenaAleatoria(6)
            print('la cadena a procesar es:', cadena)
            print('resultado sin simplificar: ')
            afd0.procesarCadena(cadena)
            print('resultado con AFD simplificado: ')
            afdSimplificado.procesarCadena(cadena)
        return afdSimplificado

class AFD(clasePrueba):
    pass
    def __init__(self, Sigma=None, Q=None , q0=None, F=None, delta=None, estadosLimbo=None, estadosInaccesibles=None):
        if Sigma == None and Q == None and q0 == None and F == None and delta == None and estadosLimbo == None and estadosInaccesibles == None:
            Sigma = []
            Q = []
            q0 = ''
            F = []
            delta = {}
            estadosLimbo = []
            estadosInaccesibles = []
        self.Sigma = Sigma
        self.Q = Q
        self.q0 = q0
        self.F = F
        self.delta = delta
        self.estadosLimbo = estadosLimbo
        self.estadosInaccesibles = estadosInaccesibles
        self.limbo = False
        self.verificarCorregirCompletitudAFD()

    #Revisa si el AFD leído está completo y sino agrega un 
    # estado limbo y ajusta las transiciones para que quede completo

    def  contructor(self, nombreArchivo):
        leyendo = ''
        with open(nombreArchivo) as f:
            for line in f:
                if line[0] == '#':
                    leyendo = line.rstrip()
                elif leyendo == '#alphabet':
                    cadena = line.rstrip()
                    if '-' not in cadena:
                        self.Sigma.append(cadena)
                    else:
                        inicio, fin = cadena.split('-')
                        letras = ''.join(chr(i) for i in range(ord(inicio), ord(fin) + 1))
                        for x in letras:
                            self.Sigma.append(x)
                elif leyendo == '#states':
                    self.Q.append(line.rstrip())
                elif leyendo == '#initial':
                    self.q0 = line.rstrip()
                elif leyendo == '#accepting':
                    self.F.append(line.rstrip())
                elif leyendo == '#transitions':
                    for x in range(0,len(line.rstrip())):
                        if line[x] == ':':
                            if line[0:x] not in self.delta:
                                self.delta[line[0:x]] = {}
                            self.delta[line[0:x]][line[x+1]] = line[x+3:len(line.rstrip())]
                    
                elif leyendo == '#inaccessible':
                    self.estadosInaccesibles.append(line.rstrip())

                elif leyendo == '#limbo':
                    self.estadosLimbo.append(line.rstrip())
        self.verificarCorregirCompletitudAFD()

    def verificarCorregirCompletitudAFD(self):
        for x in self.Sigma:
            for y in self.delta:
                if x not in self.delta[y]:
                    if not self.limbo:
                        self.crearLimbo()
                        break
                    else:
                        self.delta[y][x] = 'limbo'

    #crea el estado limbo del verificar completitud
    def crearLimbo(self):
        self.Q.append('limbo')
        self.estadosLimbo.append('limbo')
        self.delta['limbo'] = {}
        self.limbo = True
        self.verificarCorregirCompletitudAFD()
    

    #para determinar los estados limbo del autómata y guardarlos en el atributo correspondiente.
    def hallarEstadosLimbo(self):
        for x in self.delta:
            igual = True
            for y in self.delta[x]:
                if x != self.delta[x][y]:
                    igual = False
                    break
                else:
                    pass
            if igual == True:
                self.estadosLimbo.append(x)
                igual == False

    #para determinar los estados inacessibles del autómata y guardarlos en el atributo correspondiente.
    def hallarEstadosInaccesibles(self):
        for x in self.Q:#x = estados
            accesible = False
            for y in self.delta:#y = estados en la funcion delta
                if x != y and not accesible:
                    for z in self.Sigma:#z = estados luego de procesar una letra
                        if x == self.delta[y][z]:
                           accesible = True
                           break
            if not accesible and x != self.q0:
                self.estadosInaccesibles.append(x)
            accesible = False
    
    #procesa la cadena y retorna verdadero si es  aceptada y falso si es rechazada por el autómata.
    def procesarCadena(self, cadena):
        estadoActual = self.q0
        for x in cadena:
            estadoActual = self.delta[estadoActual][x]
        if estadoActual in self.F:
            print('la cadena fue aceptada')
            return True
        else:
            print('la cadena fue rechazada')
            return False
        
    #lo mismo de arriba pero muestra los detalles
    def procesarCadenaConDetalles(self, cadena):
        estadoActual = self.q0
        for x in cadena:
            estadoActual = self.delta[estadoActual][x]
            print(x+'>'+estadoActual)
        if estadoActual in self.F:
            print('la cadena fue aceptada')
            return True
        else:
            print('la cadena fue rechazada')
            return False
    

    def hallarComplemento(self, afdInput):
        complementoafdInput = AFD(self.Sigma, self.Q , self.q0, self.F, self.delta, self.estadosLimbo, self.estadosInaccesibles)
        complementoafdInput.F = []
        
        for x in afdInput.Q:
            if x not in afdInput.F:
                complementoafdInput.F.append(x)
            else:
                pass
        
        return complementoafdInput
    

    def hallarProductoCartesianoY(self, afd1, afd2):
        productoCartesiano = AFD(self.Sigma, self.Q , self.q0, self.F, self.delta, self.estadosLimbo, self.estadosInaccesibles)
        productoCartesiano.Q = []
        productoCartesiano.q0 = '('+afd1.q0+','+afd2.q0+')'
        productoCartesiano.F = []#es lo que cambia de un producto cartesiano a otro
        productoCartesiano.delta = {}
        productoCartesiano.estadosLimbo = []
        productoCartesiano.estadosInaccesibles = []
        for x in afd1.Q:#x estado del primer automata
            for y in afd2.Q:#y estado del segundo automata
                    productoCartesiano.delta['('+x+','+y+')'] = {}
                    productoCartesiano.Q.append('('+x+','+y+')')
                    if x in afd1.F and y in afd2.F:
                        productoCartesiano.F.append('('+x+','+y+')')
                    for z in afd1.Sigma:#letra procesando
                        resultado = '('+afd1.delta[x][z]+','+afd2.delta[y][z]+')'
                        productoCartesiano.delta['('+x+','+y+')'][z] = resultado
                        #print('δ(('+x+','+y+'),'+z+') = '+'(δ1('+x+','+z+'),'+'(δ2('+y+','+z+') = '+ resultado)
        productoCartesiano.hallarEstadosLimbo()
        productoCartesiano.hallarEstadosInaccesibles()
        return productoCartesiano
    

    def hallarProductoCartesianoO(self, afd1, afd2):
        productoCartesiano = AFD(self.Sigma, self.Q , self.q0, self.F, self.delta, self.estadosLimbo, self.estadosInaccesibles)
        productoCartesiano.Q = []
        productoCartesiano.q0 = '('+afd1.q0+','+afd2.q0+')'
        productoCartesiano.F = []#es lo que cambia de un producto cartesiano a otro
        productoCartesiano.delta = {}
        productoCartesiano.estadosLimbo = []
        productoCartesiano.estadosInaccesibles = []
        for x in afd1.Q:#x estado del primer automata
            for y in afd2.Q:#y estado del segundo automata
                    productoCartesiano.delta['('+x+','+y+')'] = {}
                    productoCartesiano.Q.append('('+x+','+y+')')
                    if x in afd1.F or y in afd2.F:
                        productoCartesiano.F.append('('+x+','+y+')')
                    for z in afd1.Sigma:#letra procesando
                        resultado = '('+afd1.delta[x][z]+','+afd2.delta[y][z]+')'
                        productoCartesiano.delta['('+x+','+y+')'][z] = resultado
                        #print('δ(('+x+','+y+'),'+z+') = '+'(δ1('+x+','+z+'),'+'(δ2('+y+','+z+') = '+ resultado)
        productoCartesiano.hallarEstadosLimbo()
        productoCartesiano.hallarEstadosInaccesibles()
        return productoCartesiano
    

    def hallarProductoCartesianoDiferencia(self, afd1, afd2):
        productoCartesiano = AFD(self.Sigma, self.Q , self.q0, self.F, self.delta, self.estadosLimbo, self.estadosInaccesibles)
        productoCartesiano.Q = []
        productoCartesiano.q0 = '('+afd1.q0+','+afd2.q0+')'
        productoCartesiano.F = []#es lo que cambia de un producto cartesiano a otro
        productoCartesiano.delta = {}
        productoCartesiano.estadosLimbo = []
        productoCartesiano.estadosInaccesibles = []
        for x in afd1.Q:#x estado del primer automata
            for y in afd2.Q:#y estado del segundo automata
                    productoCartesiano.delta['('+x+','+y+')'] = {}
                    productoCartesiano.Q.append('('+x+','+y+')')
                    if x in afd1.F and y not in afd2.F:
                        productoCartesiano.F.append('('+x+','+y+')')
                    for z in afd1.Sigma:#letra procesando
                        resultado = '('+afd1.delta[x][z]+','+afd2.delta[y][z]+')'
                        productoCartesiano.delta['('+x+','+y+')'][z] = resultado
                        #print('δ(('+x+','+y+'),'+z+') = '+'(δ1('+x+','+z+'),'+'(δ2('+y+','+z+') = '+ resultado)
        productoCartesiano.hallarEstadosLimbo()
        productoCartesiano.hallarEstadosInaccesibles()
        return productoCartesiano

    def hallarProductoCartesianoDiferenciaSimetrica(self, afd1, afd2):
        productoCartesiano = AFD(self.Sigma, self.Q , self.q0, self.F, self.delta, self.estadosLimbo, self.estadosInaccesibles)
        productoCartesiano.Q = []
        productoCartesiano.q0 = '('+afd1.q0+','+afd2.q0+')'
        productoCartesiano.F = []#es lo que cambia de un producto cartesiano a otro
        productoCartesiano.delta = {}
        productoCartesiano.estadosLimbo = []
        productoCartesiano.estadosInaccesibles = []
        for x in afd1.Q:#x estado del primer automata
            for y in afd2.Q:#y estado del segundo automata
                    productoCartesiano.delta['('+x+','+y+')'] = {}
                    productoCartesiano.Q.append('('+x+','+y+')')
                    if (x in afd1.F and y not in afd2.F) or (x not in afd1.F and y in afd2.F):
                        productoCartesiano.F.append('('+x+','+y+')')
                    for z in afd1.Sigma:#letra procesando
                        resultado = '('+afd1.delta[x][z]+','+afd2.delta[y][z]+')'
                        productoCartesiano.delta['('+x+','+y+')'][z] = resultado
                        #print('δ(('+x+','+y+'),'+z+') = '+'(δ1('+x+','+z+'),'+'(δ2('+y+','+z+') = '+ resultado)
        productoCartesiano.hallarEstadosLimbo()
        productoCartesiano.hallarEstadosInaccesibles()
        return productoCartesiano
        
    def hallarProductoCartesiano(self, afd1, afd2, operacion):
        if operacion == "interseccion":
            return self.hallarProductoCartesianoY(afd1, afd2)

        elif operacion == "union":
            return self.hallarProductoCartesianoO(afd1, afd2)

        elif operacion == "diferencia":
            return self.hallarProductoCartesianoDiferencia(afd1, afd2)

        elif operacion == "diferencia simétrica":
            return self.hallarProductoCartesianoDiferenciaSimetrica(afd1, afd2)

        else:
            return print('opcion incorrecta')
        
    def borrarEstadosInaccesibles(self):
        self.hallarEstadosInaccesibles()
        for x in self.estadosInaccesibles:
            if x in self.Q:
                self.Q.remove(x)
            if x in self.estadosLimbo:
                self.estadosLimbo.remove(x)
            if x in self.delta:
                del self.delta[x]

    def simplificarAFD(self, afdInput):
        noEquivalentes = []
        tablaTriangual = {}
        tabla = {}
        for x in range(0,len(afdInput.Q)):
            for y in range(0,len(afdInput.Q)):
                if x<y and afdInput.Q[x] != afdInput.Q[y]:
                    if afdInput.Q[x] not in tablaTriangual:
                        tablaTriangual[afdInput.Q[x]] = {}
                    tablaTriangual[afdInput.Q[x]][afdInput.Q[y]] = ''
                    
                    if ((afdInput.Q[x] in afdInput.F and afdInput.Q[y] in afdInput.F) or (afdInput.Q[x] not in afdInput.F and afdInput.Q[y] not in afdInput.F)): 
                        tabla['('+afdInput.Q[x]+','+afdInput.Q[y]+')'] = {}
                        for z in afdInput.Sigma:
                            tabla['('+afdInput.Q[x]+','+afdInput.Q[y]+')'][z] = '('+afdInput.delta[afdInput.Q[x]][z]+','+afdInput.delta[afdInput.Q[y]][z]+')'
                    else:
                        tablaTriangual[afdInput.Q[x]][afdInput.Q[y]] = '1'
                        noEquivalentes.append('('+afdInput.Q[x]+','+afdInput.Q[y]+')')

        iteracion = 2
        eliminados = False#variable que controla si se a eliminado algo

        while not eliminados: 
            eliminados = True
            for x in tablaTriangual:
                for y in tablaTriangual[x]:
                    for z in afdInput.Sigma:
                        if '('+x+','+y+')' not in noEquivalentes:
                            if tabla['('+x+','+y+')'][z] in noEquivalentes:
                                eliminados = False
                                noEquivalentes.append('('+x+','+y+')')
                                tabla['('+x+','+y+')'][z] = tabla['('+x+','+y+')'][z]+'x'+str(iteracion)
                                tablaTriangual[x][y] = iteracion
            iteracion+=1

        for x in tablaTriangual:
            for y in tablaTriangual[x]:
                if tablaTriangual[x][y] == '':
                    tablaTriangual[x][y] = 'E'

        for x in range(0,len(afdInput.Q)):
            string = ''
            for y in range(0,len(afdInput.Q)):
                if x > y:
                    string = string+str(tablaTriangual[afdInput.Q[y]][afdInput.Q[x]])+','
                elif x == y:
                    string = string+afdInput.Q[x]
                    break
                else:
                    break
            print(string)

        for x in tabla:
            string = (x+'|')
            for y in tabla[x]:
                string = (string+'|') + tabla[x][y]
            print(string)

        return afdInput
    
    def toString(self):
        self.hallarEstadosInaccesibles()
        self.hallarEstadosLimbo()
        print('#!dfa')
        print('#states')
        for x in self.Q:
            print(x)
        print('#initial')
        print(self.q0)
        print('#accepting')
        for x in self.F:
            print(x)
        print('#inaccessible')
        for x in self.estadosInaccesibles:
            print(x)
        print('#limbo')
        for x in self.estadosLimbo:
            print(x)
        print('#transitions')
        for x in self.delta:
            for y in self.delta[x]:
                print(x+':'+y+'>'+self.delta[x][y])
        

    def imprimirAFDSimplificado(self):
        self.hallarEstadosInaccesibles()
        self.hallarEstadosLimbo()
        print('#!dfa')
        print('#states')
        for x in self.Q:
            if x not in self.estadosInaccesibles and x not in self.estadosLimbo:
                print(x)
        print('#initial')
        print(self.q0)
        print('#accepting')
        for x in self.F:
            print(x)
        print('#transitions')
        for x in self.delta:
            for y in self.delta[x]:
                if self.delta[x][y] not in self.estadosLimbo:
                    print(x+':'+y+'>'+self.delta[x][y])
    def exportar(self, nombre):
        self.hallarEstadosInaccesibles()
        self.hallarEstadosLimbo()
        arch = open(nombre+'.dfa','w')
        arch.write('#!dfa\n')
        arch.write('#states\n')
        for x in self.Q:
            arch.write(x+'\n')
        arch.write('#initial\n')
        arch.write(self.q0+'\n')
        arch.write('#accepting\n')
        for x in self.F:
            arch.write(x+'\n')
        arch.write('#inaccessible\n')
        for x in self.estadosInaccesibles:
            arch.write(x+'\n')
        arch.write('#limbo\n')
        for x in self.estadosLimbo:
            arch.write(x+'\n')
        arch.write('#transitions\n')
        for x in self.delta:
            for y in self.delta[x]:
                arch.write(x+':'+y+'>'+self.delta[x][y]+'\n')
        arch.close()
    def procesarListaCadenas(self, listaCadenas,nombreArchivo, imprimirPantalla):
        if nombreArchivo == '':
            nombreArchivo = 'procesamientolistaCadenas'
        estadoActual = self.q0
        string = ''
        arch = open(nombreArchivo+'.txt','w')
        for x in listaCadenas:
            string=string+x+'   '   
            for y in x:
                string = string + '('+estadoActual+',' + y+')'
                estadoActual = self.delta[estadoActual][y]
                #print(estadoActual)
            if estadoActual in self.F:
                string = string+'('+estadoActual+')' +'  '+'si'
            else:
                string = string +'('+estadoActual+')' +'  '+'no'
            if imprimirPantalla:
                print(string)
            arch.write(string+'\n')
            string = ''
            estadoActual = self.q0
        arch.close()


pr = AFD()
pr.contructor("exafd.dfa")
##pr.toString()
##pr.imprimirAFDSimplificado()
#print(pr.estadosLimbo)
pr.hallarEstadosInaccesibles()
print(pr.estadosInaccesibles)
# pr.procesarCadenaConDetalles('aaaa')
# print(pr.delta)
