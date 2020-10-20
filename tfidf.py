import math
import os
import io 
import json

with open('tfp.json') as f:
    tf = json.load(f)
print("cargo el tf")

with open('idf2.json') as f:
    idf = json.load(f)

print("cargo el idf")

directorio = os.listdir('Datosrank/')

def multiplicacion(vector1,vector2):
    result =[]
    tam = 217301
    for i in range(0,tam):
        result.append(round(float(vector1[i])*float(vector2[i]),10))

    return result
cont = 0
dictionary = {}
for documento in directorio:
    aux = []
    vector1 = tf[documento]
    vector2 = idf[documento]
    # print(len(vector1))
    # print(len(vector2))
    aux = multiplicacion(vector1, vector2)
    dictionary[documento] = aux
    cont +=1
    print("contador", cont)
    


json = json.dumps(dictionary)
file = open('tfidf.json','w')
file.write(json)
file.close()
