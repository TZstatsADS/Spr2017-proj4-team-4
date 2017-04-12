# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 20:40:39 2017

@author: ZISHUO LI
"""

dtm=pd.read_csv('dtm.csv')
dtm=dtm.iloc[:,1:]
c=dtm.shape[1]
r=dtm.shape[0]


lamda=[1/c]*c

def cor(x,y):
    x_y=pd.concat([x,y],axis=1)
    correlation=x_y.apply(np.var,1)
    return (correlation)    

def score(var,lamb):
    return (sum(var*lamb))

cor_list=[]
location_list=[]
for i in range(r):
    for j in range(i+1,r):
        var=cor(dtm.iloc[i,:],dtm.iloc[j,:])
        inter=score(var,lamb)
        cor_list.append(inter)
        location_list.append([i,j])

cor_list=cor_list/np.mean(cor_list)
location=np.array(np.where(cor_list==min(cor_list)))
location=[i for i in location]
location_list=np.array(location_list)
location_list[location]





dtm.iloc[[21,89],:]












