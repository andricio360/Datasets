# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:57:06 2020

@author: Analytics - DAPRE
"""

import pandas as pd

url="MencionesDiarias/DuqueDiariodata.xlsx"
File1=pd.read_excel(url)
File1=File1[['Autor', 'Tweet',"Hora", 'Interacciones', 'Link']]
horas=File1.Hora.unique()
horas.sort()
C_I=[]


for i in horas:
    df_C_I = File1[File1.Hora == i]
    C_I.append(len(df_C_I))

    
df_I=pd.DataFrame({"Hora":horas, "Coronavirus":C_I})

File1['RT']=['RT' if 'RT @' in str(x)[:] else 'ORIGINAL' for x in File1.Tweet]

df_C_I_2= File1[File1.RT== "ORIGINAL"]
result2 = df_C_I_2.sort_values(by=['Interacciones'],ascending=False)
result2=result2.reset_index()
result3=result2[result2.index<5]
result3=result3[['Autor', 'Tweet', 'Interacciones', 'Link']]



result4=df_C_I_2[['Autor','Interacciones']]
g = result4.groupby(['Autor'])['Interacciones'].sum().to_frame()
g = g.sort_values(by=['Interacciones'],ascending=False)
g=g.reset_index()
g=g[g.index<5]
Autores=result4.Autor.unique()




url2="MencionesDiarias/DuqueDiarioConsolidado.xlsx"
File1=pd.read_excel(url2)
LTemas=File1.Tema.value_counts()

writer = pd.ExcelWriter('Infogram_Coronavirus.xlsx', engine='xlsxwriter')
df_I.to_excel(writer,sheet_name='Linea de Tiempo')
g.to_excel(writer,sheet_name='Autores con más interacciones')
result3.to_excel(writer, sheet_name='Publicaciones')
LTemas.to_excel(writer, sheet_name='Nube de Temas')
writer.save()
