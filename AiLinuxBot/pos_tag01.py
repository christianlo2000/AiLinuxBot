# no funca error con spacy
import pandas as pd
import spacy

sentence = "the house is pretty."
nlp = spacy.load("en_core",parse=True,tag=True,entity=True)
sentence_nlp = nlp(sentence)
print(str(sentence_nlp))
# pos_tag with spacy
pos_tag = [(word, word.tag_, word.pos_) for word in sentence_nlp]
pd.DataFrame(pos_tag,columns=['Word','Pos Tag']).T
