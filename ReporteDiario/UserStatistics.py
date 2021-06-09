# -*- coding: utf-8 -*-
"""
Created on Tue May  4 17:03:41 2021

@author: tvnne
"""

from PIL import Image
import tweepy
from nltk.tokenize import word_tokenize
import re
from collections import Counter
#import operator
from nltk.corpus import stopwords
#import string
from nltk import bigrams 
from nltk.util import ngrams
from collections import defaultdict
import numpy as np
import nltk
import datetime
nltk.download('punkt')
nltk.download('stopwords')
#import codecs
#from spanish_stopwords import espanol
#from propuestas_stopwords import propuestas_words
#import MySQLdb
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import unicodedata
import sys
import random

import os

#from getTweets_V0 import getTweets


def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def clean_text(text):
    text_ = strip_accents(text) 
    text_ = re.sub(r'http[s]?://(?:[a-z]|[0-9]|[$-@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+','',text_)  #remove urls
    text_ = re.sub(r'[^A-Za-z\s]+','',text_)    #remove everything except alphabets/words
    return text_

def wcloud(text,name):

     mask = np.array(Image.open("cloud.png"))  

     STOPWORDS = stopwords.words('spanish')
     wc = WordCloud(background_color="white",
                    mask=mask,
#                    max_words=80,
                    max_words=160,
#                    stopwords=stopwords,                    
                    stopwords=STOPWORDS,
                    width=800,
                    height=400,
                    mode="RGB",
                    relative_scaling=0.5,
                    prefer_horizontal=0.9
                    )

     wc.generate(text)
     
     wc.recolor(color_func=color_func)
     
     file_name = name + '/' + name +'.pdf'
     wc.to_file(file_name)

     return

def color_func(word, font_size, position, orientation,**kwargs):

    random_num = random.randint(1,4)
    if random_num==1:
        colors_ = "rgb(255, 91, 0)"
    elif random_num==2:
        colors_ = "rgb(44, 88, 137)"
    elif random_num==3:            
        colors_ = "rgb(119, 159, 212)"
    elif random_num==4:            
        colors_ = "rgb(192, 213, 238)"    
    return colors_


consumer_key = '6vHaS4hBb1zpAbLdDhfhRkEKc'
consumer_secret = 'voPnvROC9U8sRvpKwuWSh50OxdQ2n594l4lKUG0QxbUjKBH4oV'
access_token = '1061012155535945728-tA7qrTSeW8lG84rgjzb5bAMPNI0r5D'
access_token_secret = 'P77agZo2Ngbuk9wD4F0w0ILzw5PHxlmS2ruzclVXpbv7J'

#consumer_key = '5EiLFzJwbNz3OhvjO8BNfQgty'
#consumer_secret = 'Mglhl7T1qMW4r2rlr0aoSOLLYbotZfnvgItv0t1zLbqGn5CeSJ'
#access_token = '1072501856-SGzlUWEhzVe6U87cqIRpFjRVeHSfBlYxA9abIcd'
#access_token_secret = 'cC0oWg5CH7ap5fhiCqQSNR40rDnEZ6XJzgsaYRZ3Pu0SN'

#import tweepy

