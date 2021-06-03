# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 08:56:54 2020

@author: Analitica
"""

#Importar las Librerias
import pandas as pd
import unicodedata
import re
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from nltk.corpus import stopwords
from collections import OrderedDict

#Cargar el archivo csv plano
data_inicial=pd.read_csv('interacciones_11_04_2020.csv')
#Crear una copia para trabajar los datos
df1=data_inicial.copy()

#Limpieza de datos
#Quitar los acentos
def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

# function for text cleaning 
def clean_text(text):
    # remove backslash-apostrophe 
    text = re.sub("\'", "", text) 
    # remove everything except alphabets 
    text = re.sub("[^a-zA-Z]"," ",text) 
    # remove whitespaces 
    text = ' '.join(text.split()) 
    # convert text to lowercase 
    text = text.lower() 
    return text

#Cambiar los nan por una celda de texto vacia
df1 = df1.replace(np.nan, '', regex=True)
#Se aplica la funcion de quitar acentos a los argumentos de las observaciones (ObservacionesCreacion) utilizando el apply-lambda duo
df1['clean_Obs'] = df1['ObservacionesCreacion'].apply(lambda x: strip_accents(x))
#Se aplica la funcion de limpieza a los argumentos de las observaciones (ObservacionesCreacion) utilizando el apply-lambda duo
df1['clean_Obs'] = df1['clean_Obs'].apply(lambda x: clean_text(x))

##############Ver la frecuencia de palabras es opcional, no es fundamental para sacar el wordcloud##########################################
#Sacar las palabras y la frecuencia de un conjunto de documentos
def freq_words(x, terms = 30): 
  all_words = ' '.join([text for text in x]) 
  all_words = all_words.split() 
  fdist = nltk.FreqDist(all_words) 
  words_df = pd.DataFrame({'word':list(fdist.keys()), 'count':list(fdist.values())}) 
  
  # selecting top 20 most frequent words 
  d = words_df.nlargest(columns="count", n = terms)
  d=pd.DataFrame(d)
  
  # visualize words and frequencies
  plt.figure(figsize=(12,15)) 
  ax = sns.barplot(data=d, x= "count", y = "word") 
  ax.set(ylabel = 'Word') 
  plt.show()
  return d
  
# Imprimir las 100 palabras mas frecuentes 
freq_words(df1['clean_Obs'], 100)
##############Aca finaliza la parte de la frecuencia que es opcional, el resto si es obligatorio correrlo##########################################

#Cargar las stopwords que por default tiene la libreria
stop_words = stopwords.words('spanish')

#Terminos adicionales que no estan en la lista inicial de stopwords pero se desean agregar al diccionario
words_=['ja','spamdeperritos','duque','presidente','colombia','gobierno','bien','solo','ser',
    'hacer','hace', 'pais', 'debe','nene','pdte', 'abra','solicito','ivan','señor','invito','dice','usted','puede','senor',
    'casa','toda','dijo','colombianos','ejemplo','sera','republica','estan','hablemos','tambien','mesa','reconocen','orden',
    'adelantamos','seguir','anos','todas','bueno','palabras','forma','vida','gran','claro','decir','doble','parece','hora',
    'meses','pasando','ultima','menos','colombiano','colombianos','doble','alcan','peso','presento','pueblo','vamos',
    'ustedes','pasa','respeto','mismo','mientras','mejor','gracias','gente','rt','com','twitter','si','q','hoy','d','s','ly','bit'
    'co','van','va','col','segun','aqui','t','co','https','ecs','zyfg','rqpbjdwzr','f','eln','n']

#Agregar cada palabra dentro de la lista words_ al diccionario stop_words
for s in range(len(words_)):
    stop_words.append(words_[s])

#Funcion para eliminar las stopwords
def remove_stopwords(text):
    no_stopword_text = [w for w in text.split() if not w in stop_words]
    return ' '.join(no_stopword_text)

#Aplicar la funcion de eliminar las stopwords a las observaciones
df1['clean_Obs'] = df1['clean_Obs'].apply(lambda x: remove_stopwords(x))

# Imprimir las 100 palabras mas frecuentes 
freq_words(df1['clean_Obs'], 100)

#Identificar los sintomas presentes
sint_covid=['tos','fiebre','fatiga','muscular','cansancio','respiratoria','secrecion','secreciones','malestar','decaimiento']

#Funcion para detectar sintomas dentro de las observaciones limpias
def find_symp(text):
    sintomas=[i for i in text.split() if i in sint_covid]
    return ' '.join(sintomas)

#Aplicar la funcion para identificar sintomas a las observaciones
df1['Sintomas']=df1['clean_Obs'].apply(lambda x: find_symp(x))

#Funcion para contar el numero de sintomas detectados
def count_symp(text):
    num_sinto=len(text.split())
    return num_sinto

#Eliminar palabras duplicadas de la cadena de string
df1['Sintomas_Unicos']=(df1['Sintomas'].str.split().apply(lambda x: OrderedDict.fromkeys(x).keys()).str.join(' '))

#Aplicar la funcion para contar el numero de sintomas
df1['Numero_sintomas']=df1['Sintomas_Unicos'].apply(lambda x: count_symp(x))

#Filtrar por los que tengan sintomas de Covid
df2=df1[df1['Numero_sintomas']!=0]
#Organizar el dataframe
df3=df2.sort_values('Numero_sintomas',ascending=False)

#Contar el numero de veces que cada id_hash aparece
frecuencia=df3['id_hash'].value_counts().reset_index()
frecuencia.columns = ['id_hash', 'Frecuencia']

#Unir la columna de count del dataframe de frecuencia al dataframe final
df4=df3.merge(frecuencia, on='id_hash', how='left')

#Exportar a excel
df4.to_excel('Interacciones_11042020_Procesadas.xlsx')
