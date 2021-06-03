# -*- coding: utf-8 -*-
"""
Created on Mon Feb  17 16:50:58 2020
@author: analitica
"""

from PIL import Image
from nltk.tokenize import word_tokenize
import re
from nltk.corpus import stopwords 
import numpy as np
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import pandas as pd
from wordcloud import WordCloud
import unicodedata
import sys
import random
import os
import tweepy
import datetime
#Librerias para la deteccion de anomalias
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import math
from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot
from fbprophet.diagnostics import cross_validation, performance_metrics
from fbprophet.plot import plot_cross_validation_metric

data=pd.DataFrame()

Duque_tweets_limit = [0.2587897,0.6338029]
Duque_authors_limit = [0.2002785,0.5671289]

Hashtag_tweets_limit = [0.2331656,0.3966731]
Hashtag_authors_limit = [0.1958947,0.3529763]

ULimit = 1
DLimit = 1


#Hashtag="@IvanDuque OR to:IvanDuque OR IvanDuque"
#Hashtag="@orozco_angela OR to:orozco_angela OR orozco_angela OR @Vicmunro OR to:Vicmunro OR Vicmunro"
#Hashtag="#MasacresEnElCaucaSon"
#Hashtag="#DeQueMeHablasViejo"
#Hashtag="#DeQueMeHablasViejo"
#Hashtag="#NoApoyoElParo"
#Hashtag="#18Niños"
#Hashtag="#paro21denoviembre"
#Hashtag="#RazonesParaMarchar"
#Hashtag="#21NParoNacional"
#Hashtag="#DuqueTieneMIEDO"
#Hashtag="#ConstruirNoDestruir"
#Hashtag="#AlPresidenteLePregunto"
#Hashtag="#UnaSolucionParaUberYa OR @Uber_Col OR Uber_Col OR to:Uber_Col OR UberColombia"
#Hashtag="#LaPulla OR Hassan Nassar OR @HassNassar OR to:HassNassar"
#Hashtag="#LaPulla"
#Hashtag="(Universidad Nacional OR @UNColombia)"
#Hashtag="(#AlertaFracking OR Fracking OR ('Pilotos' AND 'de' AND 'Fracking')) AND Colombia"
#Hashtag="#NoMasRCN"
#Hashtag="#UnaSolucionParaUberYa OR @Uber_Col OR Uber_Col OR UberColombia"
#Hashtag="#RevocatoriaADanielQuintero"
#Hashtag="ANIF OR Cajas de Compensacion"
#Hashtag="#ElPeorGobiernoDeLaHistoria"
#Hashtag="Catatumbo OR (Fernando AND Quintero AND Mena)"
#Hashtag="(#semifallidoes OR @NancyPatricia_G OR to:@NancyPatricia_G OR NancyPatricia_G) AND ('Acuerdo' OR 'Paz' OR 'Fallido' OR 'Semifallido')"
#Hashtag="@IvanDuque OR to:IvanDuque OR IvanDuque"
#Hashtag="@FrBarbosaD OR to:FrBarbosaD OR ('Francisco Barbosa') OR ('Fiscal' AND 'General' AND 'de' AND 'la' AND 'Nacion')"
#Hashtag="('Jhonatan' AND 'Borja') AND Candelaria"
#Hashtag="ETCR OR Ituango"
#Hashtag="@AliciaArango OR to:AliciaArango OR AliciaArango OR ('Alicia' AND 'Arango') OR Norberto OR MinTrabajo OR ('Ministra' AND 'de' AND 'Trabajo')"
#Hashtag="#ParoNacional24Feb2020"
#Hashtag="DIAN AND (Duque OR Renta OR Rentas OR IvanDuque OR Holguin OR Senadora OR Presidente)"
#Hashtag="#BodeguitaUribista"
#Hashtag="('Comandante' AND 'Condolencias') OR ('Comandante' AND 'Popeye') OR ('Ejercito' AND 'Popeye') OR ('Zapateiro' AND 'Popeye') OR @COMANDANTE_EJC OR @COL_EJERCITO"
#Hashtag="#ConfesionDeAida"
Hashtag="#DuqueComproLasElecciones"

dias=1
#dias=2

