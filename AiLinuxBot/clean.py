
import re

def clean_text1(texto):
        #listTextTrash = ["(","]","}",")","[","{","/","\"]
        listTextTrash = ["(","]","}",")","[","{","/","\\"]
        #listTextTrash = ["(","]","}",")","[","{"]
        textOut = texto
        for basura in listTextTrash:
                textOut = textOut.replace(basura," ")
        return textOut

texto = "Esto es una/prueba para ver como funca."

print(clean_text1(texto))
