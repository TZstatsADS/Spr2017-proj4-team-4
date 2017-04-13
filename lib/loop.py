# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 11:56:24 2017

@author: ZISHUO LI
"""

        ts=np.repeat(0,dtm.shape[1])

                ts=ts+var.values

       ts_=pd.inner(var_list,lamb)

def mira(lamb,tao,ts,ts1):
    n_ft=len(lamb)

    accumulator = list()
    def f(x):
    # Store the list of function calls
        accumulator.append(x)
        return LA.norm([a-b for a,b in zip(x,lamb)])

    def constraint1(x):
        return np.atleast_1d(np.inner(x,ts)-np.inner(x,ts1)-1)
    def constraint2(x):
        return np.atleast_1d(tao-np.inner(x,ts))

    opt=optimize.fmin_slsqp(f, np.array([0]*n_ft),
                       ieqcons=[constraint1,constraint2, ])
    return(opt)


def loop(dtm):
    group_unique=np.unique(dtm.index)
    cluster_number=group_unique.size
    cor_list=[]
    location_list=[]
    ''' loop first time  '''
    r=cluster_number
    global var_list
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
    #global Precision_previous    
    Precision=A/(A+B)
    #Precision_previous=Precision.copy()
    Recall=A/(A+C)
    F1=2*Precision*Recall/(Precision+Recall)
    Accuracy=(A+D)/(A+B+C+D)    
    print(' '.join(['Precision:',str(Precision)]))
    print(' '.join(['Recall:',str(Recall)]))
    print(' '.join(['F1:',str(F1)]))
    print(' '.join(['Accuracy:',str(Accuracy)]))
    
    #if Precision <=0.95:
        
        
    
    
    
    
    return (np.unique(dtm.index).size) 
        
    