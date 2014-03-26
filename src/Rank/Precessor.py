'''
Created on 2014-3-20

@author: Administrator
'''
from sklearn import preprocessing as pre
import numpy as np

def loadfeature(filename):
    file = open(filename,'r')
    usernames={}
    userfeature=[]
    count = 0
    try:
        min_max_scaler = pre.MinMaxScaler()
        while 1:
            line = file.readline()
            if line =='':
                break
            temp = line.strip().split()
            usernames[temp[0]]=count
            temp = [float(temp[x]) for x in range(2,6) ]
            for x in range(0,len(temp)):
                if temp[x]==0.0:
                    temp[x] += 1.0
            userfeature.append(temp) 
            userfeature[count].append((float(temp[2])+1)/(float(temp[3])+1))    
            count+=1
    except   Exception,e:
        print Exception,e
        print count
    file.close()
    print count
    X_train = np.log(np.array(userfeature))
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
    

if __name__ == '__main__':
    usermap,userfeature=loadfeature('../../../sssddata/sampleusers.txt')
    userLabel = getLabel('../../../sssddata/finalseeds2.txt',1)
    Trainset = getTrainset(userfeature, usermap, userLabel)
    #usermap,userfeature=loadfeature('../../../sssddata/spamleusers.txt')
    pass