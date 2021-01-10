#!/usr/bin/python
#######################################################################
# script...: aiLinBot.py
# Proposito: chatBot con IA para ayudar con comandos linux a neofitos
######################################################################		
import sys
import os
import subprocess
import time
import random
import datetime
import telepot
from telepot.loop import MessageLoop
#import telegram
import calendar
import string
from textProcES import sacarPuntuacion

#global respuestaAyuda = False
# Funciones y Metodos
# metodo manejo telegram chat
def handle(msg):
	chat_id = msg['chat']['id']
	pregunta = msg['text']
	print('pregunta: %s' % pregunta)
	print('Chat Id: %s' % chat_id)
	# analizamos si el mensaje es saludo
	if (esSaludo(pregunta.lower()) == False): 
		# preguntamos si es un agradecimiento
		#if (esGracias(pregunta)):
		# procesamos pregunta
		procesarConsulta(pregunta)
		time.sleep(1)
		# hacemos una pausa de 1 segundo y preguntamos si necesita mas
		bot.sendMessage(chat_id,"Te puedo ayudar en algo mas?")
		print("Te puedo ayudar en algo mas?")
		respuestaAyuda = True
	
# Metodo destroy para finalizar ejecucion
def destroy():
	# rutina invocada para cerrar programa
	print("Fin de ejecucion script")
	os._exit(0)
	exit(0)

# Analizar pregunta
def procesarConsulta(pregunta):
 	# cargar pregunta en una lista
	cons = []
	patrones = []
	comparacion = []
	posibleCom = []
	pregunta1 = pregunta.lower()
	cons = pregunta1.split()
	# leemos archivo para obtener segunda lista
	fichero = open('listComandos.txt')
	# leemos todos los registros
	for reg in fichero:
		com,patrones,modo,bigrama = reg.split("|")
		# antes de comparar patrones, validamos pregunta versus bigramas
		if bigrama == pregunta:
			# si encontramos bigrama, asumimos que tenemos respuesta
			msg = "Comando: "+com+". "+modo
			bot.sendMessage(chat_id,msg,parse_mode='Markdown')
			print(msg+" - por bigrama")
			comparacion = []
			return
		# comparamos pregunta con patrones de comandos
		for palabra in cons:
			try:
				patrones.index(palabra)
				print("agregamos: "+palabra)
				comparacion.append(palabra)
			except:
				print("no encontre")
		# validamos el tamano de comparacion para ver si existe coincidencia y es el comando buscado
		if len(comparacion) > 1:
			#print "Comando: "+com+". "+modo
			msg = "Comando: "+"*"+com+"*"+". "+modo
			bot.sendMessage(chat_id,msg,parse_mode='Markdown')
			print(msg)
			comparacion = []
			return
		elif len(comparacion) == 1:
			posibleCom.append(com)	
		else:
			#posibleCom = []
			# reiniciamos variable comparacion
			comparacion = []
	if (len(posibleCom) == 0):
		# si no se encontro, avisamos que no se pudo encontrar nada
		#print("Lo siento, no te puedo ayudar")
		bot.sendMessage(chat_id,"Lo siento, no te puedo ayudar")
		print("Lo siento, no te puedo ayudar")
		comparacion = []
	else:
		# imprimimos posibles comandos
		for comanPos in posibleCom:
			#print("Posible comando: "+comanPos)
			msg = "Posible comando: "+"*"+comanPos+"*"
			bot.sendMessage(chat_id,msg,parse_mode='Markdown')
			print(msg)
		posibleCom = []	
	comparacion = []
	posibleCom = []
# funcion validar agradecimiento
def esGracias(pregunta1):
	gracias = ['no','gracias','muchas gracias']
# funcion saludo
def esSaludo(pregunta1):
	pregunta = []
	# definimos lista de saludos
	saludos = ['hola','que tal','como va','como estas','buenas tardes','buen dia','buenas noches']
	# suprimimos signos de admiracion y pregunta
	pregunta2 = sacarPuntuacion(pregunta1)
	pregunta = pregunta2.split()
	# validamos si la pregunta en realidad es un saludo
	for palabras in pregunta:
		if palabras in saludos:
			bot.sendMessage(chat_id,"Hola, todo bien y vos? En que puedo ayudarte?")
			print("Hola, todo bien y vos? En que puedo ayudarte?")
			respuestaAyuda = False
			return True
	return False

#def sacarPuntuacion(palabras):
	#salida = palabras
	# suprimimos signos de admiracion y pregunta
        #salida.replace("?"," ")
        #salida.replace("!"," ")
        #salida.replace("."," ")
        #salida.replace(","," ")
        #salida.replace(":"," ")
        #salida.replace(";"," ")
	#return salida
 
##############MAIN##########################
bot = telepot.Bot('955248895:AAF5qmVshW3NRGj1pgB4Zolk5y6Jm0TMSH4')
#bot = telepot.Bot('775050361:AAGpjJ7CY8crIpcU0LFCO1jphAmSymWtC7E')
bot.getMe()
bot.message_loop(handle)
MessageLoop(bot,handle).run_as_thread()
chat_id = '750975992'
bot.sendMessage(chat_id,"Reiniciado aiLinBot AIChatBot Raspberry pi 3")
print ("Reiniciado aiLinBot AIChatBot Raspberry pi 3")
print ('Escuchando mensajes ...')
while 1:
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		#print 'Fin de ejecucion script'
		#exit(0)
		# invocamos rutina para cerrar programa
		destroy()
