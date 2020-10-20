import os
import io
import json
from collections import Counter
from nltk.stem import WordNetLemmatizer



with open('Rankss.json')as f:
    rankings = json.load(f)

directorio = os.listdir('Datosrank/')
"""
wordnet = WordNetLemmatizer()
dictionary={}
aux = {}

#aux = rankings[directorio[0]]
for i in range(0, len(directorio)):
    valores =[]
    aux = rankings[directorio[i]]
    n_valores = aux.values()
    
    maximo = max(valores)
    result = {key:aux[key] / maximo for key in aux.keys()}
    dictionary[directorio[i]] = result

json = json.dumps(dictionary)
file = open('tf2.json','w')
file.write(json)
file.close()

"""

# nueva forma de realizar el TF
directorio = os.listdir('Datosrank/')

with open('pal.json')as f:
    palabras = json.load(f)

with open('tf.json')as f:
    tf = json.load(f)

with open('ranks.json')as f:
    ranks = json.load(f)


#vector_vacio = []
# for word in palabras:
#     vector_vacio.append(0)


aux ={}
n_tf={}
cont =0
for documento in directorio:
    vector_vacio = []
    for word in palabras:
        vector_vacio.append(0)
    print(documento)
    for key in tf[documento]:
        cont +=1
        
       # print("contador",cont)
        if key in ranks[documento]:
            idx = palabras.index(key)
            vector_vacio[idx] = tf[documento][key]
    n_tf[documento] = vector_vacio
    
    

    



json = json.dumps(n_tf)
file = open('tfp.json','w')
file.write(json)
file.close()






