#!/usr/bin/python3
#######################################################
# script......: linuxComHelper.py
# proposito...: chatbot con AI hecho por mi. el idioma es 
#		el ingles dado que no consegui procesar
#		texto en español (NLP) 
# Status......: operativo pero con bugs y puntos de mejora
######################################################
from six.moves import input
import urllib.request
import nltk
from  nltk.text import ConcordanceIndex
from nltk.stem.porter import *
import re 
import os
from nltk import UnigramTagger as ut
from nltk import BigramTagger as bt
from pickle import dump,load
import sys
import time
import telepot
import datetime
from telepot.loop import MessageLoop
import nlpCommon as nc # libreria hecha por mi para mejorar texto en ingles e identificar tipos de palabras especificas
# Funcion Handle de chatbot de telegram
def handle(msg):
	chat_id = msg['chat']['id']
	pregunta = msg['text']
	print('pregunta: %s' % pregunta)
	print('Chat Id: %s' % chat_id)
	# analizamos si el mensaje es saludo
	#if (pregunta.lower() == "bye" or pregunta.lower() == "see you"):
	if (isGreetings(pregunta) == False):
		# consulto por idioma de la pregunta
		idioma = nc.getIdioma(pregunta)
		if (idioma != 'en'):
                	bot.sendMessage(chat_id,"I'm sorry, I'm a chatbot that only speak english languague")
                	return
		# procesamos consulta
		procesarConsultaMasiva(pregunta)
# grabar log 
def grabarLog(registro):
	# obtengo fecha y hora para registrar
	fechaHora = datetime.datetime.now()
	# abrimos archivo
	logFile = open("/home/pi/python/AiLinuxBot/AiLinuxBot/logs/logChat.txt","a")
	regCom = str(fechaHora)+"|"+registro+'\n'
	logFile.write(regCom)
	logFile.close()
# funciones de saludo (funciona con bugs y necesita mas saludos)
def isGreetings(pregunta):
	saludos = open("/home/pi/python/AiLinuxBot/AiLinuxBot/greetings/greetings.txt","r")
	for registro in saludos:
		entrada,salida = registro.split("|")
		if (pregunta.lower() == entrada.lower()):
			# mando mensaje de respuesta
			bot.sendMessage(chat_id,salida)
			return True
		# vemos si match usando expresiones regulares
		if (re.match(entrada,pregunta,re.IGNORECASE)):
			bot.sendMessage(chat_id,salida)
	return False
#### Funciones y Metodos ######################
# variables globales
# funcion para cargar corpus uno por archivo de un directorio
def cargarCorporaFromDir(directorio):
	# lista de todos los nombres de corpus
	global corpusList
	global comandList
	global smartList
	i = 0	
	for archivo in os.listdir(directorio):
		# validamos si el ombre del archivo cmienza con "."
		if (archivo[0] =="."):
			continue
		# leemos archivo por archivo
		archCorp = directorio+"/"+archivo
		archCorp1 = open(archCorp,"r")
		# leemos archivo linea a linea
		fileInfo = ""
		print("Archivo a procesar: "+archCorp)
		# usamos variable i para identificar linea 4, y poblar el smartList
		i = 0
		for registro in archCorp1:
			# reemplazamos los () por espacios
			clean_texto = nc.clean_text1(registro)
			#registro3 = registro2.lower()
			registro3 = clean_texto.lower()
			#print("Registro3: "+registro3)
			fileInfo = fileInfo + registro3
			# esta parte es para hacer una busqueda inteligente de la linea 4 donde tiene el resumen de funcion del corpus
			if (i == 3):
				# antes de tokenizar, elimino el nombre del comando
				textoReduc = ' '.join(registro3.split()[1:])
				#token1 = nltk.word_tokenize(registro3)
				token1 = nltk.word_tokenize(textoReduc)
				textSmart = nltk.Text(token1)
				smartList.append(textSmart)
			i += 1
		# cerramos archivo
		archCorp1.close()
		# tokenizamos
		tokens = nltk.word_tokenize(fileInfo)
		textCorp = nltk.Text(tokens)
		corpusList.append(textCorp)
		comandList.append(archivo[0:len(archivo)-4])	

