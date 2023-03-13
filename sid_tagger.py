#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
file_name = config['file_info']
file_name = file_name['name_of_the_file']
print(file_name)

if '.xlsx' not in file_name:
    file_name = file_name + '.xlsx'
    
df = pd.read_excel(file_name)
df = df.fillna('')
df=df.astype(str)

max_ = 0

for x in df['session_id']:
    if x == '':
        continue
    else:
        x = int(x.replace('S',''))
        if max_<x:
            max_=x
            
            
var = df.groupby('session_title')
gp_bucket = pd.DataFrame()
gp_head = pd.DataFrame()
for name, group in var:
    
    if group['news_type'].tolist().count('Session')>1:
        
        for index, row in group.iterrows():
            if row['session_id'] == '':
                row['session_id'] = f'S{max_+1}'
                gp_bucket = pd.concat([gp_bucket, pd.DataFrame([row])], axis=0)
                max_ += 1
            else:
                gp_bucket = pd.concat([gp_bucket, pd.DataFrame([row])], axis=0)
    
        
    else:
        if len(group)==1:
            if group['session_id'].tolist() == ['']:
                group['session_id'] = f'S{max_+1}'
                max_ += 1
                gp_head = pd.concat([gp_head, group], axis=0)
                
            else:
                gp_head = pd.concat([gp_head, group], axis=0)
        else:
            
            if len(set(group['session_id'])) == 2:
                
                filtered_group = list(set(group['session_id']))
                filtered_group.sort(reverse = True)

                group['session_id'] = filtered_group[0]
                gp_head = pd.concat([gp_head, group], axis=0)
                
            elif set(group['session_id']) == {''}:
                group['session_id'] = f'S{max_+1}'
                gp_head = pd.concat([gp_head, group], axis=0)
                max_ += 1

            
            elif len(set(group['session_id'])) == 1:
                gp_head = pd.concat([gp_head, group], axis=0)
                

result = pd.concat([gp_head,gp_bucket], axis=0)

result.to_excel('op.xlsx')