# Replace the API_KEY and API_SECRET with your application's key and secret.
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth)
results_Duque_RT=[]
all_ = []
users=['greenfieldjackt']
results = results_Duque_RT
id_list = [str(tweet.id) for tweet in results]
TweetsPersonajes = pd.DataFrame(id_list,columns=["id"])
for i in range(0,len(users)):
    results_Duque_RT = []
    counter = 1
    tweetsPerQry = 100
    screen_name = users[i]
    for tweet in tweepy.Cursor(api.user_timeline, id = screen_name, count=tweetsPerQry, tweet_mode="extended").items(10000):                                
        results_Duque_RT.append(tweet)
        counter+=1
        print(str(counter))
    print('Total Tweets so far %s' %(str(len(results_Duque_RT))))
    
    results = results_Duque_RT
    
    id_list = [str(tweet.id) for tweet in results]
    data_set = pd.DataFrame(id_list,columns=["id"])
    #Precessing Tweet Data
    
    data_set["text"] = [tweet.full_text for tweet in results]
    data_set["created_at"] = [tweet.created_at for tweet in results]
    data_set["retweet_count"] = [tweet.retweet_count for tweet in results]
    data_set["favorite_count"] = [tweet.favorite_count for tweet in results]
    data_set["url_Tweet"]=["https://twitter.com/"+users[i]+"/status/"+tweet.id_str for tweet in results]
    data_set["source"] = [tweet.source for tweet in results]
    data_set["coordinates"]=[tweet.coordinates for tweet in results]
    data_set["geo"]=[tweet.geo for tweet in results]
    data_set["lang"]=[tweet.lang for tweet in results]
    
    #data_set["possibly_sensitive"]=[tweet.possibly_sensitive for tweet in results]
    #data_set["retweeted"]=[tweet.retweeted for tweet in results]
    
    
    
    data_set["listed_count"]=[tweet.author.listed_count for tweet in results]
    
    
    HashtagList=[]
    Usermen=[]
    
    for tweet in results:
        l=""
        for p in tweet.entities["hashtags"]:
            if l=="":
                l=p["text"]
            else:
                l=l+","+p["text"]
        
        HashtagList.append(l)
        mum=""
        for k in tweet.entities["user_mentions"]:
            if mum=="":
                mum=k["screen_name"]
            else:
                mum=mum+","+k["screen_name"]
        
        Usermen.append(mum)
        
                
    
    data_set["hashtags"]=HashtagList
    data_set["user_mentions"]=Usermen    
    

#Datos Personales
#Url_Img_User=results[0].author.profile_image_url
#Descripcion=results[0].author.description
#Localizacion=results[0].author.location
#username=results[0].author.screen_name
#Nombre = results[0].author.name
#Fecha_Creacion=results[0].author.created_at
#Num_Seguidores=results[0].author.followers_count
#Num_amigos=results[0].author.friends_count
    data_set["listed_count"]=[tweet.author.listed_count for tweet in results]

i=["Nombre", "Username", "Localizacion", "Descripción", "Followers", "Siguiendo", "Listas", "Fecha de Creación", "Profile_image_url"]
l=[results[0].author.name, results[0].author.screen_name, results[0].author.location, results[0].author.description, results[0].author.followers_count,results[0].author.friends_count,results[0].author.listed_count, results[0].author.created_at, results[0].author.profile_image_url]


df = pd.DataFrame({'Nombre':i,'Valor':l})


#Evaluar si es Retweet o post original.
data_set['RT']=[1 if 'RT @' in str(x)[:] else 0 for x in data_set.text]

#Separa el contenido el created_at en fecha y hora
# new data frame with split value columns 
#data_set["Fecha"] = data_set["created_at"].str.split(" ", n = 1, expand = True)


from datetime import datetime
data_set["created_at"] = pd.to_datetime(data_set["created_at"])-pd.Timedelta('5 hours')
data_set["dia"]=data_set.created_at.map(lambda x: x.strftime('%A'))

data_FI=data_set[["created_at", "RT"]]

data_FR=data_set[data_set["RT"]==1]
data_FR=data_FR[["created_at", "RT"]]


###################################################################################################
########################## Horas  #################################################################


data_FI_D=data_FI.set_index('created_at').resample('D').count()
data_FI_D.columns=["Interaciones"]
data_FI_D['index1'] = data_FI_D.index


#Filtro para Retweet y Tweet Original
#Para Rwtweets

data_FR_D=data_FR.set_index('created_at').resample('D').count()
data_FR_D.columns=["Retweets"]
data_FR_D['index1'] = data_FR_D.index


Resul_Dia=pd.merge(data_FI_D, data_FR_D, how ='inner', on ='index1') 
Resul_Dia["dia"]=Resul_Dia.index1.map(lambda x: x.strftime('%A'))

###################################################################################################
###########################   Semanal   ###########################################################

data_FI_S=data_FI.set_index('created_at').resample('W').count()
data_FI_S.columns=["Interaciones"]
data_FI_S['index1'] = data_FI_S.index


data_FR_S=data_FR.set_index('created_at').resample('W').count()
data_FR_S.columns=["Retweets"]
data_FR_S['index1'] = data_FR_S.index

Resul_Semanal=pd.merge(data_FI_S, data_FR_D, how ='inner', on ='index1') 

###################################################################################################
########################## Horas  #################################################################

data_FI_H=data_FI.set_index('created_at').resample('H').count()
data_FI_H.columns=["Interaciones"]
data_FI_H['index1'] = data_FI_H.index


data_FR_H=data_FR.set_index('created_at').resample('H').count()
data_FR_H.columns=["Retweets"]
data_FR_H['index1'] = data_FR_H.index

Resul_Hora=pd.merge(data_FI_H, data_FR_H, how ='inner', on ='index1') 

#%%
###### GENERACIÓN DEL ARCHIVO DE DATOS DE USUARIO ################################################
#os.mkdir('JCastroS')
writer = pd.ExcelWriter(users[0]+'.xlsx', engine='xlsxwriter')
df.to_excel(writer,sheet_name='DatosPersonales')
data_set.to_excel(writer,sheet_name='Tweets')
Resul_Dia.to_excel(writer, sheet_name='Diario')
Resul_Semanal.to_excel(writer, sheet_name='Semanal')
Resul_Hora.to_excel(writer, sheet_name='Hora')
#A_Losquesigue.to_excel(writer,sheet_name='Siguiendo')
writer.save()

    
#TweetsPersonajes = pd.concat([TweetsPersonajes,data_set])
##### Aquí va la validación de usuarios############

#%%
#### GENERACIÓN DE MENSAJE "DATOS DEL USUARIO" ####

#Lectura de datos

#Cargados desde el proceso de descarga de datos
Datper = pd.read_excel(users[0]+'.xlsx', sheet_name = 'DatosPersonales')
Datweets = pd.read_excel(users[0]+'.xlsx', sheet_name = 'Tweets')

#Cargados directamente de la carpeta
#Datper = pd.read_excel('GustavoBolivar.xlsx', sheet_name = 'DatosPersonales')
#Datweets = pd.read_excel('GustavoBolivar.xlsx', sheet_name = 'Tweets')

#Validación para ubicación
if isinstance(Datper['Valor'][2], float) :
    datubic = '_No registra ubicación_'
else:
    datubic = Datper['Valor'][2]
    
#Validación para Biografia
if isinstance(Datper['Valor'][3], float) :
    datbio = '_No registra biografía_'
else:
    datbio = Datper['Valor'][3]

#Filtros de Tweets Respuesta, Rts y Originales
Tweresp = Datweets['Resp'] = [1 if '@' in str(x)[0] else 0 for x in Datweets.text]
TweRT = Datweets['RT'] = [1 if 'RT @' in str(x)[0:4] else 0 for x in Datweets.text]
TweORI1 = Datweets[Datweets['Resp']== 0]
TweORI2 = TweORI1[TweORI1['RT']== 0]
TweORI = TweORI2['Ori'] = [1 if '0' in str(x) else 0 for x in TweORI2.RT]
#Nota: Los que tienen 1 en "Resp" Datweets son los tweets respuesta
#Nota: Los que tienen 1 en "RT" Datweets  son los RTs
#Nota: TweORI2 son originales

#Calculo de promedio de tweets respuesta
data_Resp = Datweets[Datweets["Resp"]==1]
if len(data_Resp) == 0:
    meanResp = 0
else:
    sumdiaResp = data_Resp.groupby(('dia')).Resp.sum()
    meanResp = round(sumdiaResp.mean())

#Calculo de promedio de tweets RT
data_RT = Datweets[Datweets["RT"]==1]
sumdiaRT = data_RT.groupby(('dia')).RT.sum()
meanRT = round(sumdiaRT.mean())

#Calculo de promedio de tweets originales
sumdiaOri = TweORI2.groupby(('dia')).Ori.sum()
if len(sumdiaOri) == 0:
    meanOri = 0
else:
    meanOri = round(sumdiaOri.mean())

#Calculo de interacciones en tweets originales
intera = TweORI2['Interaction'] = sum(TweORI2.retweet_count, TweORI2.favorite_count)
if len(intera) == 0:
    TweMaxInter = '_No hay tweets originales_'
else:
    maxinter = max(TweORI2.Interaction)
    ordeninter = TweORI2.sort_values('Interaction', ascending = False)
    TweMaxInter = ordeninter.iloc[0,6]

#Calculo de usuarios más mencionados
usmenc = Datweets.user_mentions
usmenc.dropna(inplace=True) # Elimina los NAs
#Lista de usuarios mencionados
list_gen = []
for k in range(0,len(usmenc)):
    list_gen.append(usmenc.iloc[k])
