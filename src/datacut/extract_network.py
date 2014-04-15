# -*- coding: utf-8 -*-
'''
Created on 2014-4-14

@author: Administrator
'''
import sys, os
import cPickle as pickle 


def run():
    
    
    
    allusers=set()
    fuser = open(r'../../../sssddata/users.txt','r')
    for line in fuser:
        temp = line.strip().split()
        if len(temp)>0:
            allusers.add(temp[0])
    fuser.close()    
     
    user14wan = set(os.listdir(r'E:/dataset/tweets/'))       
    user13wan=user14wan & allusers
     
     
    #==========================================================================
     # userset=set()
     # allnet = open(r'E:\dataset\UDI-TwitterCrawl-Aug2012-Network\network.txt','r')
     # fnetwork=open(r'../../../sssddata/14wan/newnetworks','w')
     # count = 0
     # for line in allnet:
     #     count += 1
     #     if count %10000000==0:
     #         print count 
     #     temp = line.strip().split()
     #     if temp[0] in user13wan and temp[1] in user13wan:
     #         fnetwork.write(line)
     #         userset.update(temp)
     # print len(userset),len(user13wan)
     # fnetwork.close()
     # allnet.close()
     #==========================================================================

    outfspam = open(r'../../../sssddata/14wan/14spamsuspend','rb')
    spamset =pickle.load(outfspam)
    print len(spamset)
    outfspam.close()
     
    userset= set()
    fnetwork=open(r'../../../sssddata/14wan/newnetworks','r')
     
    count = 0
    for line in fnetwork:
        count +=1
        #if count %100000 ==0:
        #    print count,len(userset)
        temp = line.strip().split()
        if temp[0] in spamset or temp[1] in spamset:
            userset.update(temp)        
    print len(userset)
    fuser = open('../../../sssddata/14wan/feature/userset','wb')
    pickle.dump(userset, fuser, protocol=0)
    fuser.close()
     
     
     
     
    fsmallnet = open(r'../../../sssddata/14wan/1-smallnet.txt','w')
    follow={}
    follower={}     
    fnetwork.seek(0)
    for line in fnetwork:
        temp = line.strip().split()
        if temp[0] in userset and temp[1] in userset:
            fsmallnet.write(line)
            try:
                follow[temp[0]].add(temp[1])
            except:
                follow[temp[0]]=set()    
                follow[temp[0]].add(temp[1])  
            try:
                follower[temp[1]].add(temp[0])
            except:
                follower[temp[1]]=set()         
                follower[temp[1]].add(temp[0]) 
    biouser = set(follower.keys())&set(follow.keys())
    print 'bio user',len(userset),len(biouser) ,len(set(follower.keys())&set(follow.keys()) &user13wan)
    print 'spam', len(spamset),len(spamset&userset),len(spamset&biouser)
    fsmallnet.close()
     
     
     
     #去叶子节点，即度为1的节点
    while 1:
         follower.clear()
         follow.clear()
         fnetwork.seek(0)
         for line in fnetwork:
             count +=1
             temp = line.strip().split()
             if temp[0] in biouser and temp[1] in biouser:
                 userset.update(temp)  
                 try:
                     follow[temp[0]].add(temp[1])
                 except:
                     follow[temp[0]]=set()    
                     follow[temp[0]].add(temp[1])  
                 try:
                     follower[temp[1]].add(temp[0])
                 except:
                     follower[temp[1]]=set()         
                     follower[temp[1]].add(temp[0]) 
         biouser = set(follower.keys())&set(follow.keys())
         print 'bio user',len(biouser),len(follow.keys()),len(follower.keys())  
         if len(biouser)==len(follow.keys()) and len(biouser)==len(follower.keys()):
             break     
    spamset = biouser & spamset
    print 'last users:',len(biouser),len(spamset)
     
     
     
    fsmallnet = open(r'../../../sssddata/14wan/1-smallnet-bio.txt','w')
    fnetwork.seek(0)
    for line in fnetwork:
        temp = line.strip().split()
        if temp[0] in biouser and temp[1] in biouser:
            fsmallnet.write(line)
    fsmallnet.close()
     
     
     
     
     #输出新的网络
    foutnet = open(r'../../../sssddata/14wan/1-outnet.txt','w')
    finnet = open(r'../../../sssddata/14wan/1-innet.txt','w')
    for user in follow.keys():
         foutnet.write(user+'\t'+'\t'.join(list(follow[user]))+'\n')
    for user in follower.keys():
         finnet.write(user+'\t'+'\t'.join(list(follower[user]))+'\n')
    foutnet.close()
    finnet.close()
     
    fbad = open('../../../sssddata/14wan/spamset_bio','wb')
    pickle.dump(spamset, fbad, protocol=0)
    fbad.close()
     
     
     
     
     
    nfollow = []
    nfollower = []
    for u in follow.keys():
         nfollow.append(len(follow[u]))
    for u in follower.keys():
         nfollower.append(len(follower[u]))
    nfollow.sort(reverse=True)
    nfollower.sort(reverse=True)
    dictout={}
    dictin={}
    fn = open(r'../../../sssddata/14wan/countoutdegree-cut.txt','w')
    fner = open(r'../../../sssddata/14wan/countindegree-cut.txt','w')
    dictout[0]=len(userset-set(follow.keys()))
    for it in nfollow:
         try:
             dictout[it] +=1
         except:
             dictout[it]=1
    for key in dictout.keys():
         fn.write(str(key)+'\t'+str(dictout[key])+'\n')
          
    dictin[0]=len(userset-set(follower.keys()))
    for it in nfollower:
         try:
             dictin[it] +=1
         except:
             dictin[it]=1
    for key in dictin.keys():
         fner.write(str(key)+'\t'+str(dictin[key])+'\n')
    fn.close()
    fner.close()      
    print 'network count complete!'
 
    fnetwork.close()
     
    
    
    usershare=set()
    fshare = open(r'../../../sssddata/14wan/14wanurlshare.txt','r')
    furlnet = open(r'../../../sssddata/14wan/urlsharenet.txt','w')
    count = 0
    for line in fshare:
        count +=1
        #if count %100000 ==0:
           # print count,len(usershare)
        temp = line.strip().split()
        if temp[0] in spamset or temp[1] in spamset:
            #if float(temp[2])>0.001:
                #furlnet.write(line)  
                usershare.update(temp[0:2])  
    userlast=biouser & usershare 
    print len(userlast),len(spamset&userlast),len(spamset&usershare)
    fshare.seek(0)   
    usershare.clear()
    for line in fshare:
        count +=1
        #if count %100000 ==0:
           # print count,len(usershare)
        temp = line.strip().split()
        if temp[0] in userlast and temp[1] in userlast:
           # if float(temp[2])>0.001:
                furlnet.write(line)  
                usershare.update(temp[0:2])  
    #userlast=biouser & usershare 
    print len(usershare)
    furlnet.close()
    fshare.close()
    
    
    
if __name__ == '__main__':
    run()         