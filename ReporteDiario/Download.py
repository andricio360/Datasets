# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 10:53:41 2020
@author: use
"""

import os
from datetime import datetime, timedelta
import pandas as pd
import requests
import numpy as np


def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s



def DonwloadTrend(Hashtag, dia, mes):

    data_Hashtag_FilT=pd.DataFrame()
    try:
    
        
        Hashtag=normalize(Hashtag).lower()
        
        #Test consumiendo HTTP
        URL = "http://54.159.73.101/Hashtag/index.php?dia="+str(dia)+"&mes="+str(mes)
        
        allData = requests.get(url = URL).text
        
        
        test = allData.split("\n")
        Hashtag_Mes = pd.DataFrame()
        
                
        Hashtag_Mes["a"] = [test[i].split(";")[0] if len(test[i].split(";"))>=3 else '' for i in range(len(test))]
        Hashtag_Mes["b"] = [test[i].split(";")[1] if len(test[i].split(";"))>=3 else '' for i in range(len(test))]
        Hashtag_Mes["c"] = [test[i].split(";")[2] if len(test[i].split(";"))>=3 else '' for i in range(len(test))]
        Hashtag_Mes["d"] = [test[i].split(";")[3] if len(test[i].split(";"))>=4 else '' for i in range(len(test))]
        
        
        Hashtag_Mes.c = Hashtag_Mes.c.map(lambda x: normalize(x))
        Hashtag_Cantidades=Hashtag_Mes.c.to_list()
        for i in range(0,len(Hashtag_Cantidades)):
            #    print (Hashtag_Cantidades[i])
                try:
                    if "Trendin" in Hashtag_Cantidades[i]: 
                        Hashtag_Cantidades[i]=np.nan
                except:
                    pass
        Hashtag_Mes.c=Hashtag_Cantidades
        Hashtag_Mes.c=Hashtag_Mes.c.str.lower()
        data_Hashtag_Fil1=Hashtag_Mes[(Hashtag_Mes.c==Hashtag)]
        data_Hashtag_Fil2=Hashtag_Mes[(Hashtag_Mes.c=="#"+Hashtag)]
        frames = [data_Hashtag_Fil1, data_Hashtag_Fil2]
        data_Hashtag_FilT= pd.concat(frames)
        data_Hashtag_FilT = data_Hashtag_FilT.drop_duplicates()
        data_Hashtag_FilT=data_Hashtag_FilT.reset_index()
        
        return data_Hashtag_FilT 
    except:
        return data_Hashtag_FilT 
    
    
    
