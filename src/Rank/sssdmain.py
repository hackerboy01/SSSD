'''
Created on 2014-3-20

@author: Administrator
'''
import Precessor as pre
import pagerank as PR
import Classifier


if __name__ == '__main__':
    #load features of all users including training set. username[i] corresponding feature userfeature[i]
    usermap,userfeature=pre.loadfeature('../../../sssddata/spamleusers.txt')
    #userLabel={userID:Label}
    userLabel = pre.getLabel('../../../sssddata/finalseeds2.txt',1)
    outnet,innet =PR.loadnet1('../../../sssddata/following2.txt','../../../sssddata/follower2.txt')
    users = usermap.keys()

    Trainset = pre.getTrainset(userfeature, usermap, userLabel)
    c = Classifier.Classifier('svm')
    
    goodseeds= [x for x in userLabel.keys() if userLabel[x]==0]
    badseeds= [x for x in userLabel.keys() if userLabel[x]==1]
    pGood = PR.PageRank(goodseeds,outnet,innet,users)
    pBad = PR.PageRank(badseeds,innet,outnet,users)
    
    
    
    

    goodeta = 0.02
    badeta = 0.02
    goodclass = 0.5
    badclass = 0.5
    
    trainedset=set()
    trainedset= trainedset | set(userLabel.keys())
    c.addtrainset(Trainset,userLabel)
    print 'Trainset' ,len(c.trainset)
    c.Training()
    count = 0
    while 1: 
        count += 1    
        print 'Iteration ',count
        Labelset={}
        temptrainset={}
        
        pGood.initRank(goodseeds)
        pGood.run(60) 
        pGood.orderRank()     
        tempgood = [ pGood.order[x][0] for x in range(0,int(goodeta*len(pGood.order))) if pGood.order[x][0] not in trainedset ]
        #print [ userfeature[usermap[tempgood[x]]] for x in range(0,len(tempgood)) ]
        tempclass = c.Predict([ userfeature[usermap[tempgood[x]]] for x in range(0,len(tempgood)) ])
        goodcount=0
        for x in range(0,len(tempclass)):
            if tempclass[x] <  goodclass:
                Labelset[tempgood[x]]=0
                temptrainset[tempgood[x]]=userfeature[usermap[tempgood[x]]]
                goodseeds.append(tempgood[x])
                goodcount+=1
                
        print 'Temp good user %d, add good seeds %d' %(len(tempgood),goodcount)
        
        pBad.initRank(badseeds)
        pBad.run(60)
        pBad.orderRank()
        tempbad = [ pBad.order[x][0] for x in range(0,int(badeta*len(pBad.order))) if pBad.order[x][0] not in trainedset]
        tempclass = c.Predict([ userfeature[usermap[tempbad[x]]] for x in range(0,len(tempbad)) ])
        badcount = 0
        for x in range(0,len(tempclass)):
            if tempclass[x] >  badclass:
                Labelset[tempbad[x]]=0
                temptrainset[tempbad[x]]=userfeature[usermap[tempbad[x]]]
                badseeds.append(tempgood[x])
                badcount += 1
        print 'Temp bad user %d, add bad seeds %d' %(len(tempbad),badcount)
        goodeta += 0.01
        badeta += 0.01
        c.addtrainset(temptrainset,Labelset)
        trainedset = trainedset | set(Labelset.keys())
        print 'Trainset' ,len(c.trainset),len(trainedset)
        c.Training()
        if goodeta >0.4:
            print 'done'
            break
        
        
        
        
        
        
        
        