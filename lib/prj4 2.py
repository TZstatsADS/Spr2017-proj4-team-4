# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 20:40:39 2017

@author: ZISHUO LI
"""
dtm=pd.read_csv('pca.csv')
dtm=dtm.iloc[:,1:]



dtm2=dtm.copy()
dtm3=dtm.copy()


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


for x in range(5):
    lamb=loop(dtm5)

dtm6=dtm5.copy()



score(ts,lamb)









 
   


