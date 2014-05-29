# -*- coding: utf-8 -*-
'''
Created on 2014-4-11

@author: Administrator
'''
import sys, os
import cPickle as pickle 


def run():
    try:
        
        count=0
        userset=set()
        outfspam = open(r'../../../sssddata/14wan/14spamsuspend','rb')
        spamset =pickle.load(outfspam)
        print len(spamset)
        usernet = {}
        usershare =set()
        fspam = open(r'../../../sssddata/14wan/14wanlabel-spam.txt','r')
        
        allusers=set()
        fuser = open(r'../../../sssddata/users.txt','r')
        for line in fuser:
            temp = line.strip().split()
            if len(temp)>0:
                allusers.add(temp[0])
        fuser.close()        

        #做交集        
        user14wan = set(os.listdir(r'E:/dataset/tweets/'))       
        user13wan=user14wan & allusers 
        print len(allusers),len(user14wan),len(user14wan & allusers)
        spamset = spamset & user13wan
        ffinal = open('../../../sssddata/14wan/1wan/spamset','wb')
        pickle.dump(spamset,ffinal, protocol=0)
        ffinal.close()
        print 'spamset loaded! '   
        del allusers 
        del user14wan
        
        
        #加载大网络
        follow={}
        follower={} 
        fnetwork=open(r'../../../sssddata/14wan/newnetworks','r')#网络文件
        fsmallnet = open(r'../../../sssddata/14wan/1-smallnet.txt','w')#输出文件
        for line in fnetwork:
            count +=1
            if count %100000 ==0:
                print count,len(userset)
            temp = line.strip().split()
            # 只要关系中有一个是spam，将两个用户加到用户候选集合userset中
            if temp[0] in spamset or temp[1] in spamset:
                if temp[0] in user13wan and temp[1] in user13wan:
                    userset.update(temp)        
        print len(userset)
        userset &= user13wan
        #重新扫描网络，将关系中两个都在userset中的关系提取到新文件中 
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
        biouser = set(follower.keys())&set(follow.keys()) &user13wan
        print 'bio user',len(userset),len(biouser) 
         
        
        # 提取profile
        #=======================================================================
        # fuser = open(r'../../../sssddata/users.txt','r')
        # fusersmall = open(r'../../../sssddata/14wan/user_smallnet.txt','w')
        # for line in fuser:
        #     temp = line.strip().split()
        #     if len(temp)>0:
        #         if temp[0] in userset:
        #             fusersmall.write(line)
        # fusersmall.close()
        # fuser.close() 
        #=======================================================================
        
        fuserset = open('../../../sssddata/14wan/1-smallnet_userset','wb')
        pickle.dump(userset,fuserset, protocol=0)
        fuserset.close()

        #去叶子节点，即度为1的节点
        #=======================================================================
        # while 1:
        #     follower.clear()
        #     follow.clear()
        #     fnetwork.seek(0)
        #     for line in fnetwork:
        #         count +=1
        #         temp = line.strip().split()
        #         if temp[0] in biouser and temp[1] in biouser:
        #             userset.update(temp)  
        #             try:
        #                 follow[temp[0]].add(temp[1])
        #             except:
        #                 follow[temp[0]]=set()    
        #                 follow[temp[0]].add(temp[1])  
        #             try:
        #                 follower[temp[1]].add(temp[0])
        #             except:
        #                 follower[temp[1]]=set()         
        #                 follower[temp[1]].add(temp[0]) 
        #     biouser = set(follower.keys())&set(follow.keys())
        #     print 'bio user',len(biouser),len(follow.keys()),len(follower.keys())  
        #     if len(biouser)==len(follow.keys()) and len(biouser)==len(follower.keys()):
        #         break     
        # spamset = biouser & spamset
        # print 'last users:',len(biouser),len(spamset)
        # #输出新的网络
        # foutnet = open(r'../../../sssddata/14wan/1-outnet.txt','w')
        # finnet = open(r'../../../sssddata/14wan/1-innet.txt','w')
        # for user in follow.keys():
        #     foutnet.write(user+'\t'+'\t'.join(list(follow[user]))+'\n')
        # for user in follower.keys():
        #     finnet.write(user+'\t'+'\t'.join(list(follower[user]))+'\n')
        # foutnet.close()
        # finnet.close()
        #=======================================================================
        
        
        #=======================================================================
        # ffinal = open('../../../sssddata/14wan/1wan/spamset_lastuser','wb')
        # pickle.dump(spamset,ffinal, protocol=0)
        # pickle.dump(biouser,ffinal, protocol=0)
        # ffinal.close()
        #=======================================================================
        
        
        #对网络进行统计
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
        for it in nfollow:
             try:
                 dictout[it] +=1
             except:
                 dictout[it]=1
        for key in dictout.keys():
             fn.write(str(key)+'\t'+str(dictout[key])+'\n')
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
        
        
        
        
        #=======================================================================
        # fshare = open(r'../../../sssddata/14wan/14wanurlshare.txt','r')
        # count = 0
        # for line in fshare:
        #     count +=1
        #     #if count %100000 ==0:
        #        # print count,len(usershare)
        #     temp = line.strip().split()
        #     if temp[0] in spamset or temp[1] in spamset:
        #         usershare.update(temp[0:2])     
        #  
        # userlast=biouser & usershare 
        # fshare.close()
        #=======================================================================
        #print 'last user!',len(userlast),len(userlast &spamset) 
        #print 'url-shared network loaded!',len(usershare),len(usershare &spamset) 
    finally:
        #print 'user:\t'+str(usercount),uid
       # temp.close()
        #print 'small network loaded!',len(userset),len(userset &spamset)
        
        
        fnetwork.close()
       
        fspam.close()
        
     






if __name__=='__main__':
    run()