# funcion principal para procesar consulta del usuario
# procesar consulta masiva
def procesarConsultaMasiva(pregunta1):
	# verificamos la pregunta que este correctamente redactada
	pregunta = nc.correctSent(pregunta1)
	if (pregunta.lower() != pregunta1.lower()):
		msg = "You want to say: "+pregunta+". Wait a moment, please."
		bot.sendMessage(chat_id,msg)
	# hacemos analisis sintactico y solo dejamos verbo y objeto
	listaVerbObj,listaFunc = getObjAndVerb(pregunta.lower())
	print(listaVerbObj)
	print(listaFunc)
	# realizamos smart analisis antes de valdir todo el corpus. Analizamos horacion principal de descripcion del comando.
	listTotSmart = []
	listTotOcur = []
	# listas con aquellos con una coincidencia
	listTotSmartB = []
	j = 0
	for smartC in smartList:
		#totSStat = analisisSmartCorpus(smartC,listaVerbObj,listaFunc)
		totSStat = analisisMoreSmartCorpus(smartC,listaVerbObj,listaFunc)
		print("corpus: "+str(smartC)+" totOcu: "+str(totSStat))
		# si encontramos comando con 2 o mas  ocurrencias, es el buscado
		if (totSStat >= 2):
			# encontramos un candidato a comando
			listTotSmart.append(comandList[j])
			listTotOcur.append(totSStat)
			# debug
			#print("comando: "+comandList[j]+" totStat: "+str(totSStat))
		# agregamos lista de 1 elemento como segundo parametro de busqueda
		if (totSStat == 1):
			listTotSmartB.append(comandList[j])
		j += 1
	# analizamos los candidatos encontrados
	maxS = 1
	masDe1 = False # variable para determinar si hay candidato unico
	l = 0
	maxPos = 0
	for total in listTotOcur:
		# analizamos si encontramos un segundo o tercer maximo
		if (total == maxS):
			masDe1 = True
		if (total > maxS): # hay un nuevo unico maximo
			masDe1 = False
			maxPos = l
			maxS = total
		# sumamos contador indice de listas
		l += 1
	# verificamos si tenemos un unico comando
	if (masDe1 == False and len(listTotSmart) > 0):
		# encontramos comando unico candidato
		infoLin = "I'm sure!! Command that you need is: "+listTotSmart[maxPos]
		bot.sendMessage(chat_id,infoLin,parse_mode='Markdown')
		# grabamos log
		regLog = pregunta+"|"+str(listaVerbObj)+"|"+str(listaFunc)+"|"+listTotSmart[maxPos]
		grabarLog(regLog)
		addInfo = "for more information, please consult: https://en.wikipedia.org/wiki/"+listTotSmart[maxPos]
		bot.sendMessage(chat_id,addInfo)
		return 
	# si la lista no esta vacia, acote busqueda, solo busco comandos de la lista
	if (len(listTotSmart) > 0):
		if (esComandoBuscado(listTotSmart,listaVerbObj,listaFunc,pregunta) == True):
			return 
	# validamos lista con una sola coincidencia
	if (len(listTotSmartB) > 0):
		if (esComandoBuscado(listTotSmartB,listaVerbObj,listaFunc,pregunta) == True):
			return 
	# analizamos oracion por oracion buscando coincidencia de mas de una palabra
	k = 0
	listTotS = []
	for corpusS in corpusList:
		corpusS_sent = str(corpusS).split('\n')
		# buscamos los patrones oracion por oracion
		for ora in corpusS_sent:
			#totStatS = analisisStatCorpus(ora,listaVerbObj,listaFunc)
			totStatS = analisisMoreSmartCorpus(ora,listaVerbObj,listaFunc)
			# la logica simplemente tiene que detectar coincidencias >= 2 x oracion, de ser asi, asumimos que es el comando
			#print("comando: "+comandList[k]+" totStatS: "+str(totStatS))
			if (totStatS >= 2):
				infoLin = "I'm not sure, but I'm almost sure, command that you need is: "+comandList[k]
				bot.sendMessage(chat_id,infoLin,parse_mode='Markdown')
				# grabamos log
				regLog = pregunta+"|"+str(listaVerbObj)+"|"+str(listaFunc)+"|"+comandList[k]
				grabarLog(regLog)
				addInfo = "for more information, please consult:: https://en.wikipedia.org/wiki/"+comandList[k]
				bot.sendMessage(chat_id,addInfo)
				return
			k += 1
	# barremos los corpus para detectar coincidencias, obteniendo estadisticas en bruto de las palabras.
	listTot = []
	for corpus in corpusList:
		#totStat = analisisStatCorpus(corpus,listaVerbObj,listaFunc)
		totStat = analisisMoreSmartCorpus(corpus,listaVerbObj,listaFunc)
		#print(str(corpus))
		listTot.append(totStat)
	i = 0
	max = 0
	maxCom = "no hay"
	for comando in comandList:
		if (listTot[i] > max):
			max = listTot[i]
			maxCom = comando
		i += 1 
	print("Linux Command that you search is: "+maxCom)
	if (max == 0):
		# no se encontro comando
		infoLin = "I'm sorry, I can't find a comand for your question"
	else:
		infoLin = "I guess but I'm not sure, command that you need is: "+maxCom
	bot.sendMessage(chat_id,infoLin,parse_mode='Markdown')
	# grabamos log
	regLog = pregunta+"|"+str(listaVerbObj)+"|"+str(listaFunc)+"|"+maxCom
	grabarLog(regLog)
	if (maxCom != "no hay"):
		addInfo = "for more information, please consult:: https://en.wikipedia.org/wiki/"+maxCom
		bot.sendMessage(chat_id,addInfo)
