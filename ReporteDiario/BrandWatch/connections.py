# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 09:23:55 2019

@author: DANIELA DIAZ
"""

import pandas as pd 
import re
from datetime import datetime

data_BD = pd.read_excel('paro21Nov.xlsx')
data_BD=data_BD.iloc[5::]
data_BD.columns = data_BD.iloc[0]
data_BD=data_BD.drop(data_BD.index[0])
data_BD=data_BD.reset_index()

connections_to = []
connections_from = []
timestamp_ = []

for tweet in range(len(data_BD)):
    if data_BD['Page Type'][tweet] == 'twitter':
        if 'RT @' in data_BD['Full Text'][tweet]:
            connections_to.append(data_BD['Author'][tweet])
            date_=data_BD['Date'][tweet].split('.')
            date_ = datetime.strptime(date_[0], '%Y-%m-%d %H:%M:%S')
            timestamp_.append(date_.isoformat())
            try:
                user = re.findall(r"@(\w+)",data_BD['Full Text'][tweet])[0]
                connections_from.append(user)
            except:
                try:        
                    user = re.findall(r"RT (\w+)", data_BD['Full Text'][tweet])[0]
                    connections_from.append(user)
                except:
                    print('Unidentified user')
                    connections_from.append('IvanDuque')
                    
Connection = pd.DataFrame(data={'Target':connections_to,
                                'Source':connections_from,
                                'timeset':timestamp_
                                }).to_excel('connections.xlsx')
    

