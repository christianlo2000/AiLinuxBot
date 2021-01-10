#!/usr/bin/python3
#######################################################
# script......: linuxComHelper.py
# proposito...: chatbot con AI hecho por mi. el idioma es 
#		el ingles dado que no consegui procesar
#		texto en español (NLP) 
# Status......: en construccion		mismo ayuda a los usuarios con comandos
######################################################
#from urllib import urlopen
from six.moves import input
import urllib.request
import nltk
from  nltk.text import ConcordanceIndex
#from nltk.book import *
import re 
import os
from nltk import UnigramTagger as ut
from nltk import BigramTagger as bt
#from cPickle import dump,load
from pickle import dump,load
import sys
import time
import telepot
from telepot.loop import MessageLoop

# Funcion Handle de chatbot de telegram
def handle(msg):
	chat_id = msg['chat']['id']
	pregunta = msg['text']
	print('pregunta: %s' % pregunta)
	print('Chat Id: %s' % chat_id)
	# analizamos si el mensaje es saludo
	if (pregunta.lower() == "bye" or pregunta.lower() == "see you"):
		bot.sendMessage(chat_id,"See you, bye bye")
	# procesamos consulta
	procesarConsultaMasiva(pregunta)
#### Funciones y Metodos ######################
# variables globales
textCp = ""
textMv = ""
rm = ""
mkdir = "" 
# funcion para cargar los corpus a consultar de linux
def cargarCorpus():
	# lso corpus quedan como variables globales
	global textCp, textMv, textLs, textMkdir, textRm, textDf
	# cargamos los corpus uno por cada comando
	cp = ""
	cpFile = open("./linuxCorpus/cp.txt","r")
	for registro in cpFile:
		cp = cp + registro
	cpFile.close()
	# ahora lo agrego a un corpus para poder manipular el texto
	# tokenizo el texto
	tokensCp = nltk.word_tokenize(cp)
	textCp = nltk.Text(tokensCp)
	mv = ""
	mvFile = open("./linuxCorpus/mv.txt","r")
	for registro in mvFile:
		mv = mv + registro
	mvFile.close()
	tokensMv = nltk.word_tokenize(mv)
	textMv = nltk.Text(tokensMv)
	# corpus ls
	ls = ""
	lsFile = open("./linuxCorpus/ls.txt","r")
	for registro in lsFile:
		ls = ls + registro
	lsFile.close()
	tokensLs = nltk.word_tokenize(ls)
	textLs = nltk.Text(tokensLs)
	# corpus mkdir
	mkdir = ""
	mkdirFile = open("./linuxCorpus/mkdir.txt","r")
	for registro in mkdirFile:
		mkdir = mkdir + registro
	mkdirFile.close()
	tokensMkdir = nltk.word_tokenize(mkdir)
	textMkdir = nltk.Text(tokensMkdir)
	# corpus rm
	rm = ""
	rmFile = open("./linuxCorpus/rm.txt","r")
	for registro in rmFile:
		rm = rm + registro
	rmFile.close()
	tokensRm = nltk.word_tokenize(rm)
	textRm = nltk.Text(tokensRm)
	# corpus df


# funcion para cargar corpus uno por archivo de un directorio
def cargarCorporaFromDir(directorio):
	# lista de todos los nombres de corpus
	global corpusList
	global comandList
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
		for registro in archCorp1:
			# reemplazamos los () por espacios
			registro1 = registro.replace("("," ")
			registro2 = registro1.replace(")"," ")
			fileInfo = fileInfo + registro2
		# cerramos archivo
		archCorp1.close()
		# tokenizamos
		tokens = nltk.word_tokenize(fileInfo)
		textCorp = nltk.Text(tokens)
		corpusList.append(textCorp)
		comandList.append(archivo[0:len(archivo)-4])	
# funcion principal para procesar consulta del usuario
def procesarConsulta(pregunta):
	# definimos listas a utilizar para comparar comandos
	listCom = []
	listStat = []
	# hacemos analisis sintactico y solo dejamos verbo y objeto
	listaVerbObj,listaFunc = getObjAndVerb(pregunta)
	print("lista verbo y objeto: "+str(listaVerbObj))
	# buscamos la cantidad de veces q se repite la palabra de la pregunta
	totCp = analisisStatCorpus(textCp,listaVerbObj,listaFunc)
	listCom.append("cp")
	listStat.append(totCp)
	print("total Stat Corpus cp: "+str(totCp))
	# ahora voy por el corpus de mv
	totMv = analisisStatCorpus(textMv,listaVerbObj,listaFunc)
	print("total Stat Corpus mv: "+str(totMv))
	listCom.append("mv")
	listStat.append(totMv)
	# corpus ls
	totLs = analisisStatCorpus(textLs,listaVerbObj,listaFunc)
	print("Total Stat Corpus ls: "+str(totLs))
	listCom.append("ls")
	listStat.append(totLs)
	# corpus mkdir
	totMkdir = analisisStatCorpus(textMkdir,listaVerbObj,listaFunc)
	print("total Stat Corpus mkdir: "+str(totMkdir))
	listCom.append("mkdir")
	listStat.append(totMkdir)
	# corpus rm
	totRm = analisisStatCorpus(textRm,listaVerbObj,listaFunc)
	print("total Stat Corpus rm: "+str(totRm))
	listCom.append("rm")
	listStat.append(totRm)

	i = 0
	max = 0
	maxCom = "no hay"
	for comando in listCom:
		if (listStat[i] > max):
			max = listStat[i]
			maxCom = comando
		i += 1	
	print("Linux Command that you search is: "+maxCom)
	if (max == 0):
		# no se encontro comando
		infoLin = "I'm sorry, I can't find a comand for your question"
	else:	
		infoLin = "Command that you need is: "+maxCom 
	bot.sendMessage(chat_id,infoLin,parse_mode='Markdown')
# procesar consulta masiva
def procesarConsultaMasiva(pregunta):
	# hacemos analisis sintactico y solo dejamos verbo y objeto
	listaVerbObj,listaFunc = getObjAndVerb(pregunta)
	# barremos los corpus para detectar
	listTot = []
	for corpus in corpusList:
		totStat = analisisStatCorpus(corpus,listaVerbObj,listaFunc)
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
		infoLin = "Command that you need is: "+maxCom
	bot.sendMessage(chat_id,infoLin,parse_mode='Markdown')

def getObjAndVerb(oracion):
	listaSalPal = []
	listaSalFunc = []
	# hacemos analisis sintactico de la oracion
	salida = nltk.pos_tag(oracion.split())
	print("Ora Anal: "+str(salida))
	# barro para quedarme solo con NN y VB y VBP para analisis
	for pal,func in salida:
		if (func == "VBP" or func == "VB" or func == "NN"):
			# lo agregamos  a la lista de salida
				listaSalPal.append(pal)
				listaSalFunc.append(func)
	return listaSalPal,listaSalFunc
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
#####################MAIN###############################
corpusList = []
comandList = []

if __name__ == '__main__':
	bot = telepot.Bot('955248895:AAF5qmVshW3NRGj1pgB4Zolk5y6Jm0TMSH4')
	bot.getMe()
	bot.message_loop(handle)
	MessageLoop(bot,handle).run_as_thread()
	chat_id = '750975992'
	bot.sendMessage(chat_id,"Iniciado linuxComHelper Odroid N2")
	#cargarCorpus()
	directorio = "./linuxCorpus"
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
