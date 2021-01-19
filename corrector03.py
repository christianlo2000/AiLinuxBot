from textblob import Word
import sys

word = sys.argv[1]
w = Word(word)
print(w.correct())
# chequeamos probabilidad de correcto
print(w.spellcheck())
