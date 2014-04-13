# -*- coding: utf-8 -*-

'''
Created on 2014-4-13

@author: Administrator
'''

import os,sys
import cPickle as cp
from sklearn import preprocessing as pre
import numpy as np

def run():
    
    flast = open('../../../sssddata/14wan/1wan/spamset_lastuser','rb')
    spamset = cp.load(flast)
    biouser = cp.load(flast)
    print len(spamset),len(biouser)
    
    fuser = open(r'../../../sssddata/users.txt','r')
    usermetric={}
    feature=[]
    name={}
    count = 0
    for line in fuser:
        temp = line.strip().split()
        if len(temp)>0:
            if temp[0] in biouser:
                temp1=[float(f) for f in temp[2:5]]
                for x in range(0,len(temp1)):
                    if temp1[x]==0.0:
                        temp1[x] += 1.0
                usermetric[temp[0]]=temp1
                usermetric[temp[0]].append((float(temp1[0]))/(float(temp1[1]))) 
                feature.append([float(f) for f in usermetric[temp[0]]])
                name[temp[0]]=count
                count +=1
    X_train =np.log(np.array(feature)) 
   # min_max_scaler = pre.MinMaxScaler()
    #temp = min_max_scaler.fit_transform(X_train)  
    for n in usermetric.keys():
        usermetric[n]=[str(f) for f in X_train[name[n]]]
            
    fuser.close()  
    print len(usermetric.keys()),len(biouser)
    
    
    fbio = open('../../../sssddata/14wan/14wanfeature.txt','r')
    for line in fbio:
        temp = line.strip().split()
        if temp[0] in biouser:
            usermetric[temp[0]]+=temp[1:]
    fbio.close()
    

    userfeature=[]
    usernames={}
    count = 0
    for uid in usermetric.keys():
        usernames[uid]=count
        userfeature.append([float(f) for f in usermetric[uid]])
        count+=1
   # print userfeature
    X_train =np.array(userfeature)
    min_max_scaler = pre.MinMaxScaler()
    X_train = min_max_scaler.fit_transform(X_train)  
    for id in range(0, len(X_train)):
        for mid in range(0,len(X_train[id])):
            userfeature[id][mid]=str(X_train[id][mid])
    print 'precess loadfeature!',len(usernames.keys())
    
    
    
    fmetric = open('../../../sssddata/14wan/1wan/1wan_uid_metric.txt','w')
    fmetric1 = open('../../../sssddata/14wan/1wan/1wan_metric.txt','w')
    flog = open('../../../sssddata/14wan/1wan/1wan_metric_log.txt','w')
    for uid in usermetric.keys():
        if uid in spamset:
            flog.write('\t'.join(userfeature[usernames[uid]])+'\tY\n')
            fmetric.write(str(uid)+'\t'+'\t'.join(usermetric[uid])+'\tY\n')
            fmetric1.write('\t'.join(usermetric[uid])+'\tY\n')
        else:
            flog.write('\t'.join(userfeature[usernames[uid]])+'\tN\n')
            fmetric.write(str(uid)+'\t'+'\t'.join(usermetric[uid])+'\tN\n')
            fmetric1.write('\t'.join(usermetric[uid])+'\tN\n')
    fmetric.close()
    fmetric1.close()
    flog.close()
    
    
    fmetric = open('../../../sssddata/14wan/1wan/1wanfeature','wb')
    cp.dump(usermetric, fmetric, protocol=0)
    fmetric.close()

if __name__ == '__main__':
    run()