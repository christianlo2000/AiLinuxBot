# -*- coding: utf-8 -*-
# encoding: utf-8
################# -*- coding: latin-1 -*-
import urllib2
#import urllib
#from urllib.request import urlopen
import re

# definimos la clase texto para obtener info del mismo
class Texto:
	__texto = ""
	__cantPal = -1

	def __init__(self,texto):
		self.__texto = texto
		self.__cantPal = len(self.__analisisSin)
	def getTexto(self):
		return self.__texto
	def getCantPal(self):
		return self.__cantPal
    	# concordancia y contexto
	def concordancia(self,palabra):
		listOra = []
		listOra = self.__texto.split(".")
		# buscamos en lista
		for ora in listOra:
			if (ora.find(palabra) >-1):
				print(str(ora))
                
# funciones de analisis de palabras del texto
	def esPlural(self,palabra):
		#preguntamos por palabras sin numero
		# palabras sin numero q no terminen en sis
		if (palabra.lower() == "caries"):
			return False
		if (palabra.lower().endswith("sis")):
			return False
		if (palabra.lower() in ["compás","cortés","as"]):
			return False
		if (palabra.lower().endswith("s")):
			return True
		return False
   
	# funcion para convertir a singular
	def singular(self,palabra):
		# preguntamos si es plural
		if (self.esPlural(palabra) == True):
			# aca va el core de la funcion
			tam = len(palabra)
			if (palabra.endswith("ies")):
				palSing = palabra[:tam-2]
				return palSing
			# palabras en singular finalizan en z
			if (palabra.endswith("ces")):
				palSing = palabra[:tam-3]+"z"
				return palSing
			if (palabra.endswith("les") or palabra.endswith("jes") or palabra.endswith("mes") or palabra.endswith("des")):
				palSing = palabra[:tam-2]
				return palSing
			# el resto es suprimir la s final
			palSing = palabra[:tam-1]
			return palSing
		# es singular
		return palabra
    # funcion q determina si la palabra es o no articulo
	def esArticulo(self,palabra):
		# valido si es pronombre demostrativo
		if (self.esPronDemo(palabra.lower())):
			return True
		listArt = ["la","el","las","los","un","unos","una","unos"]
		# buscamos en la lista de articulo
		for art in listArt:
			if (art == palabra.lower()):
				return True
		return False

    # funcion para determinar si es una preposicion
	def esPreposicion(self,palabra):
		prepList = ["a","ante","bajo","cabe","con","contra","de","desde","en","entre","hacia","para","por","hasta","sin","segun","so","sobre","tras","mediante","versus","vía","incluso"]
		for prep in prepList:
			if (prep == palabra.lower()):
				return True
		return False
    # funcion q determina si es pronombre demostrativo
	def esPronDemo(self,palabra):
		pronList = ["este","esta","estos","estas","estos","ese","esa","eso","esas","esos","aquel","aquella","aquello","aquellas","aquellos"]
		for pron in pronList:
			if (pron == palabra.lower()):
				return True
		return False
    # funcion para determinar adverbio de lugar
	def esAdvLugar(self,palabra):
		advList = ["aquí","acá","allá","ahí","arriba","abajo","cerca","lejos","delante","adelante","detrás","atrás","encima","enfrente","alrededor"]
		for pron in advList:
			if (pron == palabra.lower()):
				return True
		return False
    # validar si es adverbio de tiempo
	def esAdvTiempo(self,palabra):
		advList = ["antes","después","luego","pronto","tarde","temprano","todavía","aún","ya","ayer","hoy","mañana","anteayer","siempre","nunca","jamás","próximamente","prontamente","anoche","enseguida","ahora","mientras","anteriormente"]
		for pron in advList:
			if (pron == palabra.lower()):
				return True
		return False
    # validamos si es adverbio de compania
	def esAdvComp(self,palabra):
		advList = ["con","conmigo","contigo"]
		for adv in advList:
			if (adv == palabra.lower()):
				return True
		return False
    # validar si es adverbio de modo 
	def esAdvModo(self,palabra):
		advList = ["bien","mal","regular","excelente","sobresaliente","despacio","deprisa","así","rápido","lento","como","tal","aprisa","adrede","peor","mejor","orden","desorden"]
		#print "Estoy dentro de esAdvModo"
		for pron in advList:
			if (pron == palabra.lower().strip()):
				print("ENCONTRE LA PALABRA: "+palabra)
				return True
            # validamos si es otra clase de adverbio, dado que hay palabras finalizadas en -mente que corresponde a otros tipos
		if (self.esAdvTiempo(pron) or self.esAdvCant(pron) or self.esAdvAfirm(pron) or self.esAdvDuda(pron) or self.esAdvOrden(pron)):
			return False
		# validamos si termina en mente
		if (palabra.lower().endswith("mente")):
		# grabamos archivo, dado que este tipo de adverbio tiene muchos vocablos
			return True
		return False
    # validar si es adverbio de cantidad
	def esAdvCant(self,palabra):
		advList = ["muy","poco","mucho","bastante","más","menos","algo","demasiado","casi","sólo","solamente","tan","tanto","todo","nada","aproximádamente"]
		for pron in advList:
			if (pron == palabra.lower()):
				return True
		return False
    # validar si es adverbio de afirmacion
	def esAdvAfirm(self,palabra):
		advList = ["sí","también","cierto","ciertamente","efectivamente","claro","exacto","obvio","obviamente","verdaderamente","seguramente","asimismo"]
		for pron in advList:
			if (pron == palabra.lower()):
				return True
		return False
 #validar si es adverbio de negacion
	def esAdvNega(self,palabra):
		advList = ["no","jamás","nunca","tampoco"]
		for pron in advList:
			if (pron == palabra.lower()):
				return True
		return False
    # validar si es adverbio de duda
	def esAdvDuda(self,palabra):
		advList = ["quizá","quizás","probablemente","posiblemente","seguramente"]
		for pron in advList:
			if (pron == palabra.lower()):
				return True
		return False
    # validar si es adverbio de orden
	def esAdvOrden(self,palabra):
		advList = ["primeramente","últimamente","secundariamente"]
		for pron in advList:
			if (pron == palabra.lower()):
				return True
		return False
    # validar si es adjetivo posesivo
    def esAdjPosesivo(self,palabra):
        advList = ["su","sus","mi","tu","tus","nuestro","nuestra","vuestro","vuestra","mío","mía","tuyo","tuya"]
        for pron in advList:
            if (pron == palabra.lower()):
                return True
        return False
    # validar si es contraccion
    def esContraccion(self,palabra):
    	listPal = ["al","del"]
	for pal in listPal:
		if (pal == palabra.lower()):
			return True
	return False
    # validar si es conj copulativa
    def esConjCopu(self,palabra):
        advList = ["y","e","ni"]
        for pron in advList:
            if (pron == palabra.lower()):
                return True
        return False
    # validar si es conj disyuntiva
    def esConjDisyun(self,palabra):
        	advList = ["o","u"]
        	for pron in advList:
        	    if (pron == palabra.lower()):
        	        return True
        	return False
    # validar si oracion tiene sujeto tacito
    def haySujetoTacito(self,oracion):
        oraList = oracion.encode('utf-8').split(r'\x')
        #print (oraList[0])
        if (self.esVerbo(str(oraList[0])) and str(oraList[0]).endswith("r")):
            # no es sujeto tacito
            return False
        elif (self.esVerbo(str(oraList[0]))):
            return True
        return False

    # validamos si es conjuncion concesiva, faltan la spalabras compuestas
    def esConjConce(self,palabra):
        palList = ["aunque","pero"]
        for pal in palList:
            if(palabra.lower() == pal):
                return True
        return False
	# funcion q analiza q rol posee cada palabra en la oracion
    # validamos si es pronombre personal
    def esPronPer(self,palabra):
    		pronPer = ["me","yo","se","le","les","te","lo"]
    		for pron in pronPer:
        		if(pron == palabra.lower()):
            			return True
    		return False
    # Analisis sintactico de oracion
    def sintaxAnal(self,oracion1):
   	# validamos q la oracion finalice con punto
    	# defino diccionario q usare de parametro de retorno
    	listPar = []
    	oracion = ""
	#print("Oracion1: "+oracion1)
    	if(oracion1.endswith(".") != True):
       		print("Error - oracion debe finalizar con (.)")
       		return listPar
    	else:
       		oracion = oracion1[:len(oracion1)-1]
    	# defino lista donde cargaremos palabras de oracion
    	listOra = []
    	# cargamos oracion en lista
    	listOra = oracion.split()
    	# analizamos palabra por palabra sin descuidar contexto
    	# inicializamos tipo_ant
    	tipo_ant = ""
	# inicializamos variable string de salida
	oraSal = ""
    	verbo = False # para delimitar objetos de sujeto
    	sujeto = False # flag para diferenciar objetos de modifcador directo
    	# verificamos si es sujeto Tacito
    	#if (self.haySujetoTacito(oracion)):
       		#print("--->Oracion con Sujeto Tacito")
    	for palabra1 in listOra:
       		if(palabra1.endswith(",") or palabra1.endswith(":") or palabra1.endswith(";")):
          		palabra = palabra1[:len(palabra1)-1]
        	else:
            		palabra = palabra1
		# validamos si palabra anterior adverbio de cantidad
		if (tipo_ant == "C.Cantidad"):
			tipo = "OD"
			tipo_ant = tipo
			listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
			continue
		# valido si es complemento de compañia
		if (self.esAdvComp(palabra.lower())):
			tipo = "C.Compania"
			tipo_ant = tipo
			listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+"-->"+tipo)
			continue
		if (self.esAdvModo(palabra)):
                        tipo = "C.Modo"
                        tipo_ant = tipo
                        listPar.append(tipo)
                        oraSal += palabra+" --> "+tipo+"\n"
                        continue
        	#analizamos palabra por palabra
        	if (self.esArticulo(palabra.lower())):
            		tipo = "DET"
            		tipo_ant = tipo
            		listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
			continue
        	if (tipo_ant == ""):
			if (sujeto == True):
				tipo = "OD"
				tipo_ant = tipo
				listPar.append(tipo)
			else:
            			tipo = "SN"
            			sujeto = True
            			tipo_ant = tipo
            			listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
                        continue
        	if (self.esPronPer(palabra)):
		    # validamos si ya hay sujeto
		    if (sujeto == True):
			tipo = "OI"
                    	tipo_ant = tipo
                    	listPar.append(tipo)
		    else:
        	    	tipo = "SN"
        	    	sujeto = True
        	    	tipo_ant = tipo
        	    	listPar.append(tipo)
		    oraSal += palabra+" --> "+tipo+"\n"
		    print(palabra+" --> "+tipo)
                    continue
		
		if (self.esContraccion(palabra)):
		    tipo = "Contraccion"
		    tipo_ant = tipo
		    listPar.append(tipo)
		    oraSal += palabra+" --> "+tipo+"\n"
		    print(palabra+" --> "+tipo)
                    continue
	
        	if (tipo_ant == "NV" and self.esPronDemo(palabra)):
        	    tipo = "Pronombre Demostrativo"
        	    tipo_ant = tipo
        	    listPar.append(tipo)
		    oraSal += palabra+" --> "+tipo+"\n"
		    print(palabra+" --> "+tipo)
                    continue
	
        	if (self.esVerbo(palabra) and tipo_ant != "DET"):
            		# preguntamos por si es adverbio
            		if (palabra.lower() == "encima" and verbo):
               			tipo = "C.Lugar"
               			listPar.append(tipo)
               			tipo_ant = tipo
            		elif (palabra.lower() == "de"):
               			tipo = "E"
               			tipo_ant = tipo
               			listPar.append(tipo)
            		# consultamos si comienza con mayuscula sin ser la primera palabra
            		elif (palabra[0] >= 'A' and palabra[0] <= 'Z' and tipo_ant != ""):
               			tipo = "SN"
               			sujeto = True
               			tipo_ant = tipo
               			listPar.append(tipo)
            		else:
               			tipo = "NV"
               			tipo_ant = tipo
               			verbo = True
               			listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
                        continue
        	if (self.esVerbo(palabra) and tipo_ant == "DET"):
			if (sujeto == True):
				# es objeto directo
				tipo = "OD"
                        	tipo_ant = tipo
                        	listPar.append(tipo)
			else:
            			tipo = "SN"
            			sujeto = True
            			tipo_ant = tipo
            			listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
                        continue
        	if (self.esAdjPosesivo(self.singular(palabra))):
            		tipo = "Adjetivo Posesivo"
            		tipo_ant = tipo
            		listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
                        continue
        	if (self.esConjCopu(palabra)):
            		tipo = "Conjuncion Copulativa"
            		tipo_ant = tipo
			# paso sujeto y el NV a false porque es otro nucleo
			sujeto = False
			verbo = False
            		listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
                        continue
        	if (self.esConjDisyun(palabra)):
        	    	tipo = "Conjuncion Disyuntiva"
        	    	tipo_ant = tipo
        	    	listPar.append(tipo) 
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
			# paso sujeto y el NV a false porque es otro nucleo
                        sujeto = False
                        verbo = False
                        continue
        	if (self.esConjConce(palabra)):
            		tipo = "Conjuncion Concesiva"
            		tipo_ant = tipo
            		listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
                        continue
        	if (self.esPronPer(palabra)):
			if (sujeto == True):
				tipo = "OD"
				tipo_ant = tipo
				listPar.append(tipo)
			else:
            			tipo = "SN"
            			sujeto = True
            			tipo_ant = tipo
            			listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
                        continue
        	if (self.esPreposicion(palabra)):
            		tipo = "E"
            		tipo_ant = tipo
            		listPar.append(tipo)
			print(palabra+" --> "+tipo)
			oraSal += palabra+" --> "+tipo+"\n"
                        continue
        	if (self.esPronDemo(palabra)):
            		tipo = "Pronombre demostrativo"
            		tipo_ant = tipo
            		listPar.append(tipo)
			print(palabra+" --> "+tipo)
			oraSal += palabra+" --> "+tipo+"\n"
                        continue
        	if (self.esAdvLugar(palabra)):
            		tipo = "C.Lugar"
            		tipo_ant = tipo
            		listPar.append(tipo)
			print(palabra+" --> "+tipo)
			oraSal += palabra+" --> "+tipo+"\n"
                        continue
        	if (self.esAdvCant(palabra)):
            	# validamos si no es nucleo
            		if (tipo_ant == "DET" ):
				# validamos que sea objeto en lugar de sujeto
				if (sujeto == True):
					# entonces es objeto
					tipo = "OD"
                                     	tipo_ant = tipo
                                     	listPar.append(tipo)
				else:
               				tipo = "SN"
               				sujeto = True
               				tipo_ant = tipo
               				listPar.append(tipo)
            		else:
               			tipo = "C.Cantidad"
               			tipo_ant = tipo
               			listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
                        continue
        	if (self.esAdvTiempo(palabra)):
            		if (tipo_ant == "DET"):
				# validamos si ya hay sujeto
				if (sujeto == True):
					tipo = "OD"
					tipo_ant = tipo
					listPar.append(tipo)
				else:
               				tipo = "SN"
               				sujeto = True
               				tipo_ant = tipo
               				listPar.append(tipo)
            		else:
               			tipo = "C.Tiempo"
               			tipo_ant = tipo
               			listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
                        continue
        	if (self.esAdvDuda(palabra)):
            		tipo = "C.Duda"
            		tipo_ant = tipo
            		listPar.append(tipo)
			print(palabra+" --> "+tipo)
			oraSal += palabra+" --> "+tipo+"\n"
                        continue
        	if (self.esAdvAfirm(palabra)):
            		tipo = "C.Afirmacion"
            		tipo_ant = tipo
            		listPar.append(tipo)
			print(palabra+" --> "+tipo)
			oraSal += palabra+" --> "+tipo+"\n"
                        continue
        	if (self.esAdvNega(palabra)):
            		tipo = "C.Negacion"
            		tipo_ant = tipo
            		listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
                        continue
        	#if (self.esAdvModo(palabra)):
            	# este tipo de adverbio requiere analisis mas complejo
            		#if (tipo_ant in ["E","NV"]):
               			#tipo = "C.Modo"
               			#tipo_ant = tipo
               			#listPar.append(tipo)
            		#else:
               			#tipo = "OI"
               			#tipo_ant = tipo
               			#listPar.append(tipo)
			#oraSal += palabra+" --> "+tipo+"\n"
			#print(palabra+" --> "+tipo)
                        #continue
            	# intentamos diferenciar objeto de sujeto
            	if (verbo and sujeto and tipo_ant != "E"):
               		tipo = "OD"
               		tipo_ant = tipo
               		listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
                        continue
		elif (verbo and sujeto and tipo_ant == "E"):
                        tipo = "OI"
                        tipo_ant = tipo
                        listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
                        print(palabra+" --> "+tipo)
                        continue
            	elif (sujeto and not verbo):
               		tipo = "Modif Directo"
               		tipo_ant = tipo
               		listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
                        continue
            	#elif (verbo and not sujeto):
               		#tipo = "Objeto"
               		#tipo_ant = tipo
               		#listPar.append(tipo)
			#print(palabra+" --> "+tipo)
                        #continue
            	else:
			if (sujeto == True):
				tipo = "OD"
				tipo_ant = tipo
				listPar.append(tipo)
			else:
				if (verbo == True):
					tipo = "OD"
				else:
               				tipo = "SN"
               				sujeto = True
               			tipo_ant = tipo
               			listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
                        continue
	### TERMINA EL FOR ACA #######
    	# retorno diccionario con analisis sintactico
	print("########################################")
	print(str(listOra).encode('utf-8'))
	print(str(listPar))
	print("########################################")
	analSinOut = zip(listOra,listPar)
	self.grabarArchivoLog(str(analSinOut),"analisisOraciones.txt")
	self.grabarArchivoLog(str(oracion1),"TextosAnalizados.txt")
    	#return zip(listOra,listPar)
	return analSinOut,oraSal
    	#return palDicc
    # analisis Morfologico de la oracion
    def morfoAnal(self,oracion1):
        # validamos q la oracion finalice con punto
        # defino diccionario q usare de parametro de retorno
        listPar = []
        oracion = ""
        #print("Oracion1: "+oracion1)
        if(oracion1.endswith(".") != True):
                print("Error - oracion debe finalizar con (.)")
		#print("Oracion: "+oracion1)
		oracion = oracion1
                #return listPar
        else:
                oracion = oracion1[:len(oracion1)-1]
        # defino lista donde cargaremos palabras de oracion
        listOra = []
	listMorfo = []
        # cargamos oracion en lista
        listOra = oracion.split()
	# iteramos la lista para averiguar tipo de palabra
	for pal1 in listOra:
		if(pal1.endswith(",") or pal1.endswith(":") or pal1.endswith(";")):
                        pal = pal1[:len(pal1)-1]
                else:
                        pal = pal1
		if (self.esVerboInfinitivo(pal)):
			listMorfo.append("Verb. Infi")
			continue
		if (self.esAdjetivo(self.singular(pal))):
			listMorfo.append("Adjetivo")
			continue
		if (self.esAdjPosesivo(pal)):
			listMorfo.append("Adj. Pose")
			continue
		if (self.esAdvAfirm(pal)):
			listMorfo.append("Adv. Afir")
			continue
		if (self.esAdvCant(pal)):
			listMorfo.append("Adv. Cant")
			continue
		if (self.esAdvComp(pal)):
			listMorfo.append("Adv. Comp")
			continue
		if (self.esAdvDuda(pal)):
			listMorfo.append("Adv. Duda")
			continue
		if (self.esAdvLugar(pal)):
			listMorfo.append("Adv. Luga")
			continue
		if (self.esAdvModo(pal)):
			listMorfo.append("Adv. Modo")
			continue
		if (self.esAdvNega(pal)):
			listMorfo.append("Adv. Nega")
			continue
		if (self.esAdvOrden(pal)):
			listMorfo.append("Adv. Orde")
			continue
		if (self.esAdvTiempo(pal)):
			listMorfo.append("Adv. Tiem")
			continue
		if (self.esArticulo(pal)):
			listMorfo.append("Articulo")
			continue
		if (self.esConjConce(pal)):
			listMorfo.append("Conj. Conc")
			continue
		if (self.esConjCopu(pal)):
			listMorfo.append("Conj. Copu")
			continue
		if (self.esConjDisyun(pal)):
			listMorfo.append("Conj. Disy")
			continue
		if (self.esContraccion(pal)):
			listMorfo.append("Contraccion")
			continue
		if (self.esPreposicion(pal)):
			listMorfo.append("Preposicion")
			continue
		if (self.esPronDemo(pal)):
			listMorfo.append("Pron. Demo")
			continue
		if (self.esPronPer(pal)):
			listMorfo.append("Pron. Pers")
			continue
		if (self.esSustantivo(pal)):
			listMorfo.append("Sustantivo")
			continue
		if (self.esVerbo(pal)):
			listMorfo.append("Verbo")
			continue
		# no se pudo determinar morfologicamente signfiicado
		# es factible que sea adjetivo o sustantivo
		listMorfo.append("NN")
	# devolvemos lista con valores morfologicos
	print("morfoAnal: "+str(listMorfo))
	return listMorfo	
    # analisis MorfoSintactico
    def morfoSintaxAnal(self,oracion1):
   	# validamos q la oracion finalice con punto
    	# defino diccionario q usare de parametro de retorno
    	listPar = []
    	oracion = ""
	#print("Oracion1: "+oracion1)
    	if(oracion1.endswith(".") != True):
       		print("Error - oracion debe finalizar con (.)")
       		#return listPar
		oracion = oracion1
    	else:
       		oracion = oracion1[:len(oracion1)-1]
    	# defino lista donde cargaremos palabras de oracion
    	listOra = []
    	# cargamos oracion en lista
    	listOra = oracion.split()
    	# analizamos palabra por palabra sin descuidar contexto
	# inicializamos variable string de salida
	oraSal = ""
    	verbo = False # para delimitar objetos de sujeto
    	sujeto = False # flag para diferenciar objetos de modifcador directo
    	# verificamos si es sujeto Tacito
    	#if (self.haySujetoTacito(oracion)):
       		#print("--->Oracion con Sujeto Tacito")
		#sujeto = True
	# realizamos analisis morfologico
	listMorfo = self.morfoAnal(oracion)
	print("listMorfo: "+str(listMorfo))
	ind = 0
    	for palabra1 in listOra:
       		if(palabra1.endswith(",") or palabra1.endswith(":") or palabra1.endswith(";")):
          		palabra = palabra1[:len(palabra1)-1]
        	else:
            		palabra = palabra1
		 # analizamos si el adverbio de tiempo es SN o C. de tiempo
		if (listMorfo[ind] == "Adv. Tiem"):
                	if ((ind + 2) <= len(listMorfo) and (listOra[ind+1] in ["es","fue","será","está","estará"]) and listMorfo[ind+2] in ["Sustantivo","Adjetivo","NN","Adv. Modo","Articulo"]):
                        	tipo = "SN"
			else:
				tipo = "C.Tiempo"
			listPar.append(tipo)
                        oraSal += palabra+" --> "+tipo+"\n"
                        print(palabra+" --> "+tipo)
                        ind += 1
                        continue
		if (listMorfo[ind] == "Preposicion"):
                        tipo = "E"
                        listPar.append(tipo)
                        print(palabra+" --> "+tipo)
                        oraSal += palabra+" --> "+tipo+"\n"
                        ind += 1
                        continue
		# validamos si el primero ya es nucleo verbal
		if (ind == 0 and listMorfo[ind] == "Verbo"):
			tipo = "NV"
			listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			ind += 1
			verbo = True
			continue
		# validamos si no es objeto indirecto OI
		if (ind > 0 and listMorfo[ind-1] == "Contraccion" and listMorfo[ind] not in ["Verbo"]):
			tipo = "OI"
                        listPar.append(tipo)
                        oraSal += palabra+" --> "+tipo+"\n"
                        ind += 1
                        continue
		# validamos NV compuesto con E en medio: ej: fue a estudiar
		if (ind - 2>0 and listMorfo[ind] == "Verb. Infi" and listMorfo[ind-1] == "Preposicion"):
			# el infinitivo es parte del nucleo verbal
			tipo = "NV"
			listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			ind += 1
			continue
		# validamos si palabra anterior adverbio de cantidad
		if (ind > 0 and listMorfo[ind-1] == "Adv. Cant"):
			tipo = "OD"
			listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
			ind += 1
			continue
		# valido si es complemento de compañia
		if (listMorfo[ind] == "Adv. Comp"):
			tipo = "C.Compania"
			listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+"-->"+tipo)
			ind += 1
			continue
		if (listMorfo[ind] == "Adv. Modo"):
                        tipo = "C.Modo"
                        listPar.append(tipo)
                        oraSal += palabra+" --> "+tipo+"\n"
			ind += 1
                        continue
        	#analizamos palabra por palabra
        	if (listMorfo[ind] == "Articulo"):
            		tipo = "DET"
            		listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
			ind += 1
			continue
        	if (ind == 0 and listMorfo[ind] not in ["Verbo","Adv. Luga"]):
			if (sujeto == True):
				tipo = "OD"
			else:
            			tipo = "SN"
            			sujeto = True
			listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
			ind += 1
                        continue
        	if (listMorfo[ind] == "Pron. Pers"):
		    # validamos si ya hay sujeto
		    if (sujeto == True):
			tipo = "OI"
		    else:
        	    	tipo = "SN"
        	    	sujeto = True
		    listPar.append(tipo)	
		    oraSal += palabra+" --> "+tipo+"\n"
		    print(palabra+" --> "+tipo)
		    ind += 1	
                    continue
		
		if (listMorfo[ind] == "Contraccion"):
		    tipo = "E"
		    listPar.append(tipo)
		    oraSal += palabra+" --> "+tipo+"\n"
		    print(palabra+" --> "+tipo)
		    ind += 1	
                    continue
	
        	if (ind >= 0 and listMorfo[ind-1] == "Verbo" and listMorfo[ind] == "Pron. Demo"):
        	    tipo = "Pronombre Demostrativo"
        	    listPar.append(tipo)
		    oraSal += palabra+" --> "+tipo+"\n"
		    print(palabra+" --> "+tipo)
		    ind += 1	
                    continue
	
        	if (ind > 0 and listMorfo[ind] == "Verbo" and listMorfo[ind-1] != "Articulo"):
            		# preguntamos por si es adverbio
            		if (palabra.lower() == "encima" and verbo):
               			tipo = "C.Lugar"
            		elif (palabra.lower() == "de"):
               			tipo = "E"
            		# consultamos si comienza con mayuscula sin ser la primera palabra
            		elif (palabra[0] >= 'A' and palabra[0] <= 'Z' and ind > 0):
               			tipo = "SN"
               			sujeto = True
            		else:
               			tipo = "NV"
               			verbo = True
			listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
			ind += 1
                        continue
        	if (ind > 0 and listMorfo[ind] != "Verbo" and listMorfo[ind-1] != "Articulo"):
			if (sujeto == True):
				# es objeto directo
				tipo = "OD"
			else:
            			tipo = "SN"
            			sujeto = True
			listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
			ind += 1
                        continue
        	if (listMorfo[ind] == "Adj. Pose"):
            		tipo = "Adjetivo Posesivo"
            		listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
			ind += 1
                        continue
        	if (listMorfo[ind] == "Conj. Copu"):
            		tipo = "Conjuncion Copulativa"
			# paso sujeto y el NV a false porque es otro nucleo
			sujeto = False
			verbo = False
            		listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
			ind += 1
                        continue
        	if (listMorfo[ind] == "Conj. Disy"):
        	    	tipo = "Conjuncion Disyuntiva"
        	    	listPar.append(tipo) 
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
			# paso sujeto y el NV a false porque es otro nucleo
                        sujeto = False
                        verbo = False
			ind += 1
                        continue
        	if (listMorfo[ind] == "Conj. Conc"):
            		tipo = "Conjuncion Concesiva"
            		listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
			ind += 1
                        continue
        	if (listMorfo[ind] == "Pron. Pers"):
			if (sujeto == True):
				tipo = "OD"
			else:
            			tipo = "SN"
            			sujeto = True
			listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
			ind += 1
                        continue
        	if (listMorfo[ind] == "Pron. Demo"):
            		tipo = "Pronombre demostrativo"
            		listPar.append(tipo)
			print(palabra+" --> "+tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			ind += 1
                        continue
        	if (listMorfo[ind] == "Adv. Luga"):
            		tipo = "C.Lugar"
            		listPar.append(tipo)
			print(palabra+" --> "+tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			ind += 1
                        continue
        	if (listMorfo[ind] == "Adv. Cant"):
            	# validamos si no es nucleo
            		if (ind > 0 and listMorfo[ind-1] == "Articulo"):
				# validamos que sea objeto en lugar de sujeto
				if (sujeto == True):
					# entonces es objeto
					tipo = "OD"
				else:
               				tipo = "SN"
               				sujeto = True
            		else:
               			tipo = "C.Cantidad"
			listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
			ind += 1
                        continue
        	if (listMorfo[ind] == "Adv. Tiem"):
            		if (ind > 0 and listMorfo[ind-1] == "Articulo"):
				# validamos si ya hay sujeto
				if (sujeto == True):
					tipo = "OD"
				else:
               				tipo = "SN"
               				sujeto = True
            		else:
               			tipo = "C.Tiempo"
			listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
			ind += 1
                        continue
        	if (listMorfo[ind] == "Adv. Duda"):
            		tipo = "C.Duda"
            		listPar.append(tipo)
			print(palabra+" --> "+tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			ind += 1
                        continue
        	if (listMorfo[ind] == "Adv. Afir"):
            		tipo = "C.Afirmacion"
            		listPar.append(tipo)
			print(palabra+" --> "+tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			ind += 1
                        continue
        	if (listMorfo[ind] == "Adv. Nega"):
            		tipo = "C.Negacion"
            		listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
			ind += 1
                        continue
            	# intentamos diferenciar objeto de sujeto
            	if (ind > 0 and verbo and sujeto and listMorfo[ind-1] != "Preposicion"):
               		tipo = "OD"
               		listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
			ind += 1
                        continue
		elif (ind > 0 and verbo and sujeto and listMorfo[ind-1] == "Preposicion"):
                        tipo = "OI"
                        listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
                        print(palabra+" --> "+tipo)
			ind += 1
                        continue
            	elif (sujeto and not verbo):
               		tipo = "Modif Directo"
               		listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
			ind += 1
                        continue
            	else:
			if (sujeto == True):
				tipo = "OD"
			else:
				if (verbo == True):
					tipo = "OD"
				else:
               				tipo = "SN"
               				sujeto = True
			listPar.append(tipo)
			oraSal += palabra+" --> "+tipo+"\n"
			print(palabra+" --> "+tipo)
			ind += 1
                        continue
	### TERMINA EL FOR ACA #######
    	# retorno diccionario con analisis sintactico
	print("########################################")
	print(str(listOra).encode('utf-8'))
	print(str(listPar))
	print("########################################")
	analSinOut = zip(listOra,listPar)
	self.grabarArchivoLog(str(analSinOut),"analisisOraciones.txt")
	self.grabarArchivoLog(str(oracion1),"TextosAnalizados.txt")
    	#return zip(listOra,listPar)
	return analSinOut,oraSal

    # tokenizar texto   
    def tokenTexto(self):
    	tokenText = []
    	# reemplazamos la , y el punto agregando espacios
    	texto2 = re.sub(","," ,",self.__texto)
    	texto3 = re.sub(";"," ;",texto2)
    	# ponemos slash al punto por ser comodin de re
    	texto4 = re.sub(r"\.",r" .",texto3)
    	# armamos una lista con el texto ingresado
    	return(texto4.split())

    # obtener secuencia de la palabras en texto
    def frecTexto(self):
   	# tokenizamos el texto
    	#listFrec = tokenTexto(texto)
    	listFrec = self.tokenTexto()
    	# ordenamos la lista
    	listOrd = sorted(listFrec)
    	#print(str(listOrd))
    	# iteramos contando los terminos q se repiten
    	i = 0
    	listCant = []
    	listFrecRet = []
    	palAnt = ""
    	for pal1 in listOrd:
       		#print("frecTexto: "+pal)
       		# pasamos a minuscula
       		pal = pal1.lower()
       		if (palAnt == pal or palAnt == ""):
       			# misma palabra, sumo uno
            		i = i + 1
            		palAnt = pal
        	else:
            		# agrego a lista la frecuencia de la palabra
            		listCant.append(i)
            		palAnt = pal
            		i = 1
    	listCant.append(i)
    	# usamos set para eliminar palabras repetidas
    	listSet = list(set(listOrd))
    	#print("listSet elem: "+str(len(listSet)))
    	listSet.sort()
    	# unimos ambas listas y retomamos la union
    	listFrecRet = list(zip(listSet,listCant))
    	#print("listFrecRet: "+str(listFrecRet))
    	return(listFrecRet)
        
	# analizamos texto completo
    def analisisTexto(self):
   	# separamos el texto en oraciones
    	# generamos lista de oraciones
    	duplas = []
    	oraList = self.__texto.split(".")
    	for ora in oraList:
       		# analizamos oracion por oracion
       		# agregamos el punto de final de oracion
       		# validamos si la oracion esta vacia
       		if (ora == ""):
         		continue
        	ora1 = ora+"."
        	duplas += self.sintaxAnal(ora1)
     	# asigno a analisisSin
     	self.__analisisSin = duplas
    	#self.resumirTexto(duplas)
    	#self.resumirTexto(analDict)
    	return duplas
    # funcion para generar resumen del texto
    def resumirTexto(self,dicAnal):
    		# solamente imprimo sujeto-verbo-objeto
    		listSal = [] # lista salida
    		# barremos el dic palabra por palabra para obtener Sujeto-verbo-objeto
    		#for pal in dicAnal.keys():
    		for pal in dicAnal:
    		    # validamos si la palabra es Sujeto-verbo-objeto
    		    #if (dicAnal[pal] in ["Sujeto","Verbo","Objeto"]):
    		    if (pal in ["Sujeto","Verbo","Objeto"]):
    		        listSal.append(pal)
    		print(str(listSal))
    		return listSal
    		        
       
################ MAIN ################################### 