# funcion para obtener comando correcto
def esComandoBuscado(listTotSmart,listaVerbObj,listaFunc,pregunta):
	m = 0
	totmax = 0
	posMax = ""
	for comando in listTotSmart:
        # ahora que tengo comando hago referencia al corpus a traves de otra lista
		corpo_ora1 = corpusList[comandList.index(comando)]
		print("corpo_ora1: "+str(corpo_ora1))
 		# hago analisis de estadisticas de palabras linea por liena
		totStatC = analisisSmartCorpus(corpo_ora1,listaVerbObj,listaFunc)
		if (totStatC > totmax):
			totmax = totStatC
			posMax = m
		print("totStatGral: "+str(totStatC))
		m += 1
	# obtenemos el maximo
	# validamos que se haya encontrado maximo
	if (posMax != ""):
		infoLin = "I'm almost sure command that you help is: "+listTotSmart[posMax]
		bot.sendMessage(chat_id,infoLin,parse_mode='Markdown')
		# grabamos log
		regLog = pregunta+"|"+str(listaVerbObj)+"|"+str(listaFunc)+"|"+listTotSmart[posMax]
		comando = listTotSmart[posMax]
		grabarLog(regLog)
		if (len(listTotSmart) > 1):
			# comandos que tuvieron cerca
			# previo eliminamos de la lista el comando encontrado
			del listTotSmart[posMax]
			infoAdd = "Besides, You can see the following commands: "+str(listTotSmart)
			bot.sendMessage(chat_id,infoAdd)
		addinfo = "for more information, please consult:: https://en.wikipedia.org/wiki/"+comando
		bot.sendMessage(chat_id,addinfo)
		return True
	return False

# funcion para realizar analisis sintactico de la pregunta
def getObjAndVerb(oracion):
	listaSalPal = []
	listaSalFunc = []
	# hacemos analisis sintactico de la oracion
	salida = nltk.pos_tag(oracion.split())
	print("Ora Anal: "+str(salida))
	# barro para quedarme solo con NN y VB y VBP para analisis
	for pal,func in salida:
		# validamos si es verbo modal, para eliminarlo del analisis
		if (func in ["VBP","VB"]):
			if (nc.isModalVerb(pal)):
				# salteamos palabra
				continue
		# validamos si es pronombre
		if (func in ["NNS","NN"]):
			if (nc.isPronoun(pal)):
				continue
		# valido si es una stopword
		if (nc.isMyStopWord(pal)):
			continue
		if (func == "VBP" or func == "VB" or func == "NN" or func == "NNS" or func == "JJ"):
			# lo agregamos  a la lista de salida
			listaSalPal.append(pal)
			listaSalFunc.append(func)
		# buscamos sinonimos para los verbos
		if (func == "VBP" or func == "VB" or func == "JJ" or func == "NN" or func == "NNS"):
			# buscamos sinonimos
			listSin = []
			listSin = getSinonimo(pal)
			if (len(listSin) > 0):
				# barremos lista agregando sinonimos
				for sin1 in listSin:
					# validamos que no este repetido
					if (existeEnlista(listaSalPal,sin1) == False):
						# palabra no existe, la agregamos
						listaSalPal.append(sin1)
						listaSalFunc.append(func)
		# si son verbos, agregamos la forma con "s" final
		# pero antes validamos si es prononbre, en caso afirmativo, no agregamos plurales o singulares
		if (nc.isPronoun(pal) == False):
			if (func == "VB" or func == "VBP"):
				listaSalPal.append(pal+"s")
				listaSalFunc.append(func)
			# obtenemos singular
			if (func == "NNS"):
				listaSalPal.append(nc.getSingular(pal))
				listaSalFunc.append("NN")
			# obtenemos plural para sustantivos
			if (func == "NN"):
				listaSalPal.append(nc.getPlural(pal))
				listaSalFunc.append("NNS")
	print("Listamos lista de palabras de pregunta: "+str(listaSalPal))
	return listaSalPal,listaSalFunc
# verificamos si palabra existe ne lista
def existeEnlista(listaSalPal,sin1):
	for pal in listaSalPal:
		if (pal.lower() == sin1.lower()):
			return True
	return False
# analisis de smartList[]
def analisisSmartCorpus(corpus,listaPal,listaFunc):
	totOcurGral = 0
	i = 0
	#print("Estoy en analisisSmarCorpus. corpus: "+str(corpus))
	for pal in listaPal:
		# validamos que tengamos verbo y sustantivo (objeto)
		totOcurGral = totOcurGral + corpus.count(pal)
	return totOcurGral
def analisisMoreSmartCorpus(corpus,listaPal,listaFunc):
	totOcurGral = 0
	totOcurVerb = 0
	totOcurSust = 0
	i = 0
	#print("Estoy en analisisSmarCorpus. corpus: "+str(corpus))
	for pal in listaPal:
		# validamos que tengamos verbo y sustantivo (objeto)
		if (listaFunc[i] in ["VB","JJ","VBP"]):
			totOcurVerb = totOcurVerb + corpus.count(pal)
		if (listaFunc[i] in ["NN","NNS"]):
			totOcurSust = totOcurSust + corpus.count(pal)
		i += 1
	if (totOcurVerb > 0 and totOcurSust > 0):
		# sumamos totales
		totOcurGral = totOcurVerb + totOcurSust
	return totOcurGral

# analiza estadisticas de cantidad de repeticiones por palabra corpus
def analisisStatCorpus(corpus,listaPal,listaFunc):
	totOcurGral = 0
	# barremos la lista de palabras
	i = 0
	for pal in listaPal:
		# pregunto si es verbo, multiplica ocurrencia
		if (listaFunc[i] == "VB"):
			# multiplico ocurrencia dado que resalto accion de comando
			totOcurGral = totOcurGral +(corpus.count(pal)*5)
		else:
			totOcurGral = totOcurGral + corpus.count(pal)
		i += 1
	return totOcurGral	
# obtener lista de sinonimos
def getSinonimo(pal):
	listSin = []
	archSin = open("/home/pi/python/AiLinuxBot/AiLinuxBot/synonym/synonym.txt","r")
	for reg1 in archSin:
		# suprimimos el enter
		reg = reg1.strip('\n')
		if (reg.find(pal) > -1):
			listSin = reg.split("|")
			#chequeo que sea la primera palabra de la lista
			if (listSin[0] == pal):
				# la elimino de la lista
				del listSin[0]
				archSin.close()
				return listSin
	archSin.close()
	return listSin
#####################MAIN###############################
corpusList = []
comandList = []
smartList = []

if __name__ == '__main__':
	bot = telepot.Bot('955248895:AAF5qmVshW3NRGj1pgB4Zolk5y6Jm0TMSH4')
	bot.getMe()
	bot.message_loop(handle)
	MessageLoop(bot,handle).run_as_thread()
	chat_id = '750975992'
	bot.sendMessage(chat_id,"Iniciado linuxComHelper Raspberry PI 4")
	#cargarCorpus()
	directorio = "/home/pi/python/AiLinuxBot/AiLinuxBot/linuxCorpus"
	cargarCorporaFromDir(directorio)
	try:
		while(1):
			# para python3, usamos input
			pregunta = input("How can I help you with Linux OS?\n>>> ")
			print("wait a momento, please!")
			if (pregunta.lower() == "bye" or pregunta.lower() == "quit"):
				print("I hope I have helped you.\nbyeee!")
				exit(0)
			#procesarConsulta(pregunta)
			procesarConsultaMasiva(pregunta)
	except KeyboardInterrupt:
		print("Chat interrumpido por teclado")
	print("Chauuuu")
	exit(0)