consumer_key = ['5QoxKOw8dTMWHSs7exacTV5Nv','6vHaS4hBb1zpAbLdDhfhRkEKc','p71SIVtcQrzygnLplZT06E747','5QoxKOw8dTMWHSs7exacTV5Nv','6vHaS4hBb1zpAbLdDhfhRkEKc','p71SIVtcQrzygnLplZT06E747','5QoxKOw8dTMWHSs7exacTV5Nv','6vHaS4hBb1zpAbLdDhfhRkEKc','p71SIVtcQrzygnLplZT06E747','5QoxKOw8dTMWHSs7exacTV5Nv','6vHaS4hBb1zpAbLdDhfhRkEKc','p71SIVtcQrzygnLplZT06E747']
consumer_secret =['5fIucoM36WxgJ3XfDx1FfhNoYZVfyUzy7Bn14oxlS6KjAI35Jq','voPnvROC9U8sRvpKwuWSh50OxdQ2n594l4lKUG0QxbUjKBH4oV','esMof5wr3bpIS4PpRKKQ2VDV5svtNa9ZDkY1K3wVjFp8WX1iRz','5fIucoM36WxgJ3XfDx1FfhNoYZVfyUzy7Bn14oxlS6KjAI35Jq','voPnvROC9U8sRvpKwuWSh50OxdQ2n594l4lKUG0QxbUjKBH4oV','esMof5wr3bpIS4PpRKKQ2VDV5svtNa9ZDkY1K3wVjFp8WX1iRz','5fIucoM36WxgJ3XfDx1FfhNoYZVfyUzy7Bn14oxlS6KjAI35Jq','voPnvROC9U8sRvpKwuWSh50OxdQ2n594l4lKUG0QxbUjKBH4oV','esMof5wr3bpIS4PpRKKQ2VDV5svtNa9ZDkY1K3wVjFp8WX1iRz','5fIucoM36WxgJ3XfDx1FfhNoYZVfyUzy7Bn14oxlS6KjAI35Jq','voPnvROC9U8sRvpKwuWSh50OxdQ2n594l4lKUG0QxbUjKBH4oV','esMof5wr3bpIS4PpRKKQ2VDV5svtNa9ZDkY1K3wVjFp8WX1iRz']
access_token = ['1170030344495665159-xjAvLayFyiWBRGmUuSa1O4VJIXtlIJ','1061012155535945728-tA7qrTSeW8lG84rgjzb5bAMPNI0r5D','343814502-xCL24DSjHIR3nsql6F2YJgGXt0Sh7A6kpIDyJXSx','1170030344495665159-xjAvLayFyiWBRGmUuSa1O4VJIXtlIJ','1061012155535945728-tA7qrTSeW8lG84rgjzb5bAMPNI0r5D','343814502-xCL24DSjHIR3nsql6F2YJgGXt0Sh7A6kpIDyJXSx','1170030344495665159-xjAvLayFyiWBRGmUuSa1O4VJIXtlIJ','1061012155535945728-tA7qrTSeW8lG84rgjzb5bAMPNI0r5D','343814502-xCL24DSjHIR3nsql6F2YJgGXt0Sh7A6kpIDyJXSx','1170030344495665159-xjAvLayFyiWBRGmUuSa1O4VJIXtlIJ','1061012155535945728-tA7qrTSeW8lG84rgjzb5bAMPNI0r5D','343814502-xCL24DSjHIR3nsql6F2YJgGXt0Sh7A6kpIDyJXSx']
access_token_secret = ['R2Tgqxr2kMr43a6HB5tJtWBWY55kFqQxYZaqCuSpIhdPc','P77agZo2Ngbuk9wD4F0w0ILzw5PHxlmS2ruzclVXpbv7J','E9tIbrazuHNt0NBjXQjEEzf4pimuGo5dRXvFk83Lqterv','R2Tgqxr2kMr43a6HB5tJtWBWY55kFqQxYZaqCuSpIhdPc','P77agZo2Ngbuk9wD4F0w0ILzw5PHxlmS2ruzclVXpbv7J','E9tIbrazuHNt0NBjXQjEEzf4pimuGo5dRXvFk83Lqterv','R2Tgqxr2kMr43a6HB5tJtWBWY55kFqQxYZaqCuSpIhdPc','P77agZo2Ngbuk9wD4F0w0ILzw5PHxlmS2ruzclVXpbv7J','E9tIbrazuHNt0NBjXQjEEzf4pimuGo5dRXvFk83Lqterv','R2Tgqxr2kMr43a6HB5tJtWBWY55kFqQxYZaqCuSpIhdPc','P77agZo2Ngbuk9wD4F0w0ILzw5PHxlmS2ruzclVXpbv7J','E9tIbrazuHNt0NBjXQjEEzf4pimuGo5dRXvFk83Lqterv']


#Hashtag= "LaNuevaGuerrilla OR FARC OR Timochenko OR VuelvenALasArmas OR UribeHizoTrizasLaPaz"
#Hashtag= "(#PactoPorLosBosques OR #MedellínVamosPorBuenCamino) AND ('@IvanDuque OR to:IvanDuque OR IvanDuque')"
#Hashtag= "#AlertaFracking"
#Hashtag= "#NOalFracking"
#Hashtag= "#DuqueSeRajaEn"
#Hashtag="#MovilizaciónContraUribe OR #UribeMalditoSeas OR #Uribetienepanico OR #UribeLaCarcelTeEspera"
#Hashtag="#DeUribePienso"
#Hashtag= "#UribeHoraCero"
#Hashtag= "EstamosConUribe"
#Hashtag= "('Uribe') AND ('gobierno') AND ('@IvanDuque OR to:IvanDuque OR IvanDuque OR duque')"
#Hashtag= "(#marchaestudiantil OR #cumplimosconlaeducación OR #marchasenlacity OR #octubre10porlaeducación OR #estudienvagos)"
#Hashtag= "#DuqueRenuncie"
#Hashtag= "#17Octubre"


