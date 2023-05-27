class AFNL():
    def __init__(self):
        self.Sigma = []
        self.Q = []
        self.q0 = ''
        self.F = []
        self.delta = {}
        self.estadosLimbo = []
        self.estadosInaccesibles = []
        self.limbo = False

    def constructor(self, nombreArchivo):
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
                            if ';' not in line:
                                self.delta[line[0:x]][line[x+1]] = line[x+3:len(line.rstrip())]
                            else:
                                self.delta[line[0:x]][line[x+1]] = line[x+3:len(line.rstrip())].split(';')

    def calcularLambdaClausura(self, estado):
        lambdaClausura = []
        if type(estado) == list:
            for i in estado:
                if i not in lambdaClausura:
                    lambdaClausura.append(i) 
                for j in self.delta[i]['$']:
                    if j not in lambdaClausura:
                        lambdaClausura.append(j)
            return lambdaClausura
        
        else:
            lambdaClausura.append(estado)
            for i in self.delta[estado]['$']:
                if i not in lambdaClausura:
                    lambdaClausura.append(i)
            return lambdaClausura
    
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
                    
pr = AFNL()
pr.constructor('exafn$.nfe')
# print(pr.delta)
# print(len(pr.delta['s2']['$']))
# print(pr.delta['s2']['$'])
#print(pr.calcularLambdaClausura(['s0','s1']))
pr.hallarEstadosInaccesibles()

