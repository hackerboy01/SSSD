'''
Created on 2013-12-24

@author: Administrator
'''
import os,sys

def cur_file_dir():
    
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

def run():
    infile = open(r'E:\dataset\UDI-TwitterCrawl-Aug2012-Network\network.txt','r')
   # print os.chdir('..')
    infile2 = open(r'..\..\..\sssddata\spamprofile.txt','r')
    infile4 = open('../../../sssddata/users.txt','r')
    infile3 = open(r'..\..\..\sssddata\normalprofile.txt','r')
    outfile = open('../../../sssddata/following2.txt','w')
    outfile1 = open('../../../sssddata/samplerelation.txt','w')
    outfile2 = open('../../../sssddata/sampleusers.txt','w')
    outfile3 = open('../../../sssddata/follower2.txt','w')
    outfile4 = open('../../../sssddata/finalseeds2.txt','w')
    #infile1 = ('','r')
    users = set()
    goodseeds=set()
    badseeds=set()
    while 1:
        line = infile2.readline()
        if line == '':
            break
        temp = line.strip().split()
        if len(temp)>1:
            users.add(str(temp[0]))
            badseeds.add(str(temp[0]))
    print "Already read spamuser"        
    
    while 1:
        line = infile3.readline()
        if line == '':
            break
        temp = line.strip().split()
        if len(temp)>1:
            users.add(str(temp[0]))
            goodseeds.add(str(temp[0]))
    print "Already read normaluser"  
    print len(users)  
    
    testusers = set()
    while 1:
        line = infile4.readline()
        if line == '':
            break
        temp = line.strip().split()
        if len(temp)>1:
            testusers.add(str(temp[0]))
    print "Already read testuser" 
    
    filelist = set(os.listdir(r'E:\dataset\tweets'))
    
    print "Already read filelist"
    
    sampleusers = set(users)
    #sampleusers.add(users)
    follow = {}
    follower = {}
    count = 0
    usercount = len(users)
    try:
        while 1:
            if count%1000000==0:
                print count, len(sampleusers),len(users)
            count += 1
            line = infile.readline()
            if line=='':
                break
            temp = line.strip().split()
            if temp[0] in users and (temp[1]) in testusers and temp[1] in filelist:
                if temp[1] not in sampleusers:
                    sampleusers.add(str(temp[1]))           

                
        infile.seek(0)
        count = 0
        while 1:
            if count%1000000==0:
                print count,len(follow.keys()),len(follower.keys())
            count += 1
            line = infile.readline()
            if line=='':
                break
            temp = line.strip().split()
            
            if temp[0] in sampleusers and temp[1] in sampleusers:
                try:
                    outfile1.write(str(temp[0])+'\t'+str(temp[1])+'\n')
                    follow[temp[0]].append(temp[1])
                except:
                    follow[temp[0]]=[]          
                    follow[temp[0]].append(temp[1])
                    
                try:
#                     outfile3.write(str(temp[1])+'\t'+str(temp[0])+'\n')
                    follower[temp[1]].append(temp[0])
                except:
                    follower[temp[1]]=[]          
                    follower[temp[1]].append(temp[0])
        restfollow = sampleusers - set(follow.keys())
        restfollower = sampleusers -set(follower.keys()) 
        while 1:  
            flag = 0;  
            for key in follow.keys():
                for item in follow[key]:
                    if item in restfollow:
                        follow[key].remove(item)
            for key in follow.keys():
                if len(follow[key])<1:
                    flag = 1
                    restfollow.add(key)
                    del follow[key]
            if flag == 0 :
                break
        print 'The number of node whose outdegree is bigger than 0:',len(follow.keys())
        while 1:  
            flag = 0;  
            for key in follower.keys():
                for item in follower[key]:
                    if item in restfollower:
                        follower[key].remove(item)
            for key in follower.keys():
                if len(follower[key])<1:
                    flag = 1
                    restfollower.add(key)
                    del follower[key]
    #                 print len(follower.keys())
            if flag == 0 :
                break
        print 'The number of node whose indegree is bigger than 0:',len(follower.keys())     
        finaluser = set(follow.keys()) & set(follower.keys()) 
        print 'The number of final users:',len(finaluser)
        finalgoodseeds = finaluser & goodseeds
        finalbadseeds = finaluser & badseeds   
          
        for key in follow.keys():
            if key in finaluser:
                outfile.write(key+'\t'+' '.join(follow[key])+'\n')
        for key in follower.keys():
            if key in finaluser:
                outfile3.write(key+'\t'+' '.join(follower[key])+'\n')    
                
                
        infile4.seek(0)
        while 1:
            line = infile4.readline()
            if line == '':
                break
            temp = line.strip().split()
            if len(temp)>1:
                if temp[0] in finaluser:
                    outfile2.write(line)
                if temp[0] in finalgoodseeds:
                    outfile4.write(temp[0]+'\tgood\n')
                if temp[0] in finalbadseeds:
                    outfile4.write(temp[0]+'\tspam\n')
        print "Already read testuser" 
        
    finally:
        outfile.close()
        outfile1.close()
        outfile2.close()
        outfile3.close()
        outfile4.close()
        #print len(follow.keys())
        infile2.close()
        infile4.close()
        infile3.close()
        infile.close()

if __name__ == '__main__':
    run()