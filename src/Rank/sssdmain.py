'''
Created on 2014-3-20

@author: Administrator
'''
import Precessor as pre
import pagerank as PR
import Classifier


if __name__ == '__main__':
    #load features of all users including training set. username[i] corresponding feature userfeature[i]
    usermap,userfeature=pre.loadfeature('../../../sssddata/sampleusers.txt')
    #userLabel={userID:Label}
    userLabel = pre.getLabel('../../../sssddata/finalseeds.txt',0)
    outnet,innet =PR.loadnet1('../../../sssddata/following2.txt','../../../sssddata/follower2.txt')
    users = usermap.keys()

    outfile = open('../../../sssddata/Label.txt','w')


    Trainset = pre.getTrainset(userfeature, usermap, userLabel)
    c = Classifier.Classifier('svm')
    
    goodseeds= [x for x in userLabel.keys() if userLabel[x]==0]
    
    badseeds= [x for x in userLabel.keys() if userLabel[x]==1]
    print len(goodseeds),len(badseeds)
    pGood = PR.PageRank(outnet,innet,users)
    pBad = PR.PageRank(innet,outnet,users)

    goodeta = 0.02
    badeta = 0.01
    goodclass = 0.5
    badclass = 0.5
    
    trainedset=set()
    trainedset= trainedset | set(userLabel.keys())
    c.addtrainset(Trainset,userLabel)
    print 'Trainset' ,len(c.trainset)
    c.Training()
    count = 0
    try:
        while 1: 
            count += 1    
            print 'Iteration ',count
            Labelset={}
            temptrainset={}
            
           ##deal with good
            pGood.initRank(goodseeds)
            pGood.run(60) 
            pGood.orderRank()   
            pBad.initRank(badseeds)
            pBad.run(60)
            pBad.orderRank()  
            
            tempgood = [ pGood.order[x][0] for x in range(0,int(goodeta*len(pGood.order))) if pGood.order[x][0] not in trainedset ]
            tempclass = c.Predict([ userfeature[usermap[tempgood[x]]] for x in range(0,len(tempgood)) ])
            goodcount=0
            for x in range(0,len(tempclass)):
                if tempclass[x] <  goodclass:
                    #add trainset
                    Labelset[tempgood[x]]=0
                    temptrainset[tempgood[x]]=userfeature[usermap[tempgood[x]]]
                    #add seeds
                    goodseeds.append(tempgood[x])
                    goodcount+=1      
            print 'Temp good user %d, add good seeds %d' %(len(tempgood),goodcount)
            
            #deal with bad
            tempbad = [ pBad.order[x][0] for x in range(0,int(badeta*len(pBad.order))) if pBad.order[x][0] not in trainedset]
            tempclass = c.Predict([ userfeature[usermap[tempbad[x]]] for x in range(0,len(tempbad)) ])
            badcount = 0
            for x in range(0,len(tempclass)):
                if tempclass[x] >  badclass:
                    Labelset[tempbad[x]]=1
                    temptrainset[tempbad[x]]=userfeature[usermap[tempbad[x]]]
                    badseeds.append(tempbad[x])
                    badcount += 1
            print 'Temp bad user %d, add bad seeds %d' %(len(tempbad),badcount)
            
            
            goodeta += 0.02
            badeta += 0.01
            c.addtrainset(temptrainset,Labelset)
            for u in Labelset.keys():
                outfile.write(str(u)+'\t'+str(Labelset[u])+'\n')
            trainedset = trainedset | set(Labelset.keys())
            print 'Trainset' ,len(c.trainset),len(trainedset)
            c.Training()
            if badeta >0.2:
                print 'done'
                break
   
        
        test = [ u for u in usermap.keys() if u not in trainedset ]
        testclass =  c.Predict([ userfeature[usermap[test[x]]] for x in range(0,len(test)) ])
        for x in range(0,len(test)):
            if testclass[x] < goodclass:
                outfile.write(str(test[x])+'\t0\n')
            if testclass[x] > badclass:
                outfile.write(str(test[x])+'\t1\n')   
    except:
        pass
    finally:
        outfile.close()   
        
        
        
        
        
        