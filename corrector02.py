from textblob import Word

w = Word("finayll")
print(w.correct())
# chequeamos probabilidad de correcto
print(w.spellcheck())
# probamos otra palabra
w = Word("flaot")
print(w.correct())
print(w.spellcheck())
