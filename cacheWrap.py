def armadoCaches(listCache):
	listC1 = []
	for cache in listCache:
		listC1 = cache.split("|")
		# agregamos a ambas listas
		listKeyWordCache.append(listC1[0])
		listCommandCache.append(listC1[1])
def matchCacheWords(pregunta):
	i = 0
	wordsL = []
	for cacheW in listKeyWordCache:
		wordsL = cacheW.split(",")
		match = False
		for word in wordsL:
			cant = pregunta.count(word)
			#print("word: "+word)
			#print("cant: "+str(cant))
			if(cant == 0):
				# vuelvo al loop para leer otro elemento. aca no esta el patron buscado.
				match = False
				break
			else:
				match = True
		if (match == True):
			# encontre el comando
			print("El comando buscado es: "+listCommandCache[i])
			return 0 # encontro el comando, uija!!!
		i += 1
	return 1 # no encontro patron
cacheF = open("./knowDB/cache.txt","r")
listCache = cacheF.readlines()
cacheF.close()
# tenemos que armar lista de palabras claves y comandos
listKeyWordCache = []
listCommandCache = []
armadoCaches(listCache)
while(True):
	pregunta = input("Input your question: ")
	if (pregunta == "0"):
		break
	matchCacheWords(pregunta)

