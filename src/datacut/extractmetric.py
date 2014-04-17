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

    



def extract():
    s = ['profile.txt','content.txt','graph.txt','neighbor.txt']
    dir = r'E:/dataset/sssddata/14wan/feature/'
    userset = loaduser('../../../sssddata/14wan/feature/testset')
    spamset = loaduser('../../../sssddata/14wan/feature/14spamsuspend')
    print len(userset),len(spamset)
    metric={}
    for name in s:
        fname = open(dir+name,'r')
        for line in fname:
            temp = line.strip().split()
            if temp[0] in userset:
                try:
                    metric[temp[0]] += temp[1:]
                except:
                    metric[temp[0]] = temp[1:]
        fname.close()
    fout = open('../../../sssddata/14wan/feature/2-metric.arff','w')
    fout.write('@relation\t metric\n\n')
    
    fout.write('@attribute friends numeric\n')
    fout.write('@attribute follower numeric\n')
    fout.write('@attribute status numeric\n')
    fout.write('@attribute ff_ratio numeric\n')
    fout.write('@attribute age numeric\n')
    fout.write('@attribute following_rate numeric\n')
    fout.write('@attribute tweet_rate numeric\n')
    
    fout.write('@attribute url_ratio numeric\n')
    fout.write('@attribute oneurl_ratio numeric\n')
    fout.write('@attribute mention_raio numeric\n')
    fout.write('@attribute hash_ratio numeric\n')
    fout.write('@attribute ret_ratio numeric\n')
    fout.write('@attribute interval numeric\n')
    fout.write('@attribute tweet_per_day numeric\n')
    
    fout.write('@attribute bi-links numeric\n')
    fout.write('@attribute bi-links_raio numeric\n')
    fout.write('@attribute Clustering_Coefficient numeric\n')
    fout.write('@attribute Eccentricity numeric\n')
    fout.write('@attribute Closeness numeric\n')
    fout.write('@attribute Betweenness numeric\n')
    
    fout.write('@attribute avg_nbor_followers numeric\n')
    fout.write('@attribute avg_nbor_tweets numeric\n')
    fout.write('@attribute fings2_median_followers numeric\n')
    fout.write('@attribute Defective {Y,N}\n\n')
    
    fout.write('@data\n')    
    for uid in metric.keys():
        if uid in spamset:
            fout.write('\t'.join(metric[uid])+'\tY\n')
        else:
            fout.write('\t'.join(metric[uid])+'\tN\n')
    fout.close()    
    
        
def loaduser(file):
    f = open(file,'rb')
    userset = cp.load(f)
    f.close()
    return userset



if __name__ == '__main__':
    #run()
    extract()