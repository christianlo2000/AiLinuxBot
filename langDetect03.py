import nltk

tc = nltk.classify.textcat.TextCat() 

texto = input("Ingrese una oracion: ")
guess_lang = tc.guess_language(texto)
print("Idioma: "+guess_lang)