#Cadena de usuarios mencionados
StrList = ",".join(list_gen)
StrList2 = StrList.split(',')
#Calculo de frecuencia de ususarios
frecuenciaPalab = [StrList2.count(w) for w in StrList2]
#DataFrame de usuarios con su respectiva frecuencia
juntos = pd.DataFrame()
juntos['usuario'] = StrList2
juntos['frec'] = frecuenciaPalab
#Eliminando duplicados
elidup = juntos.drop_duplicates()
ordenus = elidup.sort_values('frec', ascending = False)
    
#Calculo de Hashtags más mencionados
hashmenc = Datweets.hashtags
hashmenc.dropna(inplace=True) # Elimina los NAs
#Lista de hashtags mencionados
list_gen_hash = []
for k in range(0,len(hashmenc)):
    list_gen_hash.append(hashmenc.iloc[k])
#Cadena de usuarios mencionados
StrList_hash = ",".join(list_gen_hash)
StrList2_hash = StrList_hash.split(',')
#Calculo de frecuencia de ususarios
frecuenciaPalab_hash = [StrList2_hash.count(w) for w in StrList2_hash]
#DataFrame de usuarios con su respectiva frecuencia
juntos_hash = pd.DataFrame()
juntos_hash['hasht'] = StrList2_hash
juntos_hash['frec'] = frecuenciaPalab_hash
#Eliminando duplicados
elidup_hash = juntos_hash.drop_duplicates()
ordenhash = elidup_hash.sort_values('frec', ascending = False)

#Organizando Data Frame de Originales por Fecha
tweFecha = Datweets.sort_values(["created_at"], ascending=False)
# Seleccionando elementos
hashfech = tweFecha.hashtags
hashfech.dropna(inplace=True) # Elimina los NAs
#Lista de hashtags mencionados
list_gen_hf = []
for k in range(0,len(hashfech)):
    list_gen_hf.append(hashfech.iloc[k])
#Cadena de usuarios mencionados
StrList_hf = ",".join(list_gen_hf)
StrList2_hf = StrList_hf.split(',')
#DataFrame de Hashtags
hashfech = pd.DataFrame()
hashfech['UltHashMencion'] = StrList2_hf
#Eliminando duplicados
elidup_hf = hashfech.drop_duplicates()

#Hora de mayor interacción
fecvec = np.datetime_as_string(Datweets['created_at'])
#Asignando primer valor a listafh
listafh = [fecvec[0][11:13]]
for i in range(1, len(fecvec)):
    listafh.append(fecvec[i][11:13])
#Calculando frecuencia de horas
frecuenciahf = [listafh.count(w) for w in listafh]
#DataFrame de usuarios con su respectiva frecuencia
juntos_fh = pd.DataFrame()
juntos_fh['hour'] = listafh
juntos_fh['frec'] = frecuenciahf
#Eliminando duplicados
elidup_fh = juntos_fh.drop_duplicates()
ordenfh = elidup_fh.sort_values('frec', ascending = False)
#Completando respuesta de hora
rtahour = ordenfh.iloc[0,0]+':00.'

#%%

#Mensaje
print("\n*Informe de*: "+
      "\n*Perfil*: "+Datper['Valor'][0]+
      "\n*Usuario*: "+"https://twitter.com/"+Datper['Valor'][1]+
      "\n*Ubicación*: "+datubic+
      "\n*Biografía*: "+datbio+
      "\n*Número de seguidores*: "+format(int(Datper['Valor'][4]))+
      "\n*Promedio de Tweets diarios*: "+format(int(meanOri))+
      "\n*Promedio de Retweets diarios*: "+format(int(meanRT))+
      "\n*Promedio de Comentarios diarios*: "+format(int(meanResp))+
      "\n*Hora de más interacción*: "+ rtahour+
      "\n*Hashtags más mencionados*: "+", ".join(ordenhash.iloc[0:5,0])+
      "\n*Últimos Hashtags mencionados*: "+", ".join(elidup_hf.iloc[0:3,0])+
      "\n*Usuarios más mencionados*: "+", ".join(ordenus.iloc[0:5,0])+
      "\n*Tweet de mayor interacción*: "+TweMaxInter+
      #"\n*Interacciones del Tweet*: "+format(int(maxinter))+
      "\n*Cuenta evaluada desde*: "+str(Datweets['created_at'][len(Datweets['id'])-1])+"\n*Hasta*: "+str(Datweets['created_at'][3]))

