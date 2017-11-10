#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
from google.cloud import bigquery
from google.cloud.bigquery.schema import SchemaField
from nltk.corpus import stopwords
from datetime import datetime
from math import log
import random
from datetime import datetime
from nltk import UnigramTagger
import pickle
import sys
from nltk.stem.snowball import SnowballStemmer
reload(sys)
sys.setdefaultencoding("ISO-8859-1")



class Recomendaciones:
 """
  clase la cual contiene el algoritmo Recomendaciones
 """

 def Recomendar(self,patron,precio,categoriasitio,historial,Phi,LimiteFechaDias=15):
  """ En este apartado tenemos el algoritmo de recomendar en tryme """
  i=0
  fecha1 = datetime.now()
  CadenaSQL=""""""
  TerminosRelevantesUsuario=[]
  
  TokensPatron=nltk.word_tokenize(patron[0].lower())
   
  StopWordsSpanish=stopwords.words('spanish')
  TokensPatronTemporal=[]
  ListaCategoriaSitio=categoriasitio.split(",")
  ListaCategoriaSitio=[a.lower() for a in ListaCategoriaSitio]

  for b in TokensPatron:
   IsStopWord=False
   for a in StopWordsSpanish:
    if(a.lower()==b):
     IsStopWord=True
   if not(IsStopWord):
    TokensPatronTemporal=TokensPatronTemporal+[b]

  TokensPatron=TokensPatronTemporal  
  
  with open('UnigramaEntrenado.pkl', 'rb') as input:
    uni_tag = pickle.load(input)

  TokensPatronTemp=[]

  for a in uni_tag.tag(TokensPatron):
   unigram=a
   if(unigram[1]==None):
    TokensPatronTemp=TokensPatronTemp+[unigram[0]]
   elif(unigram[1][0]=='Z'):
    TokensPatronTemp=TokensPatronTemp+[unigram[0]]
   elif(unigram[1][0]=='n'):
    TokensPatronTemp=TokensPatronTemp+[unigram[0]]     
  
  TokensPatron=TokensPatronTemp
  TokensPatronTemp=[]
  
  stemmer = SnowballStemmer("spanish",ignore_stopwords=False)
  SinRuidoPatron=[]
  SinRuidoPatron= [stemmer.stem(a) for a in TokensPatron]

  print SinRuidoPatron  
  historial_temp=historial
  historial=[]  

  for a in historial_temp:
   if (len(a)==2):
    Fecha_Iteam=a[1].split("/")
    fecha2 = datetime(int(Fecha_Iteam[2]),int(Fecha_Iteam[1]),int(Fecha_Iteam[0]), 0, 0, 0)
    diferencia = fecha1-fecha2
    if(diferencia.days <= LimiteFechaDias):
     historial=historial+[a[0]]
   else:
    historial=historial+[a[0]]

  for iteam  in historial:
   Desicion=True
   for a in SinRuidoPatron:
    if not(a.upper() in iteam.upper()):
     TerminosRelevantesUsuario=[iteam]+TerminosRelevantesUsuario

  Temp_TerminosRelevantesUsuario=[]

  for b in TerminosRelevantesUsuario:
   TokensTerminoRelevanteUsuario=nltk.word_tokenize(b.upper())
   for TokenUsuario in TokensTerminoRelevanteUsuario:
    IsStopWord=False
    for a in StopWordsSpanish:
     if(TokenUsuario.upper()==a.upper()):
      IsStopWord=True
    if not(IsStopWord):
     Temp_TerminosRelevantesUsuario=Temp_TerminosRelevantesUsuario+[TokenUsuario]

  TerminosRelevantesUsuario = [stemmer.stem(a) for a in Temp_TerminosRelevantesUsuario]
  TerminosRelevantesUsuario=list(set(TerminosRelevantesUsuario))
  Temp_TerminosRelevantesUsuario=[]


  while(i<(len(SinRuidoPatron)-1)):
   CadenaSQL=CadenaSQL+"""lower(producto) like '%"""+SinRuidoPatron[i]+"""%' or """
   i=i+1

  if (len(SinRuidoPatron)>0):
   CadenaSQL=CadenaSQL+"""lower(producto) like '%"""+SinRuidoPatron[len(SinRuidoPatron)-1]+"""%' """

  CadenaSQL="""("""+CadenaSQL+""")"""

  
  CadenaSQLDos=""""""
  i=0
 

  while(i<(len(ListaCategoriaSitio)-1)):
   CadenaSQLDos=CadenaSQLDos+"""lower(categoriasitio) like '%#"""+ListaCategoriaSitio[i]+"""%' or """
   i=i+1

  if (len(ListaCategoriaSitio)>0):
   CadenaSQLDos=CadenaSQLDos+"""lower(categoriasitio) like '%#"""+ListaCategoriaSitio[len(ListaCategoriaSitio)-1]+"""%' """

 

  CadenaSQLDos="""("""+CadenaSQLDos+""")"""


  client = bigquery.Client.from_service_account_json('/home/david_borja/CredencialesBigQuery/DjangoAplicacion/service_account.json')

  QueryString="""
     #standardSQL
  """+"""SELECT id_producto,producto,precio FROM `tryme-180122.sitiosproductos.producto` where ((precio>0)and (precio<"""+str(precio)+""") and (categoriasitio!='None')  and (producto != 'None' ) and  """+CadenaSQL+""" and  """+CadenaSQLDos+""")  """

  query_job = client.query(QueryString)
  assert query_job.state == 'RUNNING'
  TIMEOUT=20
  iterator = query_job.result(timeout=TIMEOUT)
  rows = list(iterator)
  assert query_job.state == 'DONE'


  ListaDeClasificacion=[]

  if (len(TerminosRelevantesUsuario)>0):
   SinRuidoPatron=SinRuidoPatron+[random.choice(TerminosRelevantesUsuario)]

  NDT=[1.0]*len(SinRuidoPatron)
  MaquinaEstadosNDT=['0']*len(SinRuidoPatron)
  DimensionalidadDocumento=0.0

  for row in rows:
   DimensionalidadDocumento=DimensionalidadDocumento+1.0
   Codificacion=row[1].encode('utf-8').strip()
   Codificacion=Codificacion.replace('"',"")
   Codificacion=Codificacion.lower()
   TokensMedoide=nltk.word_tokenize(Codificacion)
   SinRuidoMedoide=[]
   SinRuidoMedoide= [stemmer.stem(b) for b in TokensMedoide]
   #SinRuidoMedoide= [b for b in TokensMedoide]
   Frecuencia=[0.0]*len(SinRuidoPatron)

   i=0

   for a in SinRuidoPatron:
    for b in SinRuidoMedoide:
     if (a==b):
      if(MaquinaEstadosNDT[i]=='0'):
       NDT[i]=NDT[i]+1
       MaquinaEstadosNDT[i]='a'
    MaquinaEstadosNDT[i]='0'
    i=i+1

   i=0
   for a in SinRuidoPatron:
    for b in SinRuidoMedoide:
     if(a==b):
      Frecuencia[i]=Frecuencia[i]+1.0
    i=i+1

   ListaDeClasificacion=ListaDeClasificacion+[[row[0],Codificacion,Frecuencia,row[2]]]


  i=0

  while i <len(ListaDeClasificacion):
   j=0
   while (j<len(NDT)):
    TF=ListaDeClasificacion[i][2][j]
    IDF=(log(DimensionalidadDocumento/NDT[j]))
    TF_IDF=(TF*IDF)
    ListaDeClasificacion[i][2][j]=TF_IDF
    j=j+1
   i=i+1
  i=0

  while i < len(ListaDeClasificacion):
   j=0
   Suma=0
   while j < len(ListaDeClasificacion[i][2]):
    Suma=(Suma+ListaDeClasificacion[i][2][j])
    j=j+1
   Suma= float(Suma)/float(len(ListaDeClasificacion[i][1]))
   ListaDeClasificacion[i][2]=Suma
   i=i+1

  ListaDeClasificacion.sort(key=lambda x: x[2],reverse=True)
  ListaDeClasificacion=ListaDeClasificacion[:Phi]
  ListaDeClasificacion=[[a[0],a[1],len([stemmer.stem(aa)  for aa in nltk.word_tokenize(a[1])]),a[3]] for a in ListaDeClasificacion]
  BloqueDePrecios=[a[2] for a in ListaDeClasificacion]
  BloqueDePrecios=sorted(list(set(BloqueDePrecios)))
  ListaBucketSort=[]

  for a in BloqueDePrecios:
   bucket=[]
   for b in ListaDeClasificacion:
    if (a == b[2]):
     bucket=bucket+[[b[0],b[1],b[3]]]
   bucket.sort(key=lambda x: x[2])
   ListaBucketSort=ListaBucketSort+bucket

  ListaBucketSort=[a[0] for a  in ListaBucketSort]

  return ListaBucketSort
  

class Buscador:
    
 """
  clase la cual contiene el algoritmo Buscacor
 """
       
 
 def Buscar(self,patron,historial,Phi,LimiteFechaDias=15):
  
  """
   En este paratado tenemos el algoritmo para buscar en tryme.
  """
  i=0
  fecha1 = datetime.now()
  CadenaSQL=""""""
  TerminosRelevantesUsuario=[]
  TokensPatron=nltk.word_tokenize(patron[0].lower())
  StopWordsSpanish=stopwords.words('spanish')
  TokensPatronTemporal=[]

  for b in TokensPatron:
   IsStopWord=False
   for a in StopWordsSpanish:
    if(a==b):
     IsStopWord=True
   if not(IsStopWord):
    TokensPatronTemporal=TokensPatronTemporal+[b]

  TokensPatron=TokensPatronTemporal

  stemmer = SnowballStemmer("spanish",ignore_stopwords=False)
  SinRuidoPatron=[]
  SinRuidoPatron= [stemmer.stem(a) for a in TokensPatron]

  historial_temp=historial
  historial=[]

  for a in historial_temp:
   if (len(a)==2):
    Fecha_Iteam=a[1].split("/")
    fecha2 = datetime(int(Fecha_Iteam[2]),int(Fecha_Iteam[1]),int(Fecha_Iteam[0]), 0, 0, 0)
    diferencia = fecha1-fecha2
    if(diferencia.days <= LimiteFechaDias):
     historial=historial+[a[0]]
   else:
    historial=historial+[a[0]]  
 
  for iteam  in historial:
   Desicion=True   
   for a in SinRuidoPatron:
    if not(a.upper() in iteam.upper()):
     Desicion=False
   if Desicion:
    TerminosRelevantesUsuario=[iteam]+TerminosRelevantesUsuario

  Temp_TerminosRelevantesUsuario=[]

  for b in TerminosRelevantesUsuario:
   TokensTerminoRelevanteUsuario=nltk.word_tokenize(b.upper())
   for TokenUsuario in TokensTerminoRelevanteUsuario:
    IsStopWord=False
    for a in StopWordsSpanish:
     if(TokenUsuario==a.upper()):
      IsStopWord=True
    if not(IsStopWord):
     Temp_TerminosRelevantesUsuario=Temp_TerminosRelevantesUsuario+[TokenUsuario]
  

  TerminosRelevantesUsuario = [stemmer.stem(a) for a in Temp_TerminosRelevantesUsuario]
  TerminosRelevantesUsuario=list(set(TerminosRelevantesUsuario))
  Temp_TerminosRelevantesUsuario=[]  

  for a in TerminosRelevantesUsuario:
   Existe=False
   for b in SinRuidoPatron:
    if(a.upper() == b.upper()):
     Existe=True
   if not(Existe):
    Temp_TerminosRelevantesUsuario= Temp_TerminosRelevantesUsuario+[a]

  TerminosRelevantesUsuario=Temp_TerminosRelevantesUsuario

  
  while(i<(len(SinRuidoPatron)-1)):
   CadenaSQL=CadenaSQL+"""lower(producto) like '%"""+SinRuidoPatron[i]+"""%' and """
   i=i+1
 
  if (len(SinRuidoPatron)>0):
   CadenaSQL=CadenaSQL+"""lower(producto) like '%"""+SinRuidoPatron[len(SinRuidoPatron)-1]+"""%' """

 
  CadenaSQL="""("""+CadenaSQL+""")"""

  client = bigquery.Client.from_service_account_json('/home/david_borja/CredencialesBigQuery/DjangoAplicacion/service_account.json')
  
  
  QueryString="""
     #standardSQL
  """+"""SELECT id_producto,producto,precio FROM `tryme-180122.sitiosproductos.producto` where ((precio>0)and(producto != 'None' ) and  """+CadenaSQL+""") """

  query_job = client.query(QueryString)
  assert query_job.state == 'RUNNING'
    
  TIMEOUT=20
  iterator = query_job.result(timeout=TIMEOUT)
  rows = list(iterator)

  assert query_job.state == 'DONE'
 
  ListaDeClasificacion=[] 

  if (len(TerminosRelevantesUsuario)>0):
   SinRuidoPatron=SinRuidoPatron+[random.choice(TerminosRelevantesUsuario)]

  NDT=[1.0]*len(SinRuidoPatron)   
  MaquinaEstadosNDT=['0']*len(SinRuidoPatron)
  DimensionalidadDocumento=0.0

  for row in rows: 
   DimensionalidadDocumento=DimensionalidadDocumento+1.0
   Codificacion=row[1].encode('utf-8').strip()
   Codificacion=Codificacion.replace('"',"")
   Codificacion=Codificacion.lower()
   TokensMedoide=nltk.word_tokenize(Codificacion)
   SinRuidoMedoide=[]
   SinRuidoMedoide= [stemmer.stem(b) for b in TokensMedoide]
   Frecuencia=[0.0]*len(SinRuidoPatron)
   i=0
   
  
   for a in SinRuidoPatron:
    for b in SinRuidoMedoide:
     if (a==b):
      if(MaquinaEstadosNDT[i]=='0'):
       NDT[i]=NDT[i]+1
       MaquinaEstadosNDT[i]='a'
    MaquinaEstadosNDT[i]='0'        
    i=i+1
  
   i=0
   for a in SinRuidoPatron:
    for b in SinRuidoMedoide:
     if(a==b):
      Frecuencia[i]=Frecuencia[i]+1.0
    i=i+1 


   ListaDeClasificacion=ListaDeClasificacion+[[row[0],Codificacion,Frecuencia,row[2]]]
  
 
  i=0
  while i <len(ListaDeClasificacion):
   j=0
   while (j<len(NDT)):
    TF=ListaDeClasificacion[i][2][j]
    IDF=(log(DimensionalidadDocumento/NDT[j]))
    TF_IDF=(TF*IDF)
    ListaDeClasificacion[i][2][j]=TF_IDF
    j=j+1
   i=i+1
  
  i=0
  while i < len(ListaDeClasificacion):
   j=0
   Suma=0
   while j < len(ListaDeClasificacion[i][2]):
    Suma=(Suma+ListaDeClasificacion[i][2][j])       
    j=j+1 

   Suma= float(Suma)/float(len(ListaDeClasificacion[i][1]))
   ListaDeClasificacion[i][2]=Suma
   i=i+1

  ListaDeClasificacion.sort(key=lambda x: x[2],reverse=True)
  
  ListaDeClasificacion=ListaDeClasificacion[:Phi]
  ListaDeClasificacion=[[a[0],a[1],len([stemmer.stem(aa)  for aa in nltk.word_tokenize(a[1])]),a[3]] for a in ListaDeClasificacion]
  BloqueDePrecios=[a[2] for a in ListaDeClasificacion]
  BloqueDePrecios=sorted(list(set(BloqueDePrecios)))
  
  ListaBucketSort=[]   

  for a in BloqueDePrecios:
   bucket=[]
   for b in ListaDeClasificacion:
    if (a == b[2]):
     bucket=bucket+[[b[0],b[1],b[3]]]
   bucket.sort(key=lambda x: x[2])
   ListaBucketSort=ListaBucketSort+bucket

  ListaBucketSort=[a[0] for a  in ListaBucketSort]
    
  return ListaBucketSort
    
