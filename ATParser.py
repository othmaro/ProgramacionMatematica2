from os import popen
import time
'''
Este es un Parcer para graficar expresiones regulares tanto en su forma no determinista como en
la forma determinista y minimizada, para el caso * representa la clausura de Kleene, |
representa la alternancia y . representa la concatenacion, ademas dentro de las graficas se
encuentra este simbolo ::e:: representa una epsilon transicion
'''

class Automata:
    def __init__(self, lenguaje = set(['0','1'])):
        self.estados = set()
        self.estadoinicial = None
        self.estadosfinales = []
        self.transiciones = dict()
        self.lenguaje = lenguaje

    @staticmethod
    def epsilon():
        return "::e::"

    def ConjuntoDeEstadosIniciales(self, estado):
        self.estadoinicial = estado
        self.estados.add(estado)

    def AgregarEstadoFinal(self, estado):
        if isinstance(estado, int):
            estado = [estado]
            for s in estado:
                if s not in self.estadosfinales:
                    self.estadosfinales.append(s)

    def AgregarTransiciones(self, deestado, aestado, letra):
        if isinstance(letra, str):
            letra = set([letra])
        self.estados.add(deestado)
        self.estados.add(aestado)
        if deestado in self.transiciones:
            if aestado in self.transiciones[deestado]:
                self.transiciones[deestado][aestado] = self.transiciones[deestado][aestado].union(letra)
            else:
                self.transiciones[deestado][aestado] = letra
        else:
            self.transiciones[deestado] = {aestado : letra}

    def AgregarTransiciones_dict(self, transiciones):
        for deestado, aestado in transiciones.items():
            for estado in aestado:
                self.AgregarTransiciones(deestado, estado, aestado[estado])

    def ObtenerTransiciones(self, estado, key):
        if isinstance(estado, int):
            estado = [estado]
        estadotr = set()
        for s in estado:
            if s in self.transiciones:
                for tns in self.transiciones[s]:
                    if key in self.transiciones[s][tns]:
                        estadotr.add(tns)
        return estadotr

    def ObtenerEpsilonClausura(self, encontrarestado):
        todoslosestados = set()
        estados = set([encontrarestado])
        while len(estados)!= 0 :
            estado = estados.pop()
            todoslosestados.add(estado)
            if estado in self.transiciones:
                for tns in self.transiciones[estado]:
                    if Automata.epsilon() in self.transiciones[estado][tns] and tns not in todoslosestados:
                        estados.add(tns)
        return todoslosestados

    def Mostrar(self):
        print "estados: ", self.estados
        print "estado inicial: ", self.estadoinicial
        print "estado final: ", self.estadosfinales
        print "transiciones: "
        for deestado, aestado in self.transiciones.items():
            for estado in aestado:
                for char in aestado[estado]:
                    print " ", deestado,"->", estado, "on '"+char+"'"

    def ObtenerTextoImpreso(self):
        texto = "lenguaje: {" + ", ".join(self.lenguaje) + "}\n"
        texto += "estados: {" + ", ".join(map(str,self.estados)) + "}\n"
        texto += "estado inicial: " + str(self.estadoinicial) + "\n"
        texto += "estado final: {" + ", ".join(map(str,self.estadosfinales)) + "}\n"
        texto += "transiciones:\n"
        conteodelinea = 5
        for deestado, aestado in self.transicioes.items():
            for estado in aestado:
                for char in aestado[estado]:
                    text += "    " + str(deestado) + " -> " + str(estado) + " con '" + char + "'\n"
                    conteodelinea += 1
        return [texto, conteodelinea]

    def NuevoConstructordeNumero(self, numinicial):
        traslaciones = {}
        for i in list(self.estados):
            traslaciones[i] = numinicial
            numinicial += 1
        reconstruir = Automata(self.lenguaje)
        reconstruir.ConjuntoDeEstadosIniciales(traslaciones[self.estadoinicial])
        reconstruir.AgregarEstadoFinal(traslaciones[self.estadosfinales[0]])
        for deestado, aestado in self.transiciones.items():
            for estado in aestado:
                reconstruir.AgregarTransiciones(traslaciones[deestado], traslaciones[estado], aestado[estado])
        return[reconstruir, numinicial]

    def NuevoConstructordeEstadosEquivalentes(self, equivalente, pos):
        reconstruir = Automata(self.lenguaje)
        for deestado, aestado in self.transiciones.items():
            for estado in aestado:
                reconstruir.AgregarTransiciones(pos[deestado], pos[estado], aestado[estado])
        reconstruir.ConjuntoDeEstadosIniciales(pos[self.estadoinicial])
        for s in self.estadosfinales:
            reconstruir.AgregarEstadoFinal(pos[s])
        return reconstruir

    def ObtenerDocumento(self):
        Documento = "digraph afd{\nrankdir=LR\n"
        if len(self.estados) != 0 :
            Documento += "root=s1\nstart [shape=point]\nstart->s%d\n" % self.estadoinicial
            for estado in self.estados:
                if estado in self.estadosfinales:
                    Documento += "s%d [shape=doublecircle]\n" % estado
                else:
                    Documento += "s%d [shapa=circle]\n" % estado
            for deestado, aestado in self.transiciones.items():
                for estado in aestado:
                    for char in aestado[estado]:
                        Documento += 's%d->s%d [label="%s"]\n' % (deestado, estado, char)
        Documento += "}"
        return Documento

