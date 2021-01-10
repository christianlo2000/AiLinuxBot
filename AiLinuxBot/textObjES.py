#####################################################
# Module....: textObjES.py
# Proposito.: definicion de objetos palabra y Texto con respectivos
# 		metodos y atributos para Procesamiento de
#		lenguaje natural
####################################################

class palabra:
	__vocablo = ""
	__tipo = ""
	__significado = ""
	__genero = ""
	__numero = ""

# definimos constructores
def __init__(self,vocablo):
	setVocablo(vocablo)

# metodos set
def setVocablo(self,vocablo):
	self.__vocablo = vocablo

# metodos get
def getVocablo(self):
	return self.__vocablo

# metodos de procesamiento de palabras
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
