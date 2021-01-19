#!/usr/bin/python
#######################################################
# script......: aiChatBot.py
# proposito...: primer chatbot con AI hecho por mi. El 
#		mismo ayuda a los usuarios con comandos
#		Linux para neofitos.
######################################################

##### Funciones y Metodos
def procesarConsulta(pregunta):
 	# cargar pregunta en una lista
	cons = []
	patrones = []
	comparacion = []
	posibleCom = []
	cons = pregunta.split()
	# leemos archivo para obtener segunda lista
	fichero = open('listComandos.txt')
	# leemos todos los registros
	for reg in fichero:
		com,patrones,modo,bigrama = reg.split("|")
		# comparamos pregunta con patrones de comandos
		for palabra in cons:
			if palabra in patrones:
				comparacion.append(palabra)
		# validamos el tamano de comparacion para ver si existe coincidencia y es el comando buscado
		if len(comparacion) > 1:
			print "Comando: "+com+". "+modo
			return
		elif len(comparacion) == 1:
			posibleCom.append(com)	
		else:
			posibleCom = []
		# reiniciamos variable comparacion
		comparacion = []
	if (len(posibleCom) == 0):
		# si no se encontro, avisamos que no se pudo encontrar nada
		print("Lo siento, no te puedo ayudar")
	else:
		# imprimimos posibles comandos
		for comanPos in posibleCom:
			print("Posible comando: "+comanPos)
		posibleCom = []		

#Iteramos infinitamente
try:
	while(1):
		pregunta = raw_input("Como te puedo ayudar?\n> ")
		print("por favor, aguarda un momento")
		if (pregunta == "chau" or pregunta == "Chau"):
			print("Espero haberte ayudado.\nChauuu")
			exit(0)
		procesarConsulta(pregunta)
except KeyboardInterrupt:
	print("Interrupcion de ejecucion por teclado.")
	print("Hasta Luego")
	exit(-1)