class ConstruirAutomata:
    @staticmethod
    def EstructuraBasica(inp):
        estado1 = 1
        estado2 = 2
        basico = Automata()
        basico.ConjuntoDeEstadosIniciales(estado1)
        basico.AgregarEstadoFinal(estado2)
        basico.AgregarTransiciones(1, 2, inp)
        return basico

    @staticmethod
    def EstructuraSuma(a, b):
        [a, m1] = a.NuevoConstructordeNumero(2)
        [b, m2] = b.NuevoConstructordeNumero(m1)
        estado1 = 1
        estado2 = m2
        suma = Automata()
        suma.ConjuntoDeEstadosIniciales(estado1)
        suma.AgregarEstadoFinal(estado2)
        suma.AgregarTransiciones(suma.estadoinicial, a.estadoinicial, Automata.epsilon())
        suma.AgregarTransiciones(suma.estadoinicial, b.estadoinicial, Automata.epsilon())
        suma.AgregarTransiciones(a.estadosfinales[0], suma.estadosfinales[0], Automata.epsilon())
        suma.AgregarTransiciones(b.estadosfinales[0], suma.estadosfinales[0], Automata.epsilon())
        suma.AgregarTransiciones_dict(a.transiciones)
        suma.AgregarTransiciones_dict(b.transiciones)
        return suma

    @staticmethod
    def EstructuraPunto(a, b):
        [a, m1] = a.NuevoConstructordeNumero(1)
        [b, m2] = b.NuevoConstructordeNumero(m1)
        estado1 = 1
        estado2 = m2-1
        punto = Automata()
        punto.ConjuntoDeEstadosIniciales(estado1)
        punto.AgregarEstadoFinal(estado2)
        punto.AgregarTransiciones(a.estadosfinales[0], b.estadoinicial, Automata.epsilon())
        punto.AgregarTransiciones_dict(a.transiciones)
        punto.AgregarTransiciones_dict(b.transiciones)
        return punto

    @staticmethod
    def estructuraEstrela(a):
        [a, m1] = a.NuevoConstructordeNumero(2)
        estado1 = 1
        estado2 = m1
        estrella = Automata()
        estrella.ConjuntoDeEstadosIniciales(estado1)
        estrella.AgregarEstadoFinal(estado2)
        estrella.AgregarTransiciones(estrella.estadoinicial, a.estadoinicial, Automata.epsilon())
        estrella.AgregarTransiciones(estrella.estadoinicial, estrella.estadosfinales[0], Automata.epsilon())
        estrella.AgregarTransiciones(a.estadosfinales[0], estrella.estadosfinales[0], Automata.epsilon())
        estrella.AgregarTransiciones(a.estadosfinales[0], a.estadoinicial, Automata.epsilon())
        estrella.AgregarTransiciones_dict(a.transiciones)
        return estrella

