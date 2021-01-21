import nltk
import pycountry
from nltk.stem import SnowballStemmer

phrase_one = "good morning"
phrase_two = "hey guy I'm bussy"

tc = nltk.classify.textcat.TextCat() 
guess_one = tc.guess_language(phrase_one)
guess_two = tc.guess_language(phrase_two)

guess_one_name = pycountry.languages.get(alpha_3=guess_one).name
guess_two_name = pycountry.languages.get(alpha_3=guess_two).name
print(guess_one_name)
print(guess_two_name)

texto = input("Ingrese una oracion: ")
guess_lang = tc.guess_language(texto)
print("Idioma: "+guess_lang)

