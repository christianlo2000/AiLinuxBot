import pandas as pd
import nltk
import sys

#sentence = "the house is pretty."
if (sys.argv[1] == ""):
	print("Modo de Uso: python3 pos_tag02.py oracion_cerrada_entre_comillas")
	exit(-1)
sentence = sys.argv[1]
# pos_tag with nltk
pos_tag = nltk.pos_tag(nltk.word_tokenize(sentence))
print(str(pd.DataFrame(pos_tag,columns=['Word','Pos Tag']).T))
