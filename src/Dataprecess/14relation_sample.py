# -*- coding: utf-8 -*-
'''
Created on 2014-4-11

@author: Administrator
'''
import sys, os
import cPickle as pickle 


def run():
    #try:
        allusers=set()
        count=0
        userset=set()
        outfspam = open(r'../../../sssddata/14wan/14spamsuspend','rb')
        spamset =pickle.load(outfspam)
        print len(spamset)
        usernet = {}
        usershare =set()
        fspam = open(r'../../../sssddata/14wan/14wanlabel-spam.txt','r')
        fnetwork=open(r'../../../sssddata/14wan/newnetworks','r')
        fshare = open(r'../../../sssddata/14wan/14wanurlshare.txt','r')
        fuser = open(r'../../../sssddata/users.txt','r')
        fsmallnet = open(r'../../../sssddata/14wan/1-smallnet.txt','w')
        
        for line in fuser:
            temp = line.strip().split()
            if len(temp)>0:
                allusers.add(temp[0])
                
                
        user14wan = set(os.listdir(r'E:/dataset/tweets/'))       
        user13wan=user14wan & allusers
        
        print len(allusers),len(user14wan),len(user14wan & allusers)
        spamset = spamset & user13wan
        print 'spamset loaded! '   
        del allusers 
        del user14wan
         
         
        follow={}
        follower={} 
        for line in fnetwork:
            count +=1
            if count %100000 ==0:
                print count,len(userset)
            temp = line.strip().split()
            if temp[0] in spamset or temp[1] in spamset:
                userset.update(temp)  
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
                    
        nofollow = set(follower.keys())-set(follow.keys())
        nofollower = set(follow.keys())-set(follower.keys())
        while 1:  
            flag = 0;  
            for key in follow.keys():
                for item in follow[key]:
                    if item in nofollower:
                        follow[key].remove(item)
            for key in follow.keys():
                if len(follow[key])<1:
                    flag = 1
                    nofollow.add(key)
                    del follow[key]
            if flag == 0 :
                break 
            
            
        print 'small network loaded!'
        
        
        
        
        count = 0
        for line in fshare:
            count +=1
            if count %100000 ==0:
                print count,len(usershare)
            temp = line.strip().split()
            if temp[0] in spamset or temp[1] in spamset:
                usershare.update(temp[0:2])     
        
        userlast=userset & usershare 
         
         
    #finally:
        #print 'user:\t'+str(usercount),uid
       # temp.close()
        print 'spamset loaded!',len(spamset)
        print 'small network loaded!',len(userset),len(userset &spamset)
        print 'url-shared network loaded!',len(usershare),len(usershare &spamset)
        print 'last user!',len(userlast),len(userlast &spamset)
        fnetwork.close()
        fshare.close()
        fspam.close()
     






if __name__=='__main__':
    run()