# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 11:56:24 2017

@author: ZISHUO LI
"""
#这是这俩分的情况下的ts
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

