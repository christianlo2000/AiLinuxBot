#!/usr/bin/python3
#######################################################
# script......: aiChatWebSearchBot.py
# proposito...: primer chatbot con AI hecho por mi. El 
#		mismo ayuda a los usuarios con comandos
#		Linux para neofitos.
######################################################
#from urllib import urlopen
from six.moves import input
import urllib.request
import nltk
from  nltk.text import ConcordanceIndex
#from nltk.book import *
import re 
from nltk import UnigramTagger as ut
from nltk import BigramTagger as bt
#from cPickle import dump,load
from pickle import dump,load
import sys
import time

########Funciones, clases y metodos para analisis de texto nltk
def loadtagger(taggerfilename):
       infile = open(taggerfilename,'rb')
       tagger = load(infile); infile.close()
       return tagger

def traintag(corpusname, corpus):
       # Function to save tagger.
       def savetagger(tagfilename,tagger):
           outfile = open(tagfilename, 'wb')
           dump(tagger,outfile,-1); outfile.close()
           return
       # Training UnigramTagger.
       uni_tag = ut(corpus)
       savetagger(corpusname+'_unigram.tagger',uni_tag)
       # Training BigramTagger.
       bi_tag = bt(corpus)
       savetagger(corpusname+'_bigram.tagger',bi_tag)
       print("Tagger trained with",corpusname,"using" +\
                   "UnigramTagger and BigramTagger.")
       return

# Function to unchunk corpus.
def unchunk(corpus):
       nomwe_corpus = []
       for i in corpus:
           nomwe = " ".join([j[0].replace("_"," ") for j in i])
           nomwe_corpus.append(nomwe.split())
       return nomwe_corpus

class cesstag():
       def __init__(self,mwe=True):
           self.mwe = mwe
           # Train tagger if it's used for the first time.
           try:
               loadtagger('cess_unigram.tagger').tag(['estoy'])
               loadtagger('cess_bigram.tagger').tag(['estoy'])
           except IOError:
               print("*** First-time use of cess tagger ***")
               print("Training tagger ...")
               from nltk.corpus import cess_esp as cess
               cess_sents = cess.tagged_sents()
               traintag('cess',cess_sents)
               # Trains the tagger with no MWE.
               cess_nomwe = unchunk(cess.tagged_sents())
               tagged_cess_nomwe = batch_pos_tag(cess_nomwe)
               traintag('cess_nomwe',tagged_cess_nomwe)
               print
           # Load tagger.
           if self.mwe == True:
               self.uni = loadtagger('cess_unigram.tagger')
               self.bi = loadtagger('cess_bigram.tagger')
           elif self.mwe == False:
               self.uni = loadtagger('cess_nomwe_unigram.tagger')
               self.bi = loadtagger('cess_nomwe_bigram.tagger')

def pos_tag(tokens, mmwe=True):
       tagger = cesstag(mmwe)
       return tagger.uni.tag(tokens)

def batch_pos_tag(sentences, mmwe=True):
       tagger = cesstag(mmwe)
       return tagger.uni.batch_tag(sentences)


##### Funciones y Metodos ######################
def procesarConsulta(pregunta):
	url = "http://192.168.0.33:80/"
	# obtenemos el texto del web server
	raw_pre = urllib.request.urlopen(url)
	raw = raw_pre.read()
	#print("tipo que es raw: "+str(type(raw)))
	# cargamos los comandos en la lista
	listaCom = []
	#listaCom = setListaComandos(raw)
	#raw1 = raw
	raw1 = limpiarHtml(raw)
	#print "raw1: "+str(raw1)
	# primero tokenizamos para poder procesar el texto
	tokens = nltk.word_tokenize(raw1)
	# inicializamos texto sumandolo a nuestro corpus
	texto1 = nltk.Text(tokens)
	#print("Texto: "+str(texto1))
	# vemos linea a linea el texto1
	#for text1 in texto1:
		#print(text1)
		#print("==========")
	# tokenizamos la pregunta
	palPre = []
	# obtenemos todos los comandos
	listaCom = setListaComandos(raw1)
	palPre = pregunta.split()
	# inicializamos lista de concordancia
	con_list = []
	# loopeamos para ver palabras 
	for pal in palPre:
		concor = texto1.concordance(pal)
		#cargamos en lista comandos
		#listaCom = str(concor.split("==="))
		#print listaCom[1]
		#print str(concor)
		# obtenemos la lista de todas las concordancias
		con_list = con_list + texto1.concordance_list(pal)
		#print con_list
	#print("Salida final de con_list: "+str(con_list))
	# barremos con_list contra listaCom para saber el comando mas mencionado
	cant = 0
	max = 0
	i = 0
	comMax = ""
	for com1 in listaCom:
		# loopeo dentro de la lista de concordancia
		cant = 0
		for con1 in con_list:
			#print("busqueda final: "+str(con1)+" comando a buscar: "+com1)
			#if com1 in con1:
			# convierto lista de concordancia en string
			#lineaCon = ','.join(con1)
			lineaCon = str(con1)
			type(lineaCon)
			if lineaCon.find(com1) > -1:
				cant = cant + 1
				if (cant > max):
					# asignamos maximo
					max = cant
					comMax = com1
	# imprimimos el comando:
	print("Comando buscado: "+comMax+" .Cantidad de ocurrencias: "+str(max))

#Funcion para limpiar caracteres Html
def limpiarHtml(raw):
	cleanr = re.compile('<.*?>')
	#cleanText = re.sub(cleanr,'',raw)
	cleanText = re.sub(cleanr,'',str(raw))
	return cleanText

# armar lista de comandos
def setListaComandos(raw):
	listaComandos = []
	listaEntrada = []
	texto = re.sub(r"\n",";",raw)
	#print("TEXTO: "+str(texto))
	listaEntrada = texto.split(";")
	#print("lista de entrada: "+str(listaEntrada))
	for comando in listaEntrada:
	#for comando in raw:
		#validamos si esta el separador ===
		print("setListaComandos - linea generada: "+comando)
		#time.sleep(5)
		if (comando.find("|") > -1):
			try:
				#print("comando a analizar: "+str(comando))
				intro,com,resto,fin = comando.split("|")
				# agregamos comando a lista
				com1 = com
				listaComandos.append(com1)
			except ValueError:
				print("Excepcion - NO se pudo generar lista. Menos cantidad de campos.")
	print("Lista de comandos generada: \n"+str(listaComandos)+"\n")
	return listaComandos 	
############MAIN##################################
#Iteramos infinitamente
try:
	while(1):
		#pregunta = raw_input("Como te puedo ayudar con Linux OS?\n>>> ")
		# para python3, usamos input
		pregunta = input("Como te puedo ayudar con Linux OS?\n>>> ")
		print("por favor, aguarda un momento")
		if (pregunta == "chau" or pregunta == "Chau"):
			print("Espero haberte ayudado.\nChauuu")
			exit(0)
		procesarConsulta(pregunta)
except KeyboardInterrupt:
	print("Chat interrumpido por teclado")
	print("Chauuuu")
	exit(0)
