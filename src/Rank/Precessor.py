'''
Created on 2014-3-20

@author: Administrator
'''
from sklearn import preprocessing as pre
import numpy as np

loglist = [5,6,12,13,14,19,20,21]

def loadfeature(filename):
    file = open(filename,'r')
    usernames={}
    userfeature=[]
    count = 0
    #fout = open('../../../sssddata/14wan/feature/pre_metric.txt','w')
    try:

        while 1:
            line = file.readline()
            if line =='':
                break
            temp = line.strip().split()
            usernames[temp[0]]=count
            temp = temp[1:len(temp)-1]
            #temp = [float(temp[x]) for x in range(2,6) ]
            for x in range(0,len(temp)):
                temp[x]=float(temp[x])
                if x in loglist:
                    temp[x] = np.log(temp[x]+1)
            userfeature.append(temp) 
            
            #userfeature[count].append((float(temp[2])+1)/(float(temp[3])+1))    
            count+=1
    except   Exception,e:
        print Exception,e
        print count
    file.close()
    print count
    X_train = np.array(userfeature)
    #print X_train
    min_max_scaler = pre.MinMaxScaler()
    userfeature = min_max_scaler.fit_transform(X_train)   
    print 'precess loadfeature!',len(usernames.keys())
    #print userfeature
    return usernames,userfeature

def getLabel(filename,mode=0):
    file = open(filename,'r')
    userID=[]
    
    userLabel={}
    ###userLabel={userID:Label}
    while 1:
        line = file.readline()
        if line =='':
            break
        temp = line.strip().split()
        userID.append(temp[0])
        if mode == 0:
            userLabel[temp[0]]=int(temp[2])
        else :
            if temp[1]=='spam':
                userLabel[temp[0]]=1
            else:
                userLabel[temp[0]]=0
    print 'precess getLabel!'
    return userLabel

def getTrainset(userfeature,usernames,userLabel):
    trainset={}
    for userid in userLabel.keys():
        #print userid,usernames[userid]
        trainset[userid] = userfeature[usernames[userid]]
       # print trainset[userid]
    print 'precess getTrainset!'
    return trainset

def getallLabel(fname,spam=True):
    file = open(fname,'r')
    userID=[]  
    userLabel={}
    for line in file:
        temp = line.strip().split()
        if spam:
            if temp[len(temp)-1]=="Y":
                userLabel[temp[0]] = 1
            else :
                userLabel[temp[0]] = 0
        else:
            if temp[len(temp)-1]=="Y":
                userLabel[temp[0]] = 0
            else :
                userLabel[temp[0]] = 1
    print 'precess getLabel!'
    return userLabel
        

if __name__ == '__main__':
    usermap,userfeature=loadfeature('../../../sssddata/14wan/feature/13wan-metric.txt')
    userLabel = getallLabel('../../../sssddata/14wan/feature/13wan-metric.txt')
    Trainset = getTrainset(userfeature, usermap, userLabel)
    #usermap,userfeature=loadfeature('../../../sssddata/spamleusers.txt')
    pass