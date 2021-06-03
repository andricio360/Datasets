# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 15:31:34 2019

@author: DIEGO GUERRERO
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 14:18:58 2019
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

#Hashtag="@IvanDuque OR to:IvanDuque OR IvanDuque"
#Hashtag="#MasacresEnElCaucaSon"
#Hashtag="#DeQueMeHablasViejo"
#Hashtag="#DeQueMeHablasViejo"
#Hashtag="#NoApoyoElParo"
#Hashtag="#18Niños"
#Hashtag="#paro21denoviembre"
#Hashtag="(Marcha OR Movilizacion OR ('paro nacional') OR ParoNacional OR ('Paro civico nacional') OR Parociviconacional OR Protestas OR Bloqueo OR Manifestacion OR ('jornada nacional de protesta') OR Paro OR ('movilizacion pacifica') OR Planton)"
#Hashtag="#Paro21Noviembre"
#Hashtag="('Pacho AND Santos') OR #PachiCosas OR ('Francisco AND Santos')"
#Hashtag="(Militarizar OR Militarizada) OR ('allanamientos AND Bogota') OR @cartelurbano"
#Hashtag="('Gobierno AND Colombia')"
Hashtag="#4DParoNacional"

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
    for tweet in tweepy.Cursor(api.search, q=Hashtag, count=tweetsPerQry,since=fechaanterior,until=fecha,tweet_mode="extended",include_entities = True,lang="es",geocode="4.0000000,-72.0000000,450mi").items(42500):#"4.6097102,-74.081749,150km",geocode="4.0000000,-72.0000000,1500km"
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

Tweets = Tweets.drop_duplicates()

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
