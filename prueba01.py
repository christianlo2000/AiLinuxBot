import __pycache__
import sys
import analTextEsp

prueba = cesstag()
oracion = sys.argv[1]

print(prueba.uni.tag(oracion.split()))