#consumer_key = ['6vHaS4hBb1zpAbLdDhfhRkEKc','p71SIVtcQrzygnLplZT06E747','OrHa233toI2RSnlVLzeRGC4BQ','6vHaS4hBb1zpAbLdDhfhRkEKc','p71SIVtcQrzygnLplZT06E747','OrHa233toI2RSnlVLzeRGC4BQ']
#consumer_secret =['voPnvROC9U8sRvpKwuWSh50OxdQ2n594l4lKUG0QxbUjKBH4oV','esMof5wr3bpIS4PpRKKQ2VDV5svtNa9ZDkY1K3wVjFp8WX1iRz','S0onXeRRN77EmeOh6I457OqCn5F4v60FshuQV4Go4Rlrzdrdi8','voPnvROC9U8sRvpKwuWSh50OxdQ2n594l4lKUG0QxbUjKBH4oV','esMof5wr3bpIS4PpRKKQ2VDV5svtNa9ZDkY1K3wVjFp8WX1iRz','S0onXeRRN77EmeOh6I457OqCn5F4v60FshuQV4Go4Rlrzdrdi8']
#access_token = ['1061012155535945728-tA7qrTSeW8lG84rgjzb5bAMPNI0r5D','343814502-xCL24DSjHIR3nsql6F2YJgGXt0Sh7A6kpIDyJXSx','905797484047454208-2tftfvl7jvlSjeW8LyHkoBqNig4gGgc','1061012155535945728-tA7qrTSeW8lG84rgjzb5bAMPNI0r5D','343814502-xCL24DSjHIR3nsql6F2YJgGXt0Sh7A6kpIDyJXSx','905797484047454208-2tftfvl7jvlSjeW8LyHkoBqNig4gGgc']
#access_token_secret = ['P77agZo2Ngbuk9wD4F0w0ILzw5PHxlmS2ruzclVXpbv7J','E9tIbrazuHNt0NBjXQjEEzf4pimuGo5dRXvFk83Lqterv','DrqAILagIwqKjvHnkbZCYvJ7XUKNBgUIvXJ2c2Cnk25sV','P77agZo2Ngbuk9wD4F0w0ILzw5PHxlmS2ruzclVXpbv7J','E9tIbrazuHNt0NBjXQjEEzf4pimuGo5dRXvFk83Lqterv','DrqAILagIwqKjvHnkbZCYvJ7XUKNBgUIvXJ2c2Cnk25sV']

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


fecha = datetime.datetime.utcnow()+datetime.timedelta(days=1)

for i in range(0,dias): 
    auth = tweepy.AppAuthHandler(consumer_key[i], consumer_secret[i])
    api = tweepy.API(auth)
    if (not api):
        print ("Can't Authenticate")
        sys.exit(-1)
        
    results_Duque_RT = []
    counter = 1
    tweetsPerQry = 100
    fechaanterior=fecha-datetime.timedelta(days=1)
    fecha=fecha.strftime('%Y-%m-%d')
    fechaanterior=fechaanterior.strftime('%Y-%m-%d')
    for tweet in tweepy.Cursor(api.search, q=Hashtag, count=tweetsPerQry,since=fechaanterior,until=fecha,tweet_mode="extended",include_entities = True,lang="es").items(42500):#"4.6097102,-74.081749,150km",geocode="4.0000000,-72.0000000,1500km"
        results_Duque_RT.append(tweet)
        counter+=1
        print(str(counter))
    print('Total Tweets so far %s' %(str(len(results_Duque_RT))))
    fecha=datetime.datetime.strptime(fecha,'%Y-%m-%d')
    fecha = fecha - datetime.timedelta(days=1)
    results = results_Duque_RT
    id_list = [str(tweet.id) for tweet in results]
    data_set = pd.DataFrame(id_list,columns=["id"])
    data_set["text"] = [tweet.full_text for tweet in results]
    data_set["created_at"] = [tweet.created_at for tweet in results]
    data_set["created_at"] = pd.to_datetime(data_set["created_at"])-pd.Timedelta('5 hours')
    data_set["date"]=data_set.created_at.map(lambda x: x.strftime('%Y-%m-%d'))
    data_set["hour"]=data_set["created_at"].map(lambda x: x.strftime("%H"))
    data_set["retweet_count"] = [tweet.retweet_count for tweet in results]
    data_set["favorite_count"] = [tweet.favorite_count for tweet in results]
    data_set["user_screen_name"] = [tweet.author.screen_name for tweet in results]
    data_set["user_name"] = [tweet.author.name for tweet in results]
    data_set["profile_image"]= [tweet.author.profile_image_url for tweet in results]
    data_set["user_created_at"] = [tweet.author.created_at for tweet in results]
    data_set["profile_image"]= [tweet.author.profile_image_url for tweet in results]
    data_set["user_followers_count"] = [tweet.author.followers_count for tweet in results]
    data_set['Interacciones']=data_set['retweet_count']+data_set['favorite_count']
    data_set['link']=['https://www.twitter.com/'+row['user_screen_name']+'/status/'+str(row['id']) for idx,row in data_set.iterrows()]
    data_set['followers'] = [tweet.author.followers_count for tweet in results]
    
    rts_ = []
    
    for tweet in results:
        try:
            rts_.append(tweet.retweeted_status.full_text)
        except:
            rts_.append('')
    
    data_set["Retweeted_tweet"] = rts_
    
    rts_author = []
    rts_profile=[]
    
    for tweet in results:
        try:
            rts_author.append(tweet.retweeted_status.user.screen_name)
            rts_profile.append(tweet.author.profile_image_url)
    
        except:
            rts_author.append('')
            rts_profile.append('')
    
    data_set["Retweeted_tweet_author"] = rts_author
    data_set["profile_image_rt"]= rts_profile
    data=pd.concat([data_set,data],ignore_index=True)    
    fechas=data["date"].unique()
    data = data.drop_duplicates()
    hoy = datetime.datetime.utcnow()
    ayer=hoy-datetime.timedelta(days=1)
    hoy=hoy.strftime('%Y-%m-%d')
    ayer=ayer.strftime('%Y-%m-%d')
    if(dias==1):
        data=data.loc[data['date']==hoy]
    if(dias==2):
        data=pd.concat([data.loc[data['date']==hoy],data.loc[data['date']==ayer]],ignore_index=True)
                
