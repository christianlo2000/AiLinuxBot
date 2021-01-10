from nltk.corpus import wordnet
import sys
import random

def exist(palabra):
	# asumo que si tiene sinonimos existe
	if (wordnet.synsets(palabra)):
		return True
	return False

def anagramGen(palabra):
	if (exist(palabra) == False):
		# busco palabras que sean anagramas
		i = 0
		while(i <= len(palabra)*29*len(palabra)):
			str_var = list(palabra)
			random.shuffle(str_var)
			newpal =  ''.join(str_var)
			print("newpal: "+newpal)
			if (exist(newpal)):
				return newpal
			i += 1
			str_var = []	
	return False
if __name__ == "__main__":
	palabra = sys.argv[1]
	if (exist(palabra)):
		print("Palabra "+palabra+" Existe")
	else:
		print("Palabra "+palabra+" NO Existe")
		print("buscamos generar palabra existente con Anagrama")
		print(anagramGen(palabra))
