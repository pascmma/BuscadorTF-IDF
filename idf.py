import os
import io
import json
from collections import Counter

directorio = os.listdir('Datosrank/')

with open('pal.json')as f:
    palabras = json.load(f)

with open('idfp.json')as f:
    idf = json.load(f)

with open('ranks.json')as f:
    ranks = json.load(f)
    

# for documento in ranks:
#     for key in documento:
#         idx = pal['pal'].index(key)
#         vector_query[idx] = tf[documento][key]
#     new_tf[documento]= vector_query

count = 0
count1 = 0
new_idf = {}
for documento in directorio:
    vector_vacio = []
    for word in palabras:
        vector_vacio.append(0)
    for word in idf:
        if word in ranks[documento]:
            idx = palabras.index(word)
            vector_vacio[idx] = idf[word]
    count += 1
    # print(count1)
    # print(len(ranks[documento]))
    print("Acabe ",count)
    new_idf[documento] = vector_vacio

json = json.dumps(new_idf)
file = open('idf2.json','w')
file.write(json)
file.close()