############################### CONEXIONES RED ##############################
#%%
       
data_set=data  
fechas=data_set["date"].unique()
cons=pd.DataFrame()
conshash=pd.DataFrame()
consMen=pd.DataFrame()
    
for j in range(0,len(fechas)):
    data_set_duque = data_set[data_set.date==fechas[j]]
    texto_plain = ''
    
    for i in range(0,len(data_set_duque['text'].values)):
        texto_plain +=' '+ data_set_duque['text'].values[i]

    texto_plain_ = texto_plain.lower()
    texto_plain_ = clean_text(texto_plain_)
    stopwrds=[]
    Menciones = re.findall(r" @(\w+) ", texto_plain)
    word_me=set(Menciones)
    word_me=list(word_me)
    texto_plain_Menciones = ''
    for i in range(0,len(word_me)):
        texto_plain_Menciones +=' '+ Menciones[i]
    texto_plain_Menciones=texto_plain_Menciones.lower()
    wordmen = texto_plain_Menciones.split()
    wordmenfreq = [wordmen.count(w) for w in wordmen]
    dat2=[]
    for n in range(0,len(wordmen)):
        dat2.append(fechas[j])
    Men=pd.DataFrame(data={'Mencion':wordmen,'Frq':wordmenfreq,'Date':dat2})
    Men=Men.drop_duplicates()
    consMen=pd.concat([consMen,Men],ignore_index=True)
    Personas = consMen.groupby(by=['Mencion']).agg({'Frq':'sum', 'Mencion':'first'}).sort_values(by='Frq',ascending=False)
    Personas=pd.DataFrame(Personas[0:100])
    Personas=Personas.sort_values(by='Frq')

    venezuela=['vz','venezuela','venezolanos','venezolano','maduro','nicolasmaduro','pueblo hermano']
    uribe=['uribistas','uribe','alvarouribe','uribista']
    texto_plain_clean=texto_plain_
    for word in venezuela:
        texto_plain_clean = re.sub(word,'venezuela',texto_plain_clean)
    for word in uribe:
        texto_plain_clean = re.sub(word,'uribismo',texto_plain_clean)    
    words_=['ja','spamdeperritos','duque','presidente','colombia','gobierno','bien','solo','ser',
    'hacer','hace', 'pais', 'debe','nene','pdte', 'abra','solicito','ivan','señor','invito','dice','usted','puede','senor',
    'casa','toda','dijo','colombianos','ejemplo','sera','republica','estan','hablemos','tambien','mesa','reconocen','orden',
    'adelantamos','seguir','anos','todas','bueno','palabras','forma','vida','gran','claro','decir','doble','parece','hora',
    'meses','pasando','ultima','menos','colombiano','colombianos','doble','general','alcan','peso','presento','pueblo','vamos','ustedes','pasa','respeto','mismo','mientras','mejor','gracias','gente']
    
    for s in range(len(words_)):
        stopwrds.append(words_[s].lower())
    for s in range(len(word_me)):
       stopwrds.append(word_me[s].lower())    
    for word in stopwrds:
        texto_plain_clean = re.sub(" "+word+" ",' ',texto_plain_clean)

    texto_plain_clean = re.sub(" rt ",' ',texto_plain_clean)
    texto_plain_clean=texto_plain_clean.strip()
    texto_plain_clean=" ".join(texto_plain_clean.split())
    tokens = word_tokenize(texto_plain_clean)
    texto_comments = nltk.Text(tokens)
    fdist1 = nltk.FreqDist(texto_comments)
    
    dict_filter = lambda fdist1, stopwords: dict( (word,fdist1[word]) for word in fdist1 if word not in stopwords)
    STPWORDS = stopwords.words('spanish')
    STPWORDS_customed = STPWORDS
    for s in range(len(words_)):
       STPWORDS_customed.append(words_[s].lower())
    for s in range(len(word_me)):
       STPWORDS_customed.append(word_me[s].lower())
       
    filtered_fdist1 = nltk.probability.FreqDist(dict_filter(fdist1, STPWORDS_customed))
    
    Wrds = []
    Frq = []
    dat=[]
    for word, frequency in filtered_fdist1.most_common(500):
        if len(word)>=4:
            Wrds.append(word)
            Frq.append(frequency)
            dat.append(fechas[j])
    
    new=pd.DataFrame(data={'Wrds':Wrds,'Frq':Frq,'Date':dat})
    cons=pd.concat([cons,new],ignore_index=True)
    Palabras = cons.groupby(by=['Wrds']).agg({'Frq':'sum', 'Wrds':'first'}).sort_values(by='Frq',ascending=False)
    Palabras=pd.DataFrame(Palabras[0:100])
    Palabras=Palabras.sort_values(by='Frq')
    
    Hashstags = re.findall(r"#(\w+)", texto_plain)
    texto_plain_Hashstags = ''
    for i in range(0,len(Hashstags)):
        texto_plain_Hashstags +=' '+ Hashstags[i]
    texto_plain_Hashstags=texto_plain_Hashstags.lower()
    wordhash = texto_plain_Hashstags.split()
    wordhashfreq = [wordhash.count(w) for w in wordhash]
    dat1=[]
    for n in range(0,len(wordhash)):
        dat1.append(fechas[j])
    Hash=pd.DataFrame(data={'Hashtag':wordhash,'Frq':wordhashfreq,'Date':dat1})
    Hash=Hash.drop_duplicates()
    conshash=pd.concat([conshash,Hash],ignore_index=True)
    Tendencias = conshash.groupby(by=['Hashtag']).agg({'Frq':'sum', 'Hashtag':'first'}).sort_values(by='Frq',ascending=False)
    Tendencias=pd.DataFrame(Tendencias[0:100])
    Tendencias=Tendencias.sort_values(by='Frq')
    
