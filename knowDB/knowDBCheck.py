## Script.....: knowDBCheck.py
## Objetivo...: validar del log si las respuesta fueron correctas, a traves del operador que corrija los resultados del chatbot
## Parametros.: log file donde se encuentra la pregunta del usuario. se toma el tercer campo que tiene la pregunta. fecha del log a validar.
## salida.....: genera archivo de salida con la pregunta, respuesta original del chatbot, valoracion de respuesta (correcta,incorrecta, aprox), respuesta correcta.

## Estado.....: en construccion. Falta agregar tema fechas

import sys

# validamos cantidad de parametros
if (len(sys.argv) < 2):
	modoUso = "Modo de uso: "+sys.argv[0]+" nombreFileLog"+" fecha log"
	print(modoUso)
	exit(-1)
# abrimos y leemos el archivo de log
logName = sys.argv[1]
logFile = open(logName,"r")
knowDB = open("./knowDB.txt","a")
listReg = []
while(True):
	reg = logFile.readline()
	# validamos si es fin de archivo
	if (reg == ""):
		break
	listReg = reg.split("|")
	textoPreg = "La pregunta: "+listReg[2]+", cuya respuesta el chatbot dio: "+listReg[5]+" es correcta (S/N/M - S = SI; N = NO; A = APROX)?"
	resp = input(textoPreg)
	# respuesta NO Correcta
	if (resp == "N"):
		textoRes = input("ingrese la respuesta correcta: ")
		salidaReg = listReg[2]+"|"+listReg[5].rstrip('\n')+"|"+resp+"|"+textoRes.rstrip('\n')
	# respuesta correcta
	elif (resp == "S"):
		 salidaReg = listReg[2]+"|"+listReg[5].rstrip('\n')+"|"+resp.rstrip('\n')+"|"+listReg[5].rstrip('\n')
	# respuesta aprox
	else:
		textoRes = input("ingrese la respuesta mas precisa: ")
		salidaReg = listReg[2]+"|"+listReg[5].rstrip('\n')+"|"+resp.rstrip('\n')+"|"+textoRes.rstrip('\n')
	# grabamos archivo salida
	knowDB.write(salidaReg+'\n')
		
# cerramos los archivos
knowDB.close()
logFile.close()


