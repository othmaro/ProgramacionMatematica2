from ATParser import *
import sys

def main():
    expresion = "a.b"
    if len(sys.argv) > 1:
        expresion = sys.argv[1]
    print "Expresion regular ingresada: ", expresion
    afndObj = deERaAFND(expresion)
    afnd = afndObj.Obtenerafnd()
    afdObj = deAFNDaAFD(afnd)
    afd = afdObj.Obtenerafd()
    afdmin = afdObj.ObteneradfMinimizado()
    if estaInstalado("dot"):
        DibujarGrafica(afd, "afd")
        DibujarGrafica(afnd, "afnd")
        DibujarGrafica(afdmin, "afdmin")
        print "\n Graficas creadas"

if __name__ == '__main__':
    try:
        main()
    except BaseException as e:
        print "\nError:", e