a=data_set[["text","id","date"]]
Mencion=[]
IdMencion=[]
FechaIdMencion=[]
Hash=[]
IdHash=[]
FechaIdHash=[]
Sentimiento=[]
Confidence=[]

for j in range(len(Personas['Mencion'])):
    for i in range(len(a)):
        BB="@"+Personas['Mencion'][j]+" "
        if len(BB)>=5:
            if BB in a["text"].values[i].lower():
                Mencion.append(Personas['Mencion'][j])
                IdMencion.append(a["id"].values[i])
                FechaIdMencion.append(a["date"].values[i])
            
        if Personas['Mencion'][j] in a["text"].values[i].lower():
            Mencion.append(Personas['Mencion'][j])
            IdMencion.append(a["id"].values[i])
            FechaIdMencion.append(a["date"].values[i])


Menciones_=pd.DataFrame(Mencion,IdMencion)
Menciones_["Fecha"]=FechaIdMencion
Menciones_.columns = ['Mencion', 'Fecha']
 
for j in range(len(Tendencias['Hashtag'])):
    for i in range(len(a["text"])):
        AA="#"+Tendencias['Hashtag'][j]+" "
        if AA in a["text"].values[i].lower():
            Hash.append(Tendencias['Hashtag'][j])
            IdHash.append(a["id"].values[i])
            FechaIdHash.append(a["date"].values[i])
 
HashTags_=pd.DataFrame(Hash,IdHash)
HashTags_["Fecha"]=FechaIdHash
HashTags_.columns = ['Hashtag', 'Fecha']
          
Tema=[]
IdTema=[]
FechaIdTema=[]

for i in range(len(a["text"])):
    for word in uribe:
        a["text"].values[i] = re.sub(word,'uribismo',a["text"].values[i].lower())
for i in range(len(a["text"])):        
    for word in venezuela:
        a["text"].values[i] = re.sub(word,'venezuela',a["text"].values[i].lower()) 
        
for j in range(len(Palabras['Wrds'])):
    for i in range(len(a["text"])):
        AA=Palabras['Wrds'][j]+" "
        if AA in a["text"].values[i].lower():
           Tema.append(Palabras['Wrds'][j])
           IdTema.append(a["id"].values[i])
           FechaIdTema.append(a["date"].values[i])        

Temas_=pd.DataFrame(Tema,IdTema)
Temas_["Fecha"]=FechaIdTema
Temas_.columns = ['Tema', 'Fecha']      
           
         
Tweets=pd.DataFrame()
Tweets["Id"]=data_set['id']
Tweets["Tweet"]=data_set['text']
Tweets["Fecha"]=data_set['date']
Tweets["Hora"]=data_set['hour']
Tweets["Creado_a"]=data_set['created_at']
Tweets["Autor"]=data_set['user_screen_name']
Tweets["Profile_image"]=data_set['profile_image']
Tweets["Interacciones"]=data_set['Interacciones']
Tweets["Retweet_count"]=data_set['retweet_count']
Tweets["Retweeted_tweet"]=data_set['Retweeted_tweet']
Tweets['Seguidores'] = data_set['followers']
Tweets['Link'] = data_set['link']

Tweets = Tweets.drop_duplicates()