class deERaAFND:
    def __init__(self, expresion):
        self.estrella = '*'
        self.suma = '|'
        self.punto = '.'
        self.iparen = '('
        self.dparen = ')'
        self.operadores = [self.suma, self.punto]
        self.expresion = expresion
        self.alfabeto = [chr(i) for i in range(65,91)]
        self.alfabeto.extend([chr(i) for i in range(97,123)])
        self.alfabeto.extend([chr(i) for i in range(48,58)])
        self.construirafnd()

    def Obtenerafnd(self):
        return self.afnd

    def Mostrarafnd(self):
        self.afnd.Mostrar()

    def construirafnd(self):
        lenguaje = set()
        self.pila = []
        self.automata = []
        previo = "::e::"
        for char in self.expresion:
            if char in self.alfabeto:
                lenguaje.add(char)
                if previo != self.punto and (previo in self.alfabeto or previo in [self.dparen, self.estrella]):
                    self.AgregarOperadorAPila(self.punto)
                self.automata.append(ConstruirAutomata.EstructuraBasica(char))
            elif char == self.iparen:
                if previo != self.punto and (previo in self.alfabeto or previo in [self.dparen, self.estrella]):
                    self.AgregarOperadorAPila(self.punto)
                self.pila.append(char)
            elif char == self.dparen:
                if previo in self.operadores:
                    raise BaseException("Error '%s' despues '%s'" % (char, previo))
                while(1):
                    if len(self.pila) == 0:
                        raise BaseException("Error '%S'. pila vacia" % char)
                    o = self.pila.pop()
                    if o == self.iparen:
                        break
                    elif o in self.operadores:
                        self.processOperator(o)
            elif char == self.estrella:
                if previo in self.operadores or previo == self.iparen or previo == self.estrella:
                    raise BaseException("Error '%s' despues '%s'" % (char, previo))
                self.processOperator(char)
            elif char in self.operadores:
                if previo in self.operadores or previo == self.iparen:
                    raise BaseException("Error '%s' despues '%s'" % (char, previo))
                else:
                    self.AgregarOperadorAPila(char)
            else:
                raise BaseException("Simbolo '%s' no esta definido" % char)
            previo = char
        while len(self.pila) != 0:
            op = self.pila.pop()
            self.processOperator(op)
        if len(self.automata) > 1:
            print self.automata
            raise BaseException("Expresion regular tuvo un error")
        self.afnd = self.automata.pop()
        self.afnd.lenguaje = lenguaje

    def AgregarOperadorAPila(self, char):
        while(1):
            if len(self.pila) == 0:
                break
            top = self.pila[len(self.pila)-1]
            if top == self.iparen:
                break
            if top == char or top == self.punto:
                op = self.pila.pop()
                self.processOperator(op)
            else:
                break
        self.pila.append(char)

    def processOperator(self, operador):
        if len(self.automata) == 0:
            raise BaseException("Error '%s'. Pila esta vacia" % operador)
        if operador == self.estrella:
            a = self.automata.pop()
            self.automata.append(ConstruirAutomata.estructuraEstrela(a))
        elif operador in self.operadores:
            if len(self.automata) < 2:
                raise BaseException("Error '%s', operacion inadecuada" % operador)
            a = self.automata.pop()
            b = self.automata.pop()
            if operador == self.suma:
                self.automata.append(ConstruirAutomata.EstructuraSuma(b,a))
            elif operador == self.punto:
                self.automata.append(ConstruirAutomata.EstructuraPunto(b,a))

class deAFNDaAFD:
    def __init__(self, afnd):
        self.Construirafd(afnd)
        self.minimizar()

    def Obtenerafd(self):
        return self.afd

    def ObteneradfMinimizado(self):
        return self.afdmin

    def Mostrarafd(self):
        self.afd.Mostrar()

    def Mostrarminafd(self):
        self.afdmin.Mostrar()

    def Construirafd(self, afnd):
        todoslosestados = dict()
        epsilonclausura = dict()
        conteo = 1
        estado1 = afnd.ObtenerEpsilonClausura(afnd.estadoinicial)
        epsilonclausura[afnd.estadoinicial] = estado1
        afd = Automata(afnd.lenguaje)
        afd.ConjuntoDeEstadosIniciales(conteo)
        estados = [[estado1, conteo]]
        todoslosestados[conteo] = estado1
        conteo += 1
        while len(estados) != 0:
            [estado, deindice] = estados.pop()
            for char in afd.lenguaje:
                estadostr = afnd.ObtenerTransiciones(estado, char)
                for s in list(estadostr)[:]:
                    if s not in epsilonclausura:
                        epsilonclausura[s] = afnd.ObtenerEpsilonClausura(s)
                    estadostr = estadostr.union(epsilonclausura[s])
                if len(estadostr) != 0:
                    if estadostr not in todoslosestados.values():
                        estados.append([estadostr, conteo])
                        todoslosestados[conteo] = estadostr
                        aindice = conteo
                        conteo += 1
                    else:
                        aindice = [k for k, v in todoslosestados.iteritems() if v == estadostr][0]
                    afd.AgregarTransiciones(deindice, aindice, char)
        for valor, estado in todoslosestados.iteritems():
            if afnd.estadosfinales[0] in estado:
                afd.AgregarEstadoFinal(valor)
        self.afd = afd

    def minimizar(self):
        estados = list(self.afd.estados)
        n = len(estados)
        unchecked = dict()
        conteo = 1
        distinguido = []
        equivalente = dict(zip(range(len(estados)), [{s} for s in estados]))
        pos = dict(zip(estados, range(len(estados))))
        for i in range(n-1):
            for j in range(i+1, n):
                if not ([estados[i], estados[j]] in distinguido or [estados[j], estados[i]] in distinguido):
                    eq = 1
                    aappend = []
                    for char in self.afd.lenguaje:
                        s1 = self.afd.ObtenerTransiciones(estados[i], char)
                        s2 = self.afd.ObtenerTransiciones(estados[j], char)
                        if len(s1) != len(s2):
                            eq = 0
                            break
                        if len(s1) > 1:
                            raise BaseException("afd con transiciones multiples")
                        elif len(s1) == 0:
                            continue
                        s1 = s1.pop()
                        s2= s2.pop()
                        if s1 != s2:
                            if [s1, s2] in distinguido or [s2,s1] in distinguido:
                                eq = 0
                                break
                            else:
                                aappend.append([s1,s2,char])
                                eq = -1
                    if eq == 0:
                        distinguido.append([estados[i], estados[j]])
                    elif eq == -1:
                        s = [estados[i], estados[j]]
                        s.extend(aappend)
                        unchecked[conteo] = s
                        conteo += 1
                    else:
                        p1 = pos[estados[i]]
                        p2 = pos[estados[j]]
                        if p1 != p2:
                            st = equivalente.pop(p2)
                            for s in st:
                                pos[s] = p1
                            equivalente[p1] = equivalente[p1].union(st)
        newFound = True
        while newFound and len(unchecked) > 0:
            newFound = False
            aremover = set()
            for p, pair in unchecked.items():
                for tr in pair[2:]:
                    if [tr[0], tr[1]] in distinguido or [tr[1], tr[0]] in distinguido:
                        unchecked.pop(p)
                        distinguido.append([pair[o], pair[1]])
                        newFound = True
                        break
        for pair in unchecked.values():
            p1 = pos[pair[0]]
            p2 = pos[pair[1]]
            if p1 != p2:
                st = equivalente.pop(p2)
                for s in st:
                    pos[s] = p1
                equivalente[p1] = equivalente[p1].union(st)
        if len(equivalente) == len(estados):
            self.afdmin = self.afd
        else:
            self.afdmin = self.afd.NuevoConstructordeEstadosEquivalentes(equivalente, pos)


def DibujarGrafica(automata, file = ""):
    f = popen(r"dot -Tpng -o graph%s.png" % file, 'w')
    try:
        f.write(automata.ObtenerDocumento())
    except:
        raise BaseException("Error creando la grafica")
    finally:
        f.close()

def estaInstalado(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program) or is_exe(program+".exe"):
            return True
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file) or is_exe(exe_file+".exe"):
                return True
    return False
