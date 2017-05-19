import re
import collections

longitud = 60

# Definicion de los tokens
NUM = r'(?P<NUM>\d+)'
MAS = r'(?P<MAS>\+)'
MENOS = r'(?P<MENOS>\-)'
PROD = r'(?P<PROD>\*)'
DIV = r'(?P<DIV>\/)'
POT = r'(?P<POT>\^)'
IPAREN = r'(?P<IPAREN>\()'
DPAREN = r'(?P<DPAREN>\))'
WS = r'(?P<WS>\s+)'

pattern_maestro = re.compile('|'.join((NUM, MAS, MENOS, PROD, DIV, POT, IPAREN, DPAREN, WS)))
Token = collections.namedtuple('Token', ['tipo', 'valor'])

# Generamos los Token
def generar_tokens(pattern, text):
    scanner = pattern.scanner(text)
    for m in iter(scanner.match, None):
        token = Token(m.lastgroup, m.group())
        if token.tipo != 'WS':
            yield token

class Evaluador_Expresion:
    '''
    Implementacion del parcer. Cada metodo es una regla de la gramatica
    '''

    def parse(self, text):
        self.tokens = generar_tokens(pattern_maestro, text)
        self.current_token = None
        self.siguiente_token = None
        self._avanzar()
        return self.expr()

    def _avanzar(self):
        self.current_token, self.siguiente_token = self.siguiente_token, next(self.tokens, None)

    def _aceptar(self, token_tipo):
        # Si existe el siguiente token y coincide con el tipo de token
        if self.siguiente_token and self.siguiente_token.tipo == token_tipo:
            self._avanzar()
            return True
        else:
            return False

    def _esperar(self, token_tipo):
        if not self._aceptar(token_tipo):
            raise SyntaxError('Esperado' + token_tipo)

    def expr(self):
        # regla de la gramatica expr ::= term { (+|-) term}*
        #primero esperamos term acorde a la regla de la gramatica
        valor_expr = self.term()
        #luego si viene + o - tratamos de consumir el lado derecho
        while self._aceptar('MAS') or self._aceptar('MENOS'):
            op = self.current_token.tipo
            derecha = self.term()
            if op == 'MAS':
                valor_expr += derecha
            elif op == 'MENOS':
                valor_expr -= derecha
            else:
                raise SyntaxError('No deberia llegar aqui' + op)
        return valor_expr

    def term(self):
        #regla de la gramatica term ::= factor { (*|/) factor}*
        #primero esperamos factor
        valor_term = self.factor()

        # Analogo al anterior
        while self._aceptar('PROD') or self._aceptar('DIV'):
            op = self.current_token.tipo
            if op == 'PROD':
                valor_term *= self.factor()
            elif op == 'DIV':
                valor_term /= self.factor()
            else:
                raise SyntaxError('No deberia llegar aqui' + op)
        return valor_term

    def factor(self):
        #regla de la gramatica factor::= ext { ^ ext}*
        #Analogo
        valor_factor = self.ext()

        while self._aceptar('POT'):
            op = self.current_token.tipo
            if op == 'POT':
                valor_factor **= self.ext()
            else:
                raise SyntaxError('No deberia llegar aqui' + op)
        return valor_factor

    def ext(self):
        if self._aceptar('NUM'):
            return float(self.current_token.valor)
        elif self._aceptar('IPAREN'):
            valor_expr = self.expr()
            self._esperar('DPAREN')
            return valor_expr
        else:
            raise SyntaxError('Esperamos Numero o parentesis izquierdo')


e = Evaluador_Expresion()
print('parse 2'.ljust(longitud), e.parse('2'))

print('parse 2 ^ 3'.ljust(longitud), e.parse('2 ^ 3'))

print('parse (2 * 7) ^ (3 + 2)'.ljust(longitud), e.parse('(2 * 7) ^ (3 + 2)'))

print('parse 2 ^ 3 * 4 + 5 - 3 / 2'.ljust(longitud), e.parse('2 ^ 3 * 4 + 5 - 3 / 2'))

print('parse ((3 + 5) * 6) / 2 ^ 3'.ljust(longitud), e.parse('((3 + 5) * 6) / 2 ^ 3'))