Temas_.to_excel('MencionesDiarias/DuqueDiarioConsolidado' + '.xlsx', sheet_name='ConsolidadoMenciones')
Menciones_.to_excel('MencionesDiarias/DuqueDiarioMenciones' + '.xlsx', sheet_name='Menciones')  
HashTags_.to_excel('MencionesDiarias/DuqueDiarioHashtag' + '.xlsx', sheet_name='Hashtags')    
Tweets.to_excel('MencionesDiarias/DuqueDiariodata'+'.xlsx', sheet_name='Tweets')

#########################################Detectar Comportamiento Atipico##############################################
#Funcion para aproximar una Etiqueta de Tiempo al minuto superior con base en los segundos
def ceil_dt(dt):
    # how many secs have passed this hour
    nsecs = dt.minute*60 + dt.second
    # number of seconds to next quarter hour mark
    # Non-analytic (brute force is fun) way:  
    #   delta = next(x for x in xrange(0,3601,900) if x>=nsecs) - nsecs
    # analytic way:
    delta = math.ceil(nsecs / 60) * 60 - nsecs
    #time + number of seconds to quarter hour mark.
    return dt + datetime.timedelta(seconds=delta)

#Aplicar la funcion ceil_dt a una columna entera
Tweets['Fecha_hora_ajustada']=Tweets['Creado_a'].apply(lambda x: ceil_dt(x))

#Agrupar por fecha y contar el numero de Tweets por cada etiqueta de tiempo
time_series=Tweets.groupby('Fecha_hora_ajustada').Id.nunique()
#Pasar una serie de datos a dataframe
time_series=time_series.to_frame()
#Poner los indices como una columna y dejar los indices desde 0
time_series.reset_index(level=0, inplace=True)

#Ver estadisticas generales del dataframe
time_series.describe()

#Change colnames of a dataframe
time_series.columns=['ds','y']

#######Deteccion de Anomalias
m = Prophet(daily_seasonality=True, yearly_seasonality=False, weekly_seasonality=False,
            seasonality_mode='multiplicative', interval_width=0.99)

m = m.fit(time_series)
forecast = m.predict(time_series)
forecast['fact'] = time_series['y'].reset_index(drop = True)

m.plot(forecast, xlabel='Fecha', ylabel='Tweets', uncertainty=True, plot_cap=True)
plt.show()

fig = m.plot(forecast)
a = add_changepoints_to_plot(fig.gca(), m, forecast)

#____________________________________________________________________________________________
#%%
Tweets=data
#Hashtag_file =('IvanDuque'+hoy)
Hashtag_file =('DuqueComproLasElecciones_2_'+hoy)
path = Hashtag_file

try:
    os.mkdir(path)
except OSError:  
    print ("Creation of the directory %s failed" % path)
else:  
    print ("Successfully created the directory %s " % path)

wcloud(texto_plain_clean,Hashtag_file)
fechas=Tweets["date"].unique()
fechas=sorted(fechas)

Tweets1 = Tweets.text.drop_duplicates().copy()
Tweets2 = pd.DataFrame(data={'text':Tweets1})
Tweets2['Sentiment']='-'

Tweets2.text.iloc[0]

import re
texto_plain = ''
    
for i in range(0,len(Tweets2['text'].values)):
    texto_plain +=' '+ str(Tweets2['text'].values[i])

Hashtag = Hashtag_file

data_1 = Tweets.copy()
    
data_1 = data_1[pd.notnull(data_1['text'])]
data_1['id'] = [str(row.id) for idx,row in data_1.iterrows()]
data = data_1.copy()
data_all = data.copy()
data_all['RT']=['RT' if 'RT @' in str(x)[:] else 'ORIGINAL' for x in data_all.text]
rt_count= sum(data_all.RT == 'RT')
data_RT = data_all.groupby(by=['text','user_screen_name','created_at']).agg({'created_at':'first',
                                                                             'retweet_count':'count',
                                                                             'favorite_count':'count',
                                                                             'profile_image':'first',
                                                                             'profile_image_rt':'first',
                                                                             'user_screen_name':'first',
                                                                             'Retweeted_tweet_author':'first'}).sort_values(by='retweet_count')
data_RT['RT']=['RT' if 'RT' in str(x)[:2] else 'ORIGINAL' for x in data_RT.index.get_level_values(0)]
Connection_powerbi=data_RT.loc[data_RT['RT']=='RT']
Original = data_RT['RT'][data_RT['RT']=='ORIGINAL'].index.values
RT = data_RT['RT'][data_RT['RT']=='RT'].index.values

import datetime

now_time = datetime.datetime.now()
now_time = now_time.strftime("%d_%m_%Y")

import re
connections_to = []
connections_from = []
timestamp_ = []
timestamp_end = []

for RTs in RT:
    connections_to.append(RTs[1])
    timestamp_.append(RTs[2].isoformat())
    timestamp_end.append(datetime.datetime.now().isoformat())
    try:
        user = re.findall(r"@(\w+)", RTs[0])[0]
        connections_from.append(user)
    except:
        try:        
            user = re.findall(r"RT (\w+)", RTs[0])[0]
            connections_from.append(user)
        except:
            print('Unidentified user')
            connections_from.append('IvanDuque')

