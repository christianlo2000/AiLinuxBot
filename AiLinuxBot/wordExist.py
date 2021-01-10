from nltk.corpus import wordnet
import numpy as np
import sys

def exist(palabra):
	# asumo que si tiene sinonimos existe
	if (wordnet.synsets(palabra)):
		return True
	return False

if __name__ == "__main__":
	if (exist(sys.argv[1])):
		print("Palabra "+sys.argv[1]+" Existe")
	else:
		print("Palabra "+sys.argv[1]+" NO Existe")
