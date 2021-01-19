from nltk.stem import PorterStemmer

# definimos el objeto PorterStemmer
ps = PorterStemmer()
print(ps.stem("jumping"))
print(ps.stem("jumps"))
print(ps.stem("lying"))
print(ps.stem("core"))
