#####################################################
# Module....: textProcES.py
# Proposito.: metodos, funciones y datos para procesamiento
# 		de palabras en espanol.
####################################################

def sacarPuntuacion(palabras):
	salida = palabras
	# suprimimos signos de admiracion y preguntas
	salida.replace("?"," ")
	salida.replace("!"," ")
	salida.replace("."," ")
	salida.replace(","," ")
	salida.replace(":"," ")
	salida.replace(";"," ")
	return salida
