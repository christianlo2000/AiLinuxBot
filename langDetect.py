from langdetect import detect

len1 = detect("War doesn't show who's right, just who's left.")
len2 = detect("Ein, zwei, drei, vier")
len3 = detect("Hola Guapa")
print("Lenguaje1: "+len1)
print("Lenguaje2: "+len2)
print("Lenguaje3: "+len3)
