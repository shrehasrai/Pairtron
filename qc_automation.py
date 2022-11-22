#!/usr/bin/env python

import pandas as pd
import re
from Config import *
from datetime import datetime
import datetime
import os
import sys
df = pd.read_excel(source_file)
import numpy as np
df = df.replace(np.nan, '')

source_file = source_file.split('.')[0]

if os.path.exists(f'{source_file}.txt'):
    os.remove(f'{source_file}.txt')
    print(f'deleting priviouslg generated comments {source_file}.txt')

to_write = open(f'{source_file}.txt','a')

if not df.columns.tolist() == ['is_paid','source_id', 'manual_id', 'article_title', 'url', 'authors', 'author_affiliation', 'abstract_text', 'date', 'start_time', 'end_time', 'location', 'session_title', 'session_type', 'category', 'sub_category', 'disclosure']:
    print('hi there')
    to_write.write('#########################################################################\n\n row header is wrong \n\n#########################################################################')
    to_write.close()
    sys.exit("row header is wrong")



df = df.astype(str)
is_paid = df['is_paid'].tolist()
source_id = df['source_id'].tolist()
manual_id = df['manual_id'].tolist()
url = df['url'].tolist()
article_title = df['article_title'].tolist()
authors = df['authors'].tolist()
author_affiliation = df['author_affiliation'].tolist()
abstract_text = df['abstract_text'].tolist()
date = df['date'].tolist()
start_time = df['start_time'].tolist()
end_time = df['end_time'].tolist()
location = df['location'].tolist()
session_title = df['session_title'].tolist()
session_type = df['session_type'].tolist()
category = df['category'].tolist()
sub_category = df['sub_category'].tolist()
disclosure = df['disclosure'].tolist()

res = {'source_id':source_id,
'manual_id': manual_id,
'url':url,
'article_title':article_title,
'authors':authors,
'author_affiliation':author_affiliation,
'abstract_text':abstract_text,
'date':date,
'start_time':start_time,
'end_time':end_time,
'location':location,
'session_title':session_title,
'session_type':session_type,
'category':category,
'sub_category':sub_category,
'disclosure':disclosure}

paitron_msg = ''

    
def strip_str(res):
    msg = '##############################   extra space at start and end    ##################################\n\n'
    
    for key in res:
        
        ct = 1
        for data in res[key]:
            ct += 1
            temp_data = data.strip()
            
            if not data == temp_data:
                msg += f'{key} ============> Row no. {ct}\n'
            
            
    return f'{msg}\n\n'

temp_msg = strip_str(res)
paitron_msg += temp_msg
to_write.write(temp_msg)



def mid_format(res):
    msg = '##############################   invalid mid format   ##################################\n\n'
    
    for key in res:
        
        ct = 1
        for data in res[key]:
            ct += 1
            try:
                temp_data = re.search('(([A-Za-z]+_)+\d+)',data).group(1)
                
                if not data == temp_data:
                    msg += f'{key} ============>  Bad format   {temp_data} ================>Row no. {ct}\n'
            except:
                msg += f'{key} ============>  Bad format   {data} ================>Row no. {ct}\n'

            
    return f'{msg}\n\n'

temp_msg = mid_format({'manual_id': manual_id})
paitron_msg += temp_msg
to_write.write(temp_msg)



def line_breakes(res):
    msg = '##############################   line_breakes    ##################################\n\n'
    
    for key in res:
        ct = 1
        for data in res[key]:
            ct += 1
            
            temp_data = re.sub('\r','',data,flags=re.S)
            temp_data = re.sub('\n','',data,flags=re.S)
            
            if not data == temp_data:
                msg += f'{key} ============> Row no. {ct}\n'
            
            
    return f'{msg}\n\n'

temp_msg = line_breakes(res)
paitron_msg += temp_msg
to_write.write(temp_msg)


def author_aff_delimiter(res):
    msg = '##############################   Invalid author_aff_delimiter   ##################################\n\n'
    
    for key in res:
        
        ct = 1
        for data in res[key]:
            ct += 1
            temp_data = re.sub('\s*;\s*','; ',data,flags=re.S)
            
            if not data == temp_data:
                msg += f'{key} ============> Row no. {ct}\n'
            
            
    return f'{msg}\n\n'  

temp_msg = (author_aff_delimiter({'authors':authors, 'author_affiliation':author_affiliation}))
paitron_msg += temp_msg
to_write.write(temp_msg)


def space_(res):
    msg = '##############################   space in mid time url   ##################################\n\n'
    
    for key in res:
        
        ct = 1
        for data in res[key]:
            ct += 1
            if ' 'in data:
                msg += f'{key} ============> Row no. {ct}\n'
            
            
    return f'{msg}\n\n'   

temp_msg = space_({'manual_id':manual_id,'url':url, 'start_time':start_time, 'end_time':end_time})
paitron_msg += temp_msg
to_write.write(temp_msg)








def date_time_format(res):
    msg = '##############################   Invalid date_format   ##################################\n\n'
    
    for key in res:
        
        ct = 1
        for data in res[key]:
            ct += 1
            if not data:
                continue
            try:
                datetime.datetime.strptime(data, '%B %d, %Y')
                
            except:
                msg += f'{key} ============>Bad Format {data}   ===========>   Row no. {ct}\n'
            
            else:
                # October 18, 2022
                if not re.search('([A-Z][a-z]+ \d\d, \d\d\d\d)',data):
                    msg += f'{key} ============>Bad Format {data}   ===========>   Row no. {ct}\n'

            
    return f'{msg}\n\n'      

temp_msg = (date_time_format({'date':date}))
paitron_msg += temp_msg
to_write.write(temp_msg)


def start_end_time_format(res):
    msg = '##############################   Invalid start_end_time_format   ##################################\n\n'
    
    for key in res:
        
        ct = 1
        for data in res[key]:
            ct += 1
            
            if not data:
                continue
            try:
                datetime.datetime.strptime(data, '%H:%M')
                
            except:
                msg += f'{key} ============>Bad Format {data}   ===========>   Row no. {ct}\n'
                
            else:
                if not re.search('(\d\d:\d\d)',data):
                    msg += f'{key} ============>Bad Format {data}   ===========>   Row no. {ct}\n'
         
    return f'{msg}\n\n'      

temp_msg = (start_end_time_format({'start_time':start_time,'end_time':end_time}))
paitron_msg += temp_msg
to_write.write(temp_msg)


def start_end_time_les_0_6(res):
    msg = '##############################   time ( 7 =<time >= 0 )   ##################################\n\n'
    
    for key in res:
        
        ct = 1
        for data in res[key]:
            ct += 1
            if not data:
                continue
            try:
                temp_data = data.replace(' ','').replace(':','').strip()
                if int(temp_data) <= 700:
                    msg += f'{key} ============>    this early time not possible {data}   ===========>   Row no. {ct}\n'
            except:
                continue
                        
    return f'{msg}\n\n'      

temp_msg = (start_end_time_les_0_6({'start_time':start_time,'end_time':end_time}))
paitron_msg += temp_msg
to_write.write(temp_msg)

def is_paid_wrong_data(res):
    msg = '############################   Wrong data in is_paid   ##############################\n\n'

    for key in res:
        
        ct = 1
        for data in res[key]:
            ct += 1
            if data=='No' or data=="Yes":
                continue

            else:
                msg += f'{key} ============>    Wrong data in is_paid {data}   ===========>   Row no. {ct}\n'

        return f'{msg}\n\n'
    

temp_msg = is_paid_wrong_data({'is_pad':is_paid})
paitron_msg += temp_msg
to_write.write(temp_msg)

def start_end_time_morethan_2330(res):
    msg = '##############################   time ( time >= 23:30 )   ##################################\n\n'
    
    for key in res:
        
        ct = 1
        for data in res[key]:
            ct += 1
            if not data:
                continue
            try:

                temp_data = data.replace(' ','').replace(':','').strip()
                if int(temp_data) >= 2330:
                    msg += f'{key} ============>    this late time not possible {data}   ===========>   Row no. {ct}\n'
            except:
                continue
                        
    return f'{msg}\n\n'      

temp_msg = (start_end_time_morethan_2330({'start_time':start_time,'end_time':end_time}))
paitron_msg += temp_msg
to_write.write(temp_msg)


def invalid_end_time(res):
    msg = '##############################   start_time is blank but_end time is there   ##################################\n\n'

    ct = 1
    for x in range(len(res['start_time'])):
        ct += 1
        if not res['start_time'][x]:
            if res['end_time'][x]:
                msg += f'end_time ============>   end time not possible    ===========>   Row no. {ct}\n'
                
                        
    return f'{msg}\n\n'      

temp_msg = (invalid_end_time({'start_time':start_time,'end_time':end_time}))
paitron_msg += temp_msg
to_write.write(temp_msg)


def start_time_end_time(res):
    msg = '##############################   start_time end_time is same   ##################################\n\n'

    ct = 1
    for x in range(len(res['start_time'])):
        ct += 1
        if res['start_time'][x]== '':
            continue

        if res['start_time'][x] == res['end_time'][x]:
                msg += f'end_time ============>   start_time end_time is same    ===========>   Row no. {ct}\n'
                
                        
    return f'{msg}\n\n'      

temp_msg = (start_time_end_time({'start_time':start_time,'end_time':end_time}))
paitron_msg += temp_msg
to_write.write(temp_msg)



if '' in manual_id:
    temp_msg = '=================>  vacant cell found in manual_id column  <=================\n\n'
    to_write.write(temp_msg)
    
    
if '' in url:
    temp_msg = '=================>  vacant cell found in url column   <=================\n\n'
    to_write.write(temp_msg)
    
if '' in article_title:
    temp_msg = '=================>  vacant cell found in article_title column   <=================\n\n'
    to_write.write(temp_msg)

if '' in is_paid:
    temp_msg = '=================>  vacant cell found in is_paid column   <=================\n\n'
    to_write.write(temp_msg)

manual_id_to_b_unique = df["source_id"].tolist()
source_id_to_b_unique = df["manual_id"].tolist()
article_title_to_b_unique = df["article_title"].tolist()

manual_id_unique_dic = {}
source_id_unique_dic = {}
article_title_unique_dic = {}

for x in range(len(manual_id_to_b_unique)):
    if not manual_id_unique_dic.get(manual_id_to_b_unique[x],''):
        manual_id_unique_dic[manual_id_to_b_unique[x]] = 1
    else: 
        manual_id_unique_dic[manual_id_to_b_unique[x]] += 1

    if not source_id_unique_dic.get(source_id_to_b_unique[x],''):
        source_id_unique_dic[source_id_to_b_unique[x]] = 1
    else: 
        source_id_unique_dic[source_id_to_b_unique[x]] += 1
        
    if not article_title_unique_dic.get(article_title_to_b_unique[x],''):
        article_title_unique_dic[article_title_to_b_unique[x]] = 1
    else: 
        article_title_unique_dic[article_title_to_b_unique[x]] += 1
        
        
to_write_unique_manual_id = ''
to_write_unique_source_id = ''
to_write_unique_article_title = ''


for x,y in manual_id_unique_dic.items():
    if y>1 and x!='':
        to_write_unique_manual_id = to_write_unique_manual_id + f'{x} ===========> total count is {y}\n'
        
        
for x,y in source_id_unique_dic.items():
    if y>1 and x!='':
        to_write_unique_source_id = to_write_unique_source_id + f'{x} ===========> total count is {y}\n'
        
for x,y in article_title_unique_dic.items():
    if y>1 and x!='':
        to_write_unique_article_title = to_write_unique_article_title + f'{x} ===========> total count is {y}\n'

to_write_2 = f'''##############################   Duplicate mid  ##################################\n\n
          mannual_id which are not unique \n{to_write_unique_source_id}\n\n\n\n\n\n
-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#################################################################        Duplicates          ######################################################################
-------------------------------------------------------------------------------------------------------------------------------------------------------------------
          source_id which are not unique \n{to_write_unique_manual_id}\n\n\n\n\n\n
          
          artical_id which are not unique \n{to_write_unique_article_title}'''

to_write_2 = re.sub('1qaz2wsx.*?total count is \d+','',to_write_2)


# to_write_2 = str(to_write_2)
# to_write_2 = str(to_write_2.encode('utf-8'))
print(to_write_2)
to_write.write(to_write_2)
to_write.close()

# with open(f"{source_file}_unique_mid_sid_title.txt",'w',encoding='utf-8') as f:
#     f.write(to_write_2)
# to_write.close()


if paitron_msg.count('===========>')<1 and len(to_write_unique_source_id)<1:
    print(to_write_unique_source_id)

    os.system("python separate_authors.py")
    print('running separate_authors')
    
    

sponsor = ["Sponsor",
"Sponsored by",
"Sponsorship",
"Fund",
"Funded by",
"Financed",
"Financed by",
"Financial support",
"Supported by",
"Acknowledgement",
"Acknowledged by",
"Registration ID",
"Clinical Trial ID"]


sponsor_msg = ''


def sponsor_col(res):
    msg = '##############################   sponsor   ##################################\n\n'
    
    for key in res:
        ct = 1
        for data in res[key]:
            ct += 1
            
            for sp_key in sponsor:
                if sp_key.lower() in data.lower():

                    msg += f'May can be sponsor {sp_key} ==========> {key} ============> Row no. {ct}\n'
            
            
    return f'{msg}\n\n'

temp_msg = sponsor_col({"abstract_text":abstract_text})
sponsor_msg += temp_msg

with open(f'{source_file}_sponsor.txt','w')as s_dtails:
    s_dtails.write(sponsor_msg)


