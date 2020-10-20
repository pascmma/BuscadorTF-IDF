from django.shortcuts import render
from django.http import HttpResponse
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
import json
import os
import time 
import operator
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 


def intersection(p1,p2,ranking,ranks,termino):
    if p1 is not None and p2 is not None:
        intersection = list(set(p1) & set(p2))
        for term in intersection:
            ranking [term] = ranking[term] * ranks[term][termino]

        return intersection,ranking
    else:
        return [],ranking


def union(p1,p2,ranking,ranks,termino):
    if p1 is not None and p2 is not None:
        unioon = list(set().union(p1,p2))
        # print(ranking)
        for term in unioon:
            if term in ranking.keys():
                ranking[term] = ranking[term] + ranks[term][termino]
            else:
                ranking[term] = ranks[term][termino]
        print(ranking)
        return unioon,ranking
    else:
        return [],ranking

def fnot(p1,p2,ranking,ranks,termino):
    rnot = list(set(p1) - set(p2))
    return rnot

def query_handler(query,dictionary,ranks):
    query = query.split(" ")
    term = query[0]
    posting = dictionary[term]
    documents = posting
    ranking = {}
    for item in documents:
        ranking[item] = ranks[item][term]

    for index in range(1,len(query)):
        if(query[index] == "AND"):
            op = '&'
        elif(query[index]== "OR"):
            op = '||'
        elif(query[index]== "NOT"):
            op = '!'
        else:
            if(op == '&'):
                term = query[index]
                term = dictionary[term]
                temp = intersection(documents,term,ranking,ranks,query[index])
                documents = temp[0]
                ranking = temp[1]
                # print(ranking)
            elif(op == '||'):
                term = query[index]
                term = dictionary[term]
                temp = union(documents,term,ranking,ranks,query[index])
                documents = temp[0]
                ranking = temp[1]

            elif(op == '!'):
                term = query[index]
                term = dictionary[term]
                documents = fnot(documents,term,ranking,ranks,query[index])
    # print(ranking)
    return documents,ranking

#cosine_similarity = 1 - spatial.distance.cosine(vector1, vector2)

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
    # dot = np.dot(vector1, vector2)
    # norma = np.linalg.norm(vector1)
    # normb = np.linalg.norm(vector2)
    # cos = dot / (norma * normb)
    # if cos == "nan":
    #     return 0

    # return cos




class clibro:
    def __init__(self, nombre,autor,txt,rank = 100, id=0):
        self.nombre = nombre
        self.autor = autor
        self.txt = txt
        self.rank = int(rank)
        self.id = id
    def __repr__(self):
        return self.nombre +"=>"+ self.txt

class clibrotf:
    def __init__(self, nombre,autor,txt,rank = 100, id=0):
        self.nombre = nombre
        self.autor = autor
        self.txt = txt
        self.rank = float(rank)
        self.id = id
    def __repr__(self):
        return self.nombre +"=>"+ self.txt

def busqueda(request):
    
    return render(request, "busqueda.html")

def buscar(request):
    
    with open(r'C:/Universidad/Topicos en Base de Datos/buscador/lebuscador/diccionario.json') as json_file: 
        dictionary = json.load(json_file) 

    with open(r'C:/Universidad/Topicos en Base de Datos/buscador/lebuscador/libros.json') as json_file2: 
        libros = json.load(json_file2) 
    
    with open(r'C:/Universidad/Topicos en Base de Datos/newtf/busqueda/search/ranks.json') as json_file3: 
        ranks = json.load(json_file3) 

    query = request.GET["pal"]    
    queryresponse = query_handler(query,dictionary,ranks)
    

    count = 1
    respuesta=[]
    for item in queryresponse:
        tmp = clibro(count,libros[item],item)
        respuesta.append(tmp)
        count += 1
    
        


    # return HttpResponse(msj,'resultados.html')
    
    return render(request,"resultados.html",{"palabra":query , "rest_query":respuesta , "num" : len(respuesta)})



def buscartf(request):
    
    with open(r'C:\Universidad\Topicos en Base de Datos\newtf\busqueda\search\libros.json') as json_file2: 
        libros = json.load(json_file2) 
    
    with open(r'C:\Universidad\Topicos en Base de Datos\newtf\busqueda\search\autores.json') as json_file4: 
        autores = json.load(json_file4) 
    
    query = request.GET["pal"]
    directorio = os.listdir('C:/Universidad/Topicos en Base de Datos/newtf/busqueda/search/Datosrank')
    
    stop_words = set(stopwords.words('english'))
    tok_query = word_tokenize(query)
    final_query = [word for word in tok_query if not word in stop_words]

    with open(r'C:\Universidad\Topicos en Base de Datos\newtf\busqueda\search\pal.json') as json_file: 
        pal = json.load(json_file) 

    print("Acabe la larga espera pal")

    with open(r'C:\Universidad\Topicos en Base de Datos\newtf\busqueda\search\queryw.json') as json_file: 
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
    with open(r'C:/Universidad/Topicos en Base de Datos/Actual/TF-IDF/tfidf.json') as json_file: 
        tfidf = json.load(json_file) 

    print("Acabe la larga espera tfidf")
    toc = time.perf_counter()
    print(f"Acabe de cargar en {toc - tic:0.4f} seconds")

    for documento in directorio:
        vaux = []
        for i in range(len(listidx)):
            if documento in tfidf:
                vaux.append(tfidf[documento][idx])
        vaux = cos_measure(vectorw_query,vaux)
        if vaux != 0.0:
            
            listrpt[documento] = vaux
        
    del tfidf
    
    print(listrpt)
    respuesta=[]
    for item in listrpt:
        if (item in libros) and (item in autores) :
            tmp = clibrotf(libros[item],autores[item],item,listrpt[item],)
            respuesta.append(tmp)
    
    sortedrp = sorted(respuesta, key=lambda x: x.rank, reverse=True)
    for i in range(len(sortedrp)):
        sortedrp[i].id = i+1
        sortedrp[i].rank = round(sortedrp[i].rank,5)
        
    return render(request,"tfresultados.html",{"palabra":query , "resultados":sortedrp , "num" : len(respuesta)})
