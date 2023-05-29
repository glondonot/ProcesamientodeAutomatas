class AFNL():
    def __init__(self):
        self.Sigma = []
        self.Q = []
        self.q0 = ''
        self.F = []
        self.delta = {}
        self.estadosInaccesibles = []

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
                            self.delta[line[0:x]][line[x+1]] = line[x+3:len(line.rstrip())].split(';')

    def calcularLambdaClausura(self, estado):
        lambdaClausura = []
        if type(estado) == list:
            for x in estado:
                lambdaClausura.append(x)
                if '$' in self.delta[x]:
                    for y in self.delta[x]['$']:
                        if y not in lambdaClausura:
                            lambdaClausura.append(y)
                    if len(lambdaClausura) > 1:
                        for i in range(1,len(lambdaClausura)):
                            for j in range(len(self.Q)):
                                if '$' in self.delta[lambdaClausura[i]]:
                                    for k in self.delta[lambdaClausura[i]]['$']:
                                        if k not in lambdaClausura:
                                            lambdaClausura.append(k) 
            return lambdaClausura
        else:
            lambdaClausura.append(estado)
            if '$' in self.delta[estado]:
                for i in self.delta[estado]['$']:
                    if i not in lambdaClausura:
                        lambdaClausura.append(i)
                if len(lambdaClausura) > 1:
                    for i in range(1,len(lambdaClausura)):
                        for j in range(len(self.Q)):
                            if '$' in self.delta[lambdaClausura[i]]:
                                for k in self.delta[lambdaClausura[i]]['$']:
                                    if k not in lambdaClausura:
                                        lambdaClausura.append(k)                                
            return lambdaClausura
    
    def hallarEstadosInaccesibles(self):
        self.Sigma.append('$')
        for i in self.Q:
            self.estadosInaccesibles.append(i)
        for j in self.Q:
            for k in self.Sigma:
                if len(self.estadosInaccesibles) == 0:
                    break
                if k in self.delta[j]:
                    for l in range (0,len(self.delta[j][k])):
                        if self.delta[j][k][l] in self.estadosInaccesibles:
                            self.estadosInaccesibles.remove(self.delta[j][k][l])
        self.Sigma.remove('$')
        return self.estadosInaccesibles
    
    def toString(self):
        self.hallarEstadosInaccesibles()
        print('#!dfa')
        print('#alphabet')
        for i in self.Sigma:
            print(i)
        print('#states')
        for x in self.Q:
            print(x)
        print('#initial')
        print(self.q0)
        print('#accepting')
        for x in self.F:
            print(x)
        print('#transitions')
        for x in self.delta:
            for y in self.delta[x]:
                if len(self.delta[x][y]) == 1:
                    print(x+':'+y+'>'+self.delta[x][y][0])
                else:
                    print(x+':'+y+'>',end='')
                    for z in range(0,len(self.delta[x][y])):
                        print(self.delta[x][y][z],end='')
                        if z != len(self.delta[x][y])-1:
                            print(';',end='')
                    print('')
        print('#inaccessible')
        for x in self.estadosInaccesibles:
            print(x)

    def imprimirAFNLSimplificado(self):
        estadosInaccesibles = self.hallarEstadosInaccesibles()
        print(estadosInaccesibles)
        print('#!dfa')
        print('#alphabet')
        for i in self.Sigma:
            print(i)
        print('#states')
        for x in self.Q:
            if x not in estadosInaccesibles:
                print(x)
        print('#initial')
        print(self.q0)
        print('#accepting')
        for x in self.F:
            print(x)
        print('#transitions')
        for x in self.delta:
            if x not in estadosInaccesibles:
                for y in self.delta[x]:
                    print(x+':'+y+'>'+self.delta[x][y])

    def exportar(self, nombre):
        arch = open(nombre+'.nfe','w')
        arch.write('#!nfe\n')
        arch.write('#alphabet\n')
        for i in self.Sigma:
            arch.write(i+'\n')
        arch.write('#states\n')
        for x in self.Q:
            arch.write(x+'\n')
        arch.write('#initial\n')
        arch.write(self.q0+'\n')
        arch.write('#accepting\n')
        for x in self.F:
            arch.write(x+'\n')
        arch.write('#transitions\n')
        for x in self.delta:
            for y in self.delta[x]:
                if len(self.delta[x][y]) == 1:
                    arch.write(x+':'+y+'>'+self.delta[x][y][0]+'\n')
                else:
                    arch.write(x+':'+y+'>')
                    for z in range(0,len(self.delta[x][y])):
                        arch.write(self.delta[x][y][z])
                        if z != len(self.delta[x][y])-1:
                            arch.write(';')
                    arch.write('\n')
        arch.close()
    
    def AFN_LambdaToAFN(self, afnl):
        for i in afnl.delta:
            lambdaC = afnl.calcularLambdaClausura(i)
            print('\nLambda Clausura de',i+':',lambdaC)
            for j in afnl.Sigma:
                print('Δ`('+i+','+j+') = λ[Δ(λ['+i+'],'+j+')] = λ[Δ(',lambdaC,','+j+')] =  λ', end='')
                s = []
                for k in lambdaC:
                    if j in self.delta[k]:
                        if len(afnl.delta[k][j]) > 1:
                            for z in range(len(afnl.delta[k][j])):
                                if afnl.delta[k][j][z] not in s:
                                    s.append(afnl.delta[k][j][z])
                        else:
                            s.append(afnl.delta[k][j][0])
                print(s,'= ', end='')
                print(list(set(afnl.calcularLambdaClausura(s))))
        return
    




pr = AFNL()
pr.constructor('ex2afn$.nfe')
# print(pr.delta)
# print(len(pr.delta['s2']['$']))
# print(pr.delta['s2']['$'])
# print(pr.calcularLambdaClausura(['s0','s1']))
# print(pr.hallarEstadosInaccesibles())
# pr.toString()
# pr.exportar('p')
# print(pr.calcularLambdaClausura('s0'))
pr.AFN_LambdaToAFN(pr)
# print(pr.delta)