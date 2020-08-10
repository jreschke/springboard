# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 07:05:47 2020

@author: jenny
"""
import requests
import time
import pandas as pd

#grabbing the user data from web scrapping
users = pd.read_csv("C:\\Users\\jenny\\Desktop\\cod\\cod\\users.csv")
t = 1
#the loop for each user
for row in range(0,99):
    url = users.iloc[row,0]
    holding = url.rfind('/')
    user = url[(holding+1):]
    game_type = url[(url.rfind('/',0,holding)+1):holding]

    #this is to change the titles to meet the api
    if game_type == 'ps4':
        game_type = 'psn'
    elif game_type == 'pc':
        game_type = 'battle'
    elif game_type == 'xbox':
        game_type = 'xbl'
    elif game_type == 'act':
        game_type = 'uno'
    
    url = "https://call-of-duty-modern-warfare.p.rapidapi.com/multiplayer/"+user+"/"+game_type
    
    headers = {
        'x-rapidapi-host': "call-of-duty-modern-warfare.p.rapidapi.com",
        'x-rapidapi-key': "85be852fa8msh73af847c6aab55dp1cd6c2jsn0564acdc6d4f"
        }
    
    response = requests.request("GET", url, headers=headers)
    time.sleep(-time.time()%1)
    dic_r = response.json()
    if len(dic_r)>2:
        data = dic_r['lifetime']['itemData']
        for key, item in data.items():
            for key2, item2 in data[key].items():
               if(t==1):
                   holder = data[key][key2]['properties']
                   all_time = pd.DataFrame.from_dict(holder, orient='index')
                   result = all_time.transpose()
                   result['weapon'] = key2
                   result['weapontype']=key
                   result['user']=user
                   result['gametype']=game_type
                   t = 2
               else:
                   holder = data[key][key2]['properties']
                   all_time = pd.DataFrame.from_dict(holder, orient='index')
                   all_t2 = all_time.transpose()
                   all_t2['weapon'] = key2
                   all_t2['weapontype']=key
                   all_t2['user']=user
                   all_t2['gametype']=game_type
                   result = pd.concat([result,all_t2],axis=0,sort=False)
result.to_csv("C:\\Users\\jenny\\Desktop\\cod\\cod\\users-data.csv",index = False, header=True)