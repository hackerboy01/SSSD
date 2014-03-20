'''
Created on 2014-3-20

@author: Administrator
'''
from sklearn import preprocessing as pre
import numpy as np

def loadfeature(filename):
    file = open(filename,'r')
    #userLabel = getLabel('../../../sssddata/finalseeds2.txt')
   # outfile = open('../../../sssddata/finalseeds.txt','w')
    usernames={}
    userfeature=[]
    count = 0
    while 1:
        line = file.readline()
        if line =='':
            break
        temp = line.strip().split()
        userfeature.append([float(temp[x]) for x in range(2,6)]) 
        userfeature[count].append((float(temp[2])+1)/(float(temp[3])+1))
        #if temp[0] in userLabel.keys():
        #    outfile.write(str(temp[0])+'\t'+str(temp[1])+'\t'+str(userLabel[temp[0]])+'\n')
        #print userfeature[count],count
        usernames[temp[0]]=count
        count+=1
    file.close()
    #outfile.close()
    X_train = np.array(userfeature)
    min_max_scaler = pre.MinMaxScaler()
    userfeature = min_max_scaler.fit_transform(X_train)
    #userfeature = pre.normalize(userfeature,norm='l1',axis=0)
    #for x in range(0,len(userfeature)):
    #    print userfeature[x]     
    print 'precess loadfeature!'
    return usernames,userfeature

def getLabel(filename):
    file = open(filename,'r')
    userID=[]
    
    userLabel={}
    #userLabel={userID:Label}
    while 1:
        line = file.readline()
        if line =='':
            break
        temp = line.strip().split()
        userID.append(temp[0])
        #print temp
        userLabel[temp[0]]=int(temp[2])
        #if temp[1]=='spam':
        #    userLabel[temp[0]]=1
        #else:
         #   userLabel[temp[0]]=0
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
    loadfeature('../../../sssddata/sampleusers.txt')
    pass