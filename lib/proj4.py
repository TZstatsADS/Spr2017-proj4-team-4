# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 15:17:10 2017
@author: ZISHUO LI
"""
import re
import os
import pandas as pd
import numpy as np
os.getcwd()
os.chdir('C:\\Users\\ZISHUO LI\\Documents\\GitHub\\Spr2017-proj4-team-4\\data\\nameset\\')
with open('AKumar.txt') as f:
    content = f.readlines()

content=pd.DataFrame([x.lower().rstrip('\n').split('<>') for x in content])
content.columns=['author','title','publish']

author=content['author']
author_splited=[x.split(';') for x in author]

pattern='[0-9]+_[0-9]+'
# generate index
index=[re.search(pattern,x).group(0) for x in author]
index_splited=pd.DataFrame([x.split('_') for x in index])
# generate author
index_len=[len(x) for x in index]
author=pd.DataFrame([x[m:len(x)] for x,m in zip(author, index_len)])

#combine them together
content=pd.concat([index_splited,author,content[['title','publish']]],axis=1)
content.columns=['author','index','co-author','title','publish']
'''
clean author part

'''
# deal with co-author in original data
content['co-author']=[x.strip() for x in content['co-author']]
content['co-author']=[x.strip(';') for x in content['co-author']]

# seperate each author 
author=[x.split(';') for x in content['co-author']]
author_inter=[]
for i in range(len(author)):
    inter=[x.strip() for x in author[i]]
    author_inter.append(inter) 
author=author_inter.copy()  # generate a list of author


''' generate all author'''
all_author=[]
for i in range(len(author)):
    inter=[x for x in author[i]]
    all_author.extend(inter)
    
all_author=np.array(all_author)
''' generate author_name'''
author_unique, counts=np.unique(all_author,return_counts=True)
author_name=author_unique[np.argmax(counts)]


'''remove the name which len are smaller than 3'''
author_cleaned=[]
for i in range(len(author)):
    inter=[x for x in author[i] if len(x)>=3]
    author_cleaned.append(inter)

#remove author
author_new=[]
for i in range(len(author_cleaned)):
    if author_name in author_cleaned[i]:
        inter=author_cleaned[i].copy()
        inter.remove(author_name) 
    author_new.append(inter)
# we have already got the final 


# define funtion to match name and take three characters as juding standard
def partial_match(x,y): 
   for i in range(len(x)):
        for j in range(len(y)):                        
            x_feature=[x[i][0:3],x[i][(len(x)-3):]]
            y_feature=[y[j][0:3],y[j][(len(y)-3):]] 
            if x_feature[0] in y_feature[0] and x_feature[1] in y_feature[1]:
                x.remove(x[i])
                y.remove(y[j])
                return (list_match(x,y))              


def match(x,y):
    if x == y:
            return (True)
    x_index=[x[0:4],x[(len(x)-4):]]        
    for i in range(len(x)-6):
        inter=x[i:i+6]
        if x_index[0] in y[0:4] or x_index[1] in y[(len(y)-4):len(y)] or inter in y:
            x_splited=x.split(' ')
            y_splited=y.split(' ')        
            if x_index[0] in y[0:4] and x_index[1] in y[(len(y)-4):len(y)]:
                return (True)
            else:
                partial_match(x_splited,y_splited)
                
            
#define wether a list match with another list.
def list_match(x,y):
    for i in range(len(x)):
        for j in range(len(y)):
            if match(x[i],y[j]):
                return (True)


cluster=list(range(len(author_new)))

#judge cluster
author_new2=author_new.copy()
author_set=[set(x) for x in author_new2]
for i in range(len(author_new2)):
    for j in range(i + 1, len(author_new2)):
        inter=list_match(author_new[i], author_new[j])
        if inter==True:
            cluster[j]=cluster[i]
            author_set[i].update(author_set[j])
            author_set[j]=author_set[i].copy()
            
cluster



#cluster_index,counts=np.unique(cluster,return_counts=True)

cluster=pd.DataFrame(cluster)
dd=pd.concat([cluster,content[['author','co-author']]],axis=1)



dd.to_csv('dd.txt')


a='shun yan cheung'
b='kei-hoi cheung'
match(a,b)


x='s y cheung'
y='shun yan cheung'
match(x,y)