Connection = pd.DataFrame(data={'Target':connections_to,
                                'Source':connections_from,
                                'timeset':timestamp_
                                })

Connection_powerbi =pd.DataFrame(data={
                                'Target':Connection_powerbi['user_screen_name'],
                                'profile_target':Connection_powerbi['profile_image'],
                                'Source':Connection_powerbi['Retweeted_tweet_author'],
                                'profile_source':Connection_powerbi['profile_image_rt'],
                                'timeset':Connection_powerbi['created_at']
                                })   
    
sources__ = list(set(connections_from))   

Tweets.to_excel(Hashtag_file+'/Tweets'+Hashtag+'.xlsx')    
Connection.to_excel(Hashtag_file+'/connections'+Hashtag+'.xlsx')
#Connection_powerbi.to_excel('MencionesDiarias/connectionsPowerBi'+Hashtag+'.xlsx')
  

data_all['Interacciones']=1+data_all['retweet_count']+data_all['favorite_count']*0.5

data_all_1 = data_all[data_all['RT']=="ORIGINAL"].copy()
data_all_1.sort_values(by='Interacciones',ascending=False,inplace=True)


data_all_1['Interacciones_acumuladas']=data_all_1['Interacciones'].cumsum()
data_all_1['Interacciones_acumuladas_per']=data_all_1['Interacciones_acumuladas']/data_all_1['Interacciones'].sum()*100

data_all_1 = data_all_1.reset_index(drop=True)

data_all_1['tweets_per']=(data_all_1.index+1)/len(data_all_1.index.values)*100

from scipy.interpolate import interp1d

x = data_all_1['tweets_per'].values
y = data_all_1['Interacciones_acumuladas_per'].values

f2 = interp1d(x, y, kind='cubic')

ynew = 90
ynew_1 = 95
ynew_2 = 99

def value_root(ynew,x_try,fun):
    y_0 = x_try
    x_try_1 = x_try
    x = lambda ynew,fun,y_0: (ynew-fun(y_0))**2
    error_tol = x(ynew,fun,y_0) 
    while error_tol > 1e-6:
        der_err = (x(ynew,fun,y_0+1e-6)-x(ynew,fun,y_0) )/1e-6
        y_1 = y_0 - error_tol/(der_err)
        try:
            error_tol = (ynew-fun(y_1))**2
        except:
            x_try_1 = x_try_1/2
            y_1 = x_try_1
            error_tol = (ynew-fun(y_1))**2
        y_0 = y_1
    return y_0

conver_per = value_root(ynew,x.mean(),f2)
conver_per_1 = value_root(ynew_1,x.mean(),f2)
conver_per_2 = value_root(ynew_2,x.mean(),f2)


data_all_1['link']=['https://www.twitter.com/'+row['user_screen_name']+'/status/'+str(row['id']) for idx,row in data_all_1.iterrows()]

data_all_1.to_excel(Hashtag_file+'/'+Hashtag+'Top10_'+'.xlsx')

Original_tweets = data_all_1.sort_values(by='Interacciones',ascending=False)

Autores_top_tweets = Original_tweets.groupby(by=['user_screen_name','text','created_at','id']).agg({'user_screen_name':'first',
                                                                                  'text':'last',
                                                                                  'id':'last',
                                                                                  'created_at':'last',
                                                                                  'retweet_count':'sum',
                                                                                  'favorite_count':'sum',
                                                                                  'Interacciones':'sum',
                                                                                  'user_followers_count':'mean'})    

Autores_top = Original_tweets.groupby(by=['user_screen_name']).agg({'text':'count',
                                                                    'retweet_count':'sum',
                                                                    'favorite_count':'sum',
                                                                    'Interacciones':'sum',
                                                                    'user_followers_count':'mean',
                                                                    'id':'first'})

Autores_top['user_screen_name']=Autores_top.index
    
Autores_top['Interacciones_']=1+Autores_top['retweet_count']+Autores_top['favorite_count']*0.5

Autores_top['Interacciones_tweet']=Autores_top['Interacciones_']/Autores_top['text']

Autores_top['per_engagement']=Autores_top['Interacciones_tweet']/Autores_top['user_followers_count']*100

Autores_top.sort_values(by='Interacciones_',ascending=False,inplace=True)

Autores_top['Interacciones_acumuladas']=Autores_top['Interacciones'].cumsum()
Autores_top['Interacciones_acumuladas_per']=Autores_top['Interacciones_acumuladas']/Autores_top['Interacciones'].sum()*100

Autores_top = Autores_top.reset_index(drop=True)

Autores_top['authors_per']=(Autores_top.index+1)/len(Autores_top.index.values)*100
Autores_top.to_excel('MencionesDiarias/usuariosUnicos'+'.xlsx', sheet_name='usuarios')

x = Autores_top['authors_per'].values
y = Autores_top['Interacciones_acumuladas_per'].values

f2 = interp1d(x, y, kind='cubic')

conver_per_author = value_root(ynew,90,f2)
conver_per_author_1 = value_root(ynew_1,90,f2)
conver_per_author_2 = value_root(ynew_2,90,f2)

from time import gmtime, strftime, localtime,strptime
fecha = strftime("%Y-%m-%d %I:%M:%S %p", localtime())

import locale
locale.setlocale(locale.LC_ALL, '')

n=len(fechas)-1
#print("\n*Análisis de '"+Hashtag_file+"'* \n*Fecha y Hora de análisis*: "+str(fecha)+"\n*Periodo de tiempo de análisis*: de "+str(fechas[0])+" a "+str(fechas[n])+" \n*Tweets Originales*: {:,} \n*Autores únicos*: {:,}\n*RTs*: {:,}\n*Favoritos*: {:,}\n*Alcance Potencial*: {:,}\n".format(int(len(data_all_1['tweets_per'])),int(len(Autores_top['authors_per'])),int(data_all_1['retweet_count'].sum()),int(data_all_1['favorite_count'].sum()),Autores_top['user_followers_count'].sum()).replace(',','.'))
#print("\n*Análisis de '"+Hashtag_file+"'* \n*Fecha y Hora de análisis*: "+str(fecha)+"\n*Periodo de tiempo de análisis*: de "+str(fechas[0])+" a "+str(fechas[n])+" \n*Tweets Originales*: {:,} \n*Autores únicos*: {:,}\n*RTs*: {:,}\n*Favoritos*: {:,}\n*Menciones Totales*:{:,}\n".format(int(len(data_all_1['tweets_per'])),int(len(Autores_top['authors_per'])),int(rt_count),int(data_all_1['favorite_count'].sum()),int(rt_count+int(len(data_all_1['tweets_per'])))).replace(',','.'))
print("\n*Análisis de '"+Hashtag_file+"'* \n*Fecha y Hora de análisis*: "+str(fecha)+" \n*Tweets Originales*: {:,} \n*Autores únicos*: {:,}\n*RTs*: {:,}\n*Favoritos*: {:,}\n*Menciones Totales*:{:,}\n".format(int(len(data_all_1['tweets_per'])),int(len(Autores_top['authors_per'])),int(rt_count),int(data_all_1['favorite_count'].sum()),int(rt_count+int(len(data_all_1['tweets_per'])))).replace(',','.'))

print('*%.0f* (*%.0f%%*) Tweets publicados por *%.0f* autores únicos (*%.0f%%*) generaron el *%.0f%%* de las interacciones respecto al tema de análisis.\n'%(conver_per/100*len(data_all_1['tweets_per']),conver_per,conver_per_author/100*len(Autores_top['authors_per']),conver_per_author,ynew))
#print('El *%.0f%%* de las interacciones en Twitter corresponden al *%.0f%%* (*%.0f*) de Tweets generados por el *%.0f%%* (*%.0f*) de autores únicos \n'%(ynew,conver_per,conver_per/100*len(data_all_1['tweets_per']),conver_per_author,conver_per_author/100*len(Autores_top['authors_per'])))

def percentageEv(per_auth,per_tweets,auth_range,tweet_range):
    tweet_normal = ''
    author_normal = ''
    if per_auth > auth_range[0] and per_auth < auth_range[1] :
        author_normal = 'Normal'
    else:
        author_normal = 'Mayor' if per_auth > auth_range[1] else 'Menor'
        
    if per_tweets > tweet_range[0] and per_tweets < tweet_range[1]:
        tweet_normal = 'Normal'
    else:
        tweet_normal = 'Mayor' if per_tweets > tweet_range[1] else 'Menor'
        
    return tweet_normal,author_normal
        
   

if 'IvanDuque' in Hashtag_file:
    t_normal, a_normal = percentageEv(conver_per_author/100,conver_per/100,Duque_authors_limit,Duque_tweets_limit)
    print('El porcentaje de Tweets es: ' + t_normal + ' y el porcentaje de autores es: ' + a_normal)
else:
    t_normal2, a_normal2 = percentageEv(conver_per_author/100,conver_per/100,Hashtag_authors_limit,Hashtag_tweets_limit)
    print('El porcentaje de Tweets es: ' + t_normal2 + ' y el porcentaje de autores es: ' + a_normal2)
        
Autores_top.to_excel(Hashtag_file+'/'+Hashtag+'Top10Authors_'+'.xlsx')

Best_Tweet = data_all_1.sort_values(by='Interacciones',ascending=False).head(1).copy()

fecha_best_tweet = pd.to_datetime(str(Best_Tweet['created_at'].values[0])).strftime("%Y-%m-%d %I:%M:%S %p")

#print('\n*Tweet con mayor interacción*\n\n{}\n\n*Fecha:* {}\n*Autor:* {}\n*Retweets:* {:,}\n*Favoritos:* {:,}\n*Seguidores:* {:,}\n*Link del Tweet:* {}'.format(Best_Tweet['text'].values[0],
#      fecha_best_tweet,
#      Best_Tweet['user_screen_name'].values[0],
#      int(Best_Tweet['retweet_count'].values[0]),
#      int(Best_Tweet['favorite_count'].values[0]),
#      int(Best_Tweet['user_followers_count'].values[0]),
#      Best_Tweet['link'].values[0]).replace(',','.'))