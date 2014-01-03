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
    outfile = open('../../../sssddata/following.txt','w')
    outfile1 = open('../../../sssddata/samplerelation.txt','w')
    outfile2 = open('../../../sssddata/spamleusers.txt','w')
    #infile1 = ('','r')
    users = set()
    while 1:
        line = infile2.readline()
        if line == '':
            break
        temp = line.strip().split()
        if len(temp)>1:
            users.add(str(temp[0]))
    print "Already read spamuser"        
    
    while 1:
        line = infile3.readline()
        if line == '':
            break
        temp = line.strip().split()
        if len(temp)>1:
            users.add(str(temp[0]))
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
#                 if (temp[1]) in users and (temp[0]) in testusers and temp[0] in filelist:
#                     if temp[0] not in sampleusers:
#                         sampleusers.add(int(temp[0]))        
#                         follow[temp[0]].append(temp[1])
                
        infile.seek(0)
        count = 0
        while 1:
            if count%1000000==0:
                print count,len(follow.keys())
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
        for key in follow.keys():
            outfile.write(key+'\t'+' '.join(follow[key])+'\n')
            
        infile4.seek(0)
        while 1:
            line = infile4.readline()
            if line == '':
                break
            temp = line.strip().split()
            if len(temp)>1:
                if temp[0] in follow.keys():
                    outfile2.write(line)
        print "Already read testuser" 
        
    finally:
        outfile.close()
        outfile1.close()
        #print len(follow.keys())
        infile2.close()
        infile4.close()
        infile3.close()
        infile.close()

if __name__ == '__main__':
    run()