#-*-encoding:utf8-*-

class Analizador:

    def __init__(self):
        self.letra_actual=''
        self.estado_actual=0
        self.valor_lexema=''
        self.aceptacion = False

    def switch(self, estado):
        self.estados = {
        0: self.estado_cero,
        1: self.estado_uno,
        2: self.estado_dos,
        }
        func = self.estados.get(estado, lambda: 'No es un caracter válido' )
        return func()

    def estado_cero(self):
        if int(self.letra_actual) > 0:
            self.estado_actual = 2
            self.valor_lexema = self.valor_lexema + self.letra_actual
        elif int(self.letra_actual) == 0:
            self.estado_actual = 1
            self.valor_lexema = self.valor_lexema + self.letra_actual
        else:
            self.aceptacion = False
            print('No hay transición disponible de estado 0 con ', self.letra_actual)
            self.valor_lexema = ''

    def estado_uno(self):
        print("He aceptado el lexema ", self.valor_lexema)
        self.estado_actual = 0
        self.aceptacion = True

    def estado_dos(self):
        if self.letra_actual.isdigit():
            self.estado_actual = 2
            self.valor_lexema = self.valor_lexema + self.letra_actual
            self.aceptacion = True
        else:
            self.estado_actual = 0
            print("He aceptado el lexema ", self.valor_lexema)

    def analizar(self, cadena):
        cadena = str(cadena)
        for x in cadena:
            self.letra_actual = x
            self.switch(self.estado_actual)
        print("He aceptado el lexema ", self.valor_lexema)

Analizador().analizar('1224aq555')
