# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 20:40:39 2017

@author: ZISHUO LI
"""
# the best score:
unique_cluster=np.unique([int(x) for x in content['author'].values])
best_score_var=


dtm=pd.read_csv('pca.csv')
dtm.shape


dtm2=dtm.copy()
dtm3=dtm.copy()

dtm=dtm.iloc[:,1:]
c=dtm.shape[1]
r=dtm.shape[0]

lamb=[1/c]*c
label=[int(x) for x in content['author']]

def cor(x,y):
    x_y=pd.concat([x,y],axis=0)
    correlation=x_y.apply(np.var,0)
    return (correlation)    
def score(var,lamb):
    return (sum(var*lamb))
'''initial assignment'''


for x in range(15):
    loop()











 
   


