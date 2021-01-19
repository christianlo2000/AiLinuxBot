import nlpCommon as nc
import sys
import re

oracion = sys.argv[1]

oracionCor = nc.correctSent(oracion)
print("Oracion: "+oracion)
print("Oracion Corregida: "+str(oracionCor))
