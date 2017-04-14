# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 15:17:10 2017
@author: ZISHUO LI
"""
import re
import os
import pandas as pd
import numpy as np
import nltk
import pylab as pl
from scipy import optimize
from numpy import linalg as LA
os.getcwd()
''' change your working directory '''
os.chdir('C:\\Users\\ZISHUO LI\\Documents\\GitHub\\Spr2017-proj4-team-4\\data\\nameset\\')
with open('AKumar.txt') as f:
    content = f.readlines()

content=pd.DataFrame([x.lower().rstrip('\n').split('<>') for x in content])
content.columns=['author','title','publish']
content2=content.copy()
nrows=content2.shape[0]

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

''' define funtion to match name and take three characters as juding standard'''
def partial_match(x,y): 
   for i in range(len(x)):
        for j in range(len(y)):                                    
            if x[i] == y[j]:
                inter1=x.copy()
                inter2=y.copy()                
                inter1.remove(x[i])
                inter2.remove(y[j])
                for n in range(len(inter1)):
                    for m in range(len(inter2)):
                        if inter1[n].startswith(inter2[m]) or inter2[m].startswith(inter1[n]):
                            return (True)        
def match(x,y):
    if x == y:
        return (True)
    elif x[0:4] in y[0:4] or x[(len(x)-4):len(x)] in y[(len(y)-4):len(y)] :  # judge if head and tail or inter are equal
        x_splited=x.split(' ')                                    
        y_splited=y.split(' ')        
        if x[0:4] in y[0:4] and x[(len(x)-4):len(x)] in y[(len(y)-4):len(y)]:       # judge head and tail are equal
            return (True)
        else:
            return (partial_match(x_splited,y_splited))
                
#define wether a list match with another list.
def list_match(x,y):
    for i in range(len(x)):
        for j in range(len(y)):
            if match(x[i],y[j]):
                return (True)
cluster=list(range(len(author_new)))
#judge cluster
publish_set=[set([x]) for x in content['publish']]
title_set=[set([x]) for x in content['title']]
for i in range(len(author_new)):
    for j in range(i + 1, len(author_new)):
        inter=list_match(author_new[i], author_new[j])
        if inter==True:
            cluster[j]=cluster[i]
            publish_set[i].update(publish_set[j])
            publish_set[j]=publish_set[i].copy()
            title_set[i].update(title_set[j])
            title_set[j]=title_set[i].copy()
#cluster_index,counts=np.unique(cluster,return_counts=True)
cluster=pd.DataFrame(cluster)

title_set=pd.DataFrame([';'.join(x) for x in title_set])
title_set=pd.DataFrame(title_set)

title_set.to_csv('dd5.csv')



'''  between this two step, we use R to deal with the data'''

dtm=pd.read_csv('pca.csv')
dtm=dtm.iloc[:,1:]

c=dtm.shape[1]
lamb=[1/c]*c
label=[int(x) for x in content['author']]

def cor(x,y):
    x_y=pd.concat([x,y],axis=0)
    correlation=x_y.apply(np.var,0)
    return (correlation)    
def score(var,lamb):
    return (sum(var*lamb))


def Ts(x,y):
    ts_1_x=np.where(dtm_index_copy==group_unique[x])
    ts_1_y=np.where(dtm_index_copy==group_unique[y])        
    answer=cor(dtm.iloc[ts_1_x[0],:],dtm.iloc[ts_1_y[0],:])
    group_unique_left=[m for m in group_unique if m!=group_unique[x] and m!=group_unique[y]]
    for p in range(len(group_unique_left)):
        for l in range(p+1,len(group_unique_left)):
            ts_1_x=np.where(dtm_index_copy==group_unique[x])
            ts_1_y=np.where(dtm_index_copy==group_unique[y])        
            inter=cor(dtm.iloc[ts_1_x[0],:],dtm.iloc[ts_1_y[0],:])
            answer+=inter
    return (answer)


def group_precision(x,y):
    g1=np.where(dtm_index_copy==group_unique[x])
    g2=np.where(dtm_index_copy==group_unique[y])        
    dtm_index_copy2=dtm_index_copy.copy()
    answer=[]
    for o in range(len(dtm_index_copy2)):
        if dtm_index_copy2[o]!=group_unique[y] :
            answer.append(dtm_index_copy2[o])
        else:
            answer.append(group_unique[x])
    return (answer)
    
def precision(group):
    A=0
    B=0
    C=0
    D=0
    for i in range(len(group)):
        for j in range(len(group)):
            if group[i]==group[j] and label[i]==label[j]:
                A+=1
            elif group[i]==group[j] and label[i]!=label[j]:
                B+=1
            elif group[i]!=group[j] and label[i]==label[j]:
                C+=1
            else:
                D+=1
    
    Precision=A/(A+B)
    Recall=A/(A+C)
    F1=2*Precision*Recall/(Precision+Recall)
    Accuracy=(A+D)/(A+B+C+D)
    print(' '.join(['Accuracy:',str(Accuracy)]))
    print(' '.join(['Precision:',str(Precision)])) 
    return (Precision)  
 
   
def mira(la,tao,ts,ts1,par=5000):
    n_ft=len(lamb)

    accumulator = list()
    def f(x):
    # Store the list of function calls
        accumulator.append(x)
        return LA.norm([a-b for a,b in zip(x,lamb)])

    def constraint1(x):
        return np.atleast_1d(np.inner(x,ts)-np.inner(x,ts1)-par)
    def constraint2(x):
        return np.atleast_1d(-tao+np.inner(x,ts))

    opt=optimize.fmin_slsqp(f, np.array([0]*n_ft),
                       ieqcons=[constraint1,constraint2, ])
    return(opt)


def loop(dtm,tao=5000):
    global lamb
    global dtm_index_copy
    global group_unique
    group_unique=np.unique(dtm.index)
    cluster_number=group_unique.size
    cor_list=[]
    location_list=[]
    ''' loop first time  '''
    r=cluster_number
    for i in range(r):
        for j in range(i+1,r):
            i_loc=np.where(dtm.index==group_unique[i])
            j_loc=np.where(dtm.index==group_unique[j])
            var=cor(dtm.iloc[i_loc[0],:],dtm.iloc[j_loc[0],:])         
            inter=score(var,lamb)
            cor_list.append(inter)
            location_list.append([i,j])
    
    cor_list=cor_list/np.mean(cor_list)
    location=np.array(np.where(cor_list==min(cor_list)))
    location_list=np.array(location_list)
    location_min=location_list[location]
    
    ''' group part'''   
    group=[x for x in range(r)]
    group_copy=group.copy()
    
    for i in range(location.size):
        num1=location_min[0][i][0]
        num2=location_min[0][i][1]
        g_loc2=np.where(group==num2)
        if len(g_loc2[0])!=0:
            group[g_loc2[0][0]]=num1
        
        dtm_loc=np.where(dtm.index==group_unique[num2])
        ''' generate new dtm index'''
        dtm_index_copy=dtm.index.copy()      
        dtm_new=[]
        for x in dtm_index_copy:
            if x==group_unique[num2]:
                dtm_new.extend([group_unique[num1]])
            else:
                dtm_new.extend([x])
        ''' store dtm_new into dtm index'''
        dtm.index=dtm_new   
    '''accuration part'''    
    group=dtm.index.copy() 
    precision_st=precision(group)
    
    if precision_st <=0.95:
        # get ts : total score without using paramter
        ts_cluster=np.unique(dtm.index).size
        group_unique_ts=np.unique(dtm.index)
        ts=np.repeat(0,dtm.shape[1])
        for m in range(ts_cluster):
            for n in range(m+1,ts_cluster):
                m_loc=np.where(dtm.index==group_unique_ts[m])
                n_loc=np.where(dtm.index==group_unique_ts[n])
                var=cor(dtm.iloc[m_loc[0],:],dtm.iloc[n_loc[0],:])
                ts=ts+var.values
        
        for i in range(len(group_unique)):
            for j in range(i+1,len(group_unique)):
                    judge_precision=precision(group_precision(i,j))
                    if judge_precision >precision_st:
                        print([i,j])
                        ts1=Ts(i,j)                 
                        lamb=mira(la=lamb,tao=tao,ts=ts,ts1=ts1)  
                        dtm=dtm2.copy()
                        break
            if judge_precision> precision_st:
                break
    print(np.unique(dtm.index).size) 
    print(lamb)               
    return (lamb) 



n=0
while np.unique(dtm.index).size>=14 or n<1000: 
    lamb=loop(dtm)
    n+=1 
 


'''
dtm2=dtm.copy()
dtm3=dtm.copy()
dtm=dtm3.copy()
score(ts,lamb)
np.unique(dtm3.index).size

