# libreria para procesamiento de texto generico
# librerias a importar
from nltk.stem.porter import *
import re
import collections
from textblob import Word
from langdetect import detect

# Funciones y metodos de esta libreria
# validacion de idioma y devolvemos el idioma del texto
# ej: ingles = 'en'
def getIdioma(texto):
	""" valida el idioma del texto pasado por parametro. """
	idioma = detect(texto)
	return(idioma)
# Elimina texto basura
def clean_text1(texto):
	""" elimina algunos caracteres especiales del texto pasado como argumento """
	#listTextTrash = ["(","]","}",")","[","{","/","\"]
	listTextTrash = ["(","]","}",")","[","{","/","-","\\"]
	#listTextTrash = ["(","]","}",")","[","{"]
	textOut = texto
	for basura in listTextTrash:
		textOut = textOut.replace(basura," ")
	return textOut
# elimina texto basura usando regex - mas sofisticado
def clean_text2(texto,remove_digits=False):
	""" Elimina todos los caracteres especiales, y se le puede indicar eliminar numeros por si o por no """
	pattern = r"[^a-zA-Z0-9\s]" if not remove_digits else r"[^a-zA-Z\s]"
	text = re.sub(pattern," ",texto)
	return text
# determinamos si es un pronombre en ingles
def isPronoun(word):
	""" Determina si la palabra parametro es o no Pronombre """
	pronList = ["i","you","he","she","we","they"]
	for pron in pronList:
		if (word.lower() == pron):
			return True
	return False
def isModalVerb(word):
	""" We can know if the verb is modal verb or not. Return True or False """
	modVerb = ["can","may","want","should","shall","need","would","might"] 
	for verb in modVerb:
		if (verb == word.lower()):
			return True
	return False
def isMyStopWord(pal):
	""" We detect if parameter is a my stopword """
	myList = ["like"]
	if (isModalVerb(pal) or isPronoun(pal)):
		return True
	for stop in myList: 
		if (pal.lower() == stop):
			return True
	return False
def correctSent(sent):
	""" Correct sintax of a sentence. For now, We use only example want to and need to and send to. Parameter is original sentence and return new sentence corrected. Besides, detect if a word is bad spelling  """
	listBigr1 = ["send","want","need","like"]
	listSent = sent.lower().split(" ")
	sentOut = []
	miLexico = getMiLexico()
	i = 0
	for pal in listSent:
		# validamos si son contracciones
                # busco en diccionario de contracciones
		pal1 = re.sub("[^0-9a-zA-Z]+","\'",pal)
		#if (pal1.find("'") > -1 or pal.find("´") > -1 or pal.find("`") > -1):
		if (pal1.find("'") > -1):
		# tiene una contraccion, busco reemplazo
			contract = CONTRACTION_MAP[pal1]
			sentOut.append(contract)
			continue
		# validamos si la palabra pertenece a lexico especial
		if (pal in miLexico):
			# agrego la palabra y la tomo como buena
			sentOut.append(pal)
			continue
		# validamos que este bien deletreada la palabra
		word = Word(pal)
		newWord = word.correct()
		if (word != newWord):
			pal = newWord
		if (pal in listBigr1 and listSent[i+1] != "to"):
			sentOut.append(pal)
			sentOut.append("to")
		else:
			sentOut.append(pal)
		i += 1
	oracion = ' '.join(sentOut)
	return oracion
		

# funcion para obtener mi lexico
def getMiLexico():
	""" diccionario especial con palabras de lexico particular """
	lexFile = open("/home/pi/python/AiLinuxBot/AiLinuxBot/miLexico/miLexico.txt","r")
	lista = [] 
	for pal in lexFile:
		pal1 = pal.replace('\n','')
		lista.append(pal1)
	lexFile.close()
	return lista	
# obtenemos singular, a partir de stemmer
def getSingular(pal):
	""" Devuelve el string singular de la palabra argumento """
	# preguntamos si el plural tiene sufijos determinados
	if (pal.endswith("ies")):
		singular = pal[0:len(pal)-3]+"y"
		print("Singular: "+singular)
		return singular
	stemmer = PorterStemmer()
	singular = stemmer.stem(pal)
	print("Singular: "+singular)
	return singular
# obtenemos plural agregando solo la s - mmuy rustico
def getPlural(pal):
	""" Devuelve el string plural de la palabra argumento """
	if (pal.endswith("y")):
		plural = pal[0:len(pal)-1]+"ies"
		print("Plural: "+plural)
		return plural
	print("Plural: "+pal+"s")
	return pal+"s"
def textStemmer(texto):
	""" Stemming all text's word. Doesn't work good. Need help to improve """
	ps = PorterStemmer()
	text = ' '.join([ps.stem(word) for word in texto.split()])
	return text
#########FUNCIONES DE CORRECTION DE TEXTO ############################
def tokens(text):
	"""Devuelve todas las palabras del texto parametro """
	return re.findall("[a-z]+",text.lower())
def edits0(word):
	""" retorna la palabra pasada como argumento """
	return {word}
def edits1(word):
	""" retorna todas las letras del texto que aparece solo 1 vez """
	alfabeto = "abcdefghijklmnopqrstuvwxyz"
	def splits(word):
		""" retorna una lista de posibles palabras con la palabra ingresada """
		return[(word[:i],word[i:]) for i in range(len(word)+1)]
	pairs = splits(word)
	deletes = [a+b[1:] for (a,b) in pairs if b]
	transposes = [a+b[1]+b[0]+b[:2] for (a,b) in pairs if len(b) > 1]
	replaces = [a+c+b[1:] for (a,b) in pairs for c in alfabeto if b]
	inserts = [a+c+b for (a,b) in pairs for c in alfabeto]
	return set(deletes+transposes+replaces+inserts)
def remove_repeated_char(tokens):
	""" Remueve caracteres repetidos de la palabra argumento """
	repeat_pattern = re.compile(r"(\w*)(\w)\2(\w*)")
	match_subs = r"\1\2\3"
	def replace(old_word):
		if (wordnet.synsets(old_word)):
			return old_word
		new_word = repeat_pattern.sub(match_subs,old_word)
		return replace(new_word) if new_word != old_word else new_word
	correct_tokens = [replace(word) for word in tokens]
	return correct_tokens	
			
def isWordExist(word):
	""" Return True if the word exist, otherwise return False """
	if (wordnet.synsets(word)):
		return True
	return False 

#########FIN DE FUNCIONES CORRECCION DE TEXTO ########################
###########################################################
# Contracciones en ingles
CONTRACTION_MAP = {
	"ain't" : "is not",
	"aren't" : "are not",
	"can't" : "can not",
	"can't've" : "can not have",
	"i'm" : "i am",
	"you're" : "you are",
	"didn't" : "did not",
	"don't" : "do not",
	"doesn't" : "does not",
	"we're" : "we are",
	"they're" : "they are",
	"i'd" : "i would",
	"you'd" : "you would",
	"he'd" : "he would",
	"she'd" : "she would",
	"we'd" : "we would",
	"they'd" : "they would"
}
