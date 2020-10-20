import os
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
import json
import time

def cos_measure(vector1,vector2):
    sumat_pto = 0
    sumat_v1 = 0
    sumat_v2 = 0
    for i in range(len(vector1)):
        sumat_pto += float(vector1[i]) * float(vector2[i])
        sumat_v1 += float(vector1[i])**2
        sumat_v2 += float(vector2[i])**2
    sumat_v1 = sumat_v1**0.5
    if sumat_v1 == 0:
        sumat_v1 = 1
    sumat_v2 = sumat_v2**0.5
    if sumat_v2 == 0:
        sumat_v2 = 1
    
    measure = sumat_pto/(sumat_v1 * sumat_v2)
    return measure




directorio = os.listdir('Datosrank/')

query = "31483txt start project gutenberg ebook gaslight sonata produced suzanne shell"
stop_words = set(stopwords.words('english'))
tok_query = word_tokenize(query)
final_query = [word for word in tok_query if not word in stop_words]

with open('pal.json') as json_file: 
    pal = json.load(json_file) 

print("Acabe la larga espera pal")

with open('queryw.json') as json_file: 
    queryw = json.load(json_file) 

print("Acabe la larga espera query")
listidx = []
vectorw_query = []
for word in final_query:
    idx = pal.index(word)
    listidx.append(idx)
    vectorw_query.append(queryw[idx])

del queryw
del pal

print("Libere memoria")

listrpt = {}
tic = time.perf_counter()
with open('tfidf.json') as json_file: 
    tfidf = json.load(json_file) 

print("Acabe la larga espera tfidf")
toc = time.perf_counter()
print(f"Acabe de cargar en {toc - tic:0.4f} seconds")

for documento in directorio:
    vaux = []
    for i in range(len(listidx)):
        vaux.append(tfidf[documento][idx])
    vaux = cos_measure(vectorw_query,vaux)
    listrpt[documento] = vaux
    

print(listrpt)


