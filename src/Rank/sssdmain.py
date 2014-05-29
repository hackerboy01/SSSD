# -*- coding: utf-8 -*-
'''
Created on 2014-3-20

@author: Administrator
'''
import Precessor as pre
import pagerank as PR
import Classifier
import pickle


def runsssd():
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

   
    
    trainedset=set()
    trainedset= trainedset | set(userLabel.keys())
    c.addtrainset(Trainset,userLabel)
    print 'Trainset' ,len(c.trainset)
    c.TrainingB()
    count = 0
    
    ratio = float(c.spam)/c.normal
    goodeta = 0.2
    badeta = goodeta*ratio
    goodclass = 0.5
    badclass = 0.5
    
    
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
            
            tgood = [ pGood.order[x][0] for x in range(0,int(goodeta*len(pGood.order))) if pGood.order[x][0] not in trainedset ]
            tbad = [ pBad.order[x][0] for x in range(0,int(badeta*len(pBad.order))) if pBad.order[x][0] not in trainedset]
            tempgood = list(set(tgood)-set(tbad))
            tempbad = list(set(tbad)-set(tgood))
            
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
           # tempbad = [ pBad.order[x][0] for x in range(0,int(badeta*len(pBad.order))) if pBad.order[x][0] not in trainedset]
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
            badeta += 0.02*ratio
            c.addtrainset(temptrainset,Labelset)
            for u in Labelset.keys():
                outfile.write(str(u)+'\t'+str(Labelset[u])+'\n')
            trainedset = trainedset | set(Labelset.keys())
            print 'Trainset' ,len(c.trainset),len(trainedset)
            c.TrainingB()
            if badeta >0.5:
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
def runsssd2():
    usermap,userfeature=pre.loadfeature('../../../sssddata/14wan/feature/13wan-metric.txt')
    userLabel = pre.getallLabel('../../../sssddata/14wan/feature/13wan-metric.txt')
    outfile = open('../../../sssddata/14wan/predict.txt','w')
    fin = open('../../../sssddata/14wan/newspam_4times','rb')
    newspam = pickle.load(fin)
    fin.close()
    
    fbad = open('../../../sssddata/14wan/spamset_bio','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    
    netname = '1-smallnet-bio.txt'

    #初始化rank模型、种子
    pr=PR.PageRank(rankname='reversPR')
    pr.initNet('../../../sssddata/14wan/rank/'+netname,reverse=True)
    pr.initRank(spamset)
    pr.run(100, good=1.0, TrustRank=False)
    order = pr.orderRank()
    
    ratioT = 4
    Trainset = {}
    spamseeds = 400
    badseeds=[]
    badcount = 0
    spamcount = 0
    for item in order:
        user, score = item
        if user in spamset:
            
            if spamcount ==spamseeds:
                break
            Trainset[user] = userfeature[usermap[user]]
            badseeds.append(user)
            spamcount += 1
            badcount += 1
            
            
    goodseeds=[]
    goodcount = 0
    base_goodseeds = ratioT*spamcount
    for item in order:
        user, score = item
        if user not in spamset and user not in newspam and goodcount < base_goodseeds:
            Trainset[user] = userfeature[usermap[user]]
            goodseeds.append(user)
            goodcount += 1
    print len(goodseeds),len(badseeds)        
   
    pGood = PR.PageRank(rankname='TrustRank') 
    pGood.initNet('../../../sssddata/14wan/rank/'+netname,reverse=False)
    pBad = PR.PageRank(rankname='AntiRank')
    pBad.initNet('../../../sssddata/14wan/rank/'+netname,reverse=True)
    #初始化训练集、分类器
    c = Classifier.Classifier('forest')
    trainedset=set()
    trainedset= trainedset | set(Trainset.keys())
    c.addtrainset(Trainset,userLabel)
    print 'Trainset' ,len(c.trainset)
    c.Training()
    
    #一些参数
    count = 0
    ratio = float(c.spam)/c.normal
    goodeta = 0.1
    badeta = goodeta*ratio
    goodclass = 0.5
    badclass = 0.5
    
    #测试参数
    
    try:
        while 1: 
            count += 1    
            print 'Iteration ',count
            Labelset={}
            temptrainset={}
            
            ##deal with good
            pGood.initRank(goodseeds)
            pGood.run(100, good=1.0, TrustRank=True) 
            pGood.orderRank()   
            pBad.initRank(badseeds)
            pBad.run(100, good=1.0, TrustRank=False)
            
            for user in pBad.Rank.keys():
                    #spamrank[user]=float(antiRank[user])/float(trustRank[user])
                    pBad.Rank[user]=float(pBad.Rank[user])-float(pGood.Rank[user])
                    #print pBad.Rank[user]
                    #print antiRank[user],trustRank[user],spamrank[user]
            pBad.orderRank()    
            
            
            
            
            tgood = [ pGood.order[x][0] for x in range(0,int(goodeta*len(pGood.order))) if pGood.order[x][0] not in trainedset ]
            tbad = [ pBad.order[x][0] for x in range(0,int(badeta*len(pBad.order))) if pBad.order[x][0] not in trainedset]
            tempgood = list(set(tgood)-set(tbad))
            tempbad = list(set(tbad)-set(tgood))
            
            tempclass = c.Predict([ userfeature[usermap[tempgood[x]]] for x in range(0,len(tempgood)) ])
            goodcount=0
            
            labelgood=[]
            for x in range(0,len(tempclass)):
                if tempclass[x] <  goodclass:
                    ## add trainset
                    labelgood.append(tempgood[x])
                    Labelset[tempgood[x]]=0
                    temptrainset[tempgood[x]]=userfeature[usermap[tempgood[x]]]
                    ## add seeds
                    goodseeds.append(tempgood[x])
                    goodcount+=1 

            print 'Temp good user %d, add good seeds %d' %(len(tempgood),goodcount)
            
            #deal with bad
           # tempbad = [ pBad.order[x][0] for x in range(0,int(badeta*len(pBad.order))) if pBad.order[x][0] not in trainedset]
            tempclass = c.Predict([ userfeature[usermap[tempbad[x]]] for x in range(0,len(tempbad)) ])
            badcount = 0
            labelbad=[]
            for x in range(0,len(tempclass)):
                if tempclass[x] >  badclass:
                    labelbad.append(tempbad[x])
                    Labelset[tempbad[x]]=1
                    temptrainset[tempbad[x]]=userfeature[usermap[tempbad[x]]]
                    badseeds.append(tempbad[x])
                    badcount += 1
            print 'Temp bad user %d, add bad seeds %d' %(len(tempbad),badcount)
            
            
            
            
            goodeta += 0.1
            badeta += 0.1*ratio
            c.addtrainset(temptrainset,Labelset)
            #===================================================================
            # for u in Labelset.keys():
            #     outfile.write(str(u)+'\t'+str(Labelset[u])+'\n')
            #===================================================================
            trainedset = trainedset | set(Labelset.keys())
            print 'Trainset' ,len(c.trainset)
            c.Training()
            if badeta >0.3:
                print 'done'
                break
   
        
       
    except:
        pass
    finally:
       # outfile.close()  
        test = [ u for u in usermap.keys() if u not in trainedset ]
        
        testall = len(test)
        print '测试集:',testall
        testgood = 0
        testgoodr = 0
        testgoodw = 0
        testbad = 0
        testbadr = 0
        testbadw = 0
        testbadall = 0 #测试集中有多少个spam
        testclass =  c.Predict([ userfeature[usermap[test[x]]] for x in range(0,len(test)) ])
        for x in range(0,len(test)):
            if test[x] in newspam or test[x] in spamset:
                testbadall += 1
            if testclass[x] < goodclass:
                if test[x] in newspam or test[x] in spamset:
                    testbadw += 1
                else:
                    testgoodr += 1
                testgood += 1
            if testclass[x] > badclass:
                if test[x] in newspam or test[x] in spamset:
                    testbadr += 1
                else:
                    testgoodw += 1
                testbad += 1 
        print 'spam准确率:', float(testbadr)/testbad,testbadr,testbad
        print 'spam召回率:', float(testbadr)/testbadall,testbadr,testbadall
        print 'normal准确率', float(testgoodr)/testgood,testgoodr,testgood
        print 'normal召回率', float(testgoodr)/(testall-testbadall), testgoodr,(testall-testbadall)
        pass
def runsssd3():
    usermap,userfeature=pre.loadfeature('../../../sssddata/14wan/feature/13wan-metric.txt')
    userLabel = pre.getallLabel('../../../sssddata/14wan/feature/13wan-metric.txt')
    outfile = open('../../../sssddata/14wan/predict.txt','w')
   # fin = open('../../../sssddata/14wan/newspam_3times_tree&svm','rb')
    fin = open('../../../sssddata/14wan/newspam_3times','rb')
    newspam = pickle.load(fin)
    fin.close()
    
    fbad = open('../../../sssddata/14wan/spamset_bio','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    
    netname = '1-smallnet-bio.txt'

    #初始化rank模型、种子
    pr=PR.PageRank(rankname='reversPR')
    pr.initNet('../../../sssddata/14wan/rank/'+netname,reverse=True)
    pr.initRank(spamset)
    pr.run(100, good=1.0, TrustRank=False)
    order = pr.orderRank()
    
    ratioT = 4
    Trainset = {}
    spamseeds = 400
    badseeds=[]
    badcount = 0
    spamcount = 0
    for item in order:
        user, score = item
        if user in spamset:
            
            if spamcount ==spamseeds:
                break
            Trainset[user] = userfeature[usermap[user]]
            badseeds.append(user)
            spamcount += 1
            badcount += 1
            
            
    goodseeds=[]
    goodcount = 0
    base_goodseeds = ratioT*spamcount
    for item in order:
        user, score = item
        if user not in spamset and user not in newspam and goodcount < base_goodseeds:
            Trainset[user] = userfeature[usermap[user]]
            goodseeds.append(user)
            goodcount += 1
    print len(goodseeds),len(badseeds)        
   
    pGood = PR.PageRank(rankname='TrustRank') 
    pGood.initNet('../../../sssddata/14wan/rank/'+netname,reverse=False)
    pBad = PR.PageRank(rankname='AntiRank')
    pBad.initNet('../../../sssddata/14wan/rank/'+netname,reverse=True)
    #初始化训练集、分类器
    c = Classifier.Classifier('svm')
    trainedset=set()
    trainedset= trainedset | set(Trainset.keys())
    c.addtrainset(Trainset,userLabel)
    print 'Trainset' ,len(c.trainset)
    c.Training()
    
    #一些参数
    count = 0
    ratio = float(c.spam)/c.normal
    goodeta = 0.1
    badeta = goodeta*ratio
    goodclass = 0.5
    badclass = 0.5
    
    #测试参数
    
    try:
        while 1: 
            count += 1    
            print 'Iteration ',count
            Labelset={}
            temptrainset={}
            
            ##deal with good
            pGood.initRank(goodseeds)
            pGood.run(100, good=1.0, TrustRank=True) 
            pGood.orderRank()   
            pBad.initRank(badseeds)
            pBad.run(100, good=1.0, TrustRank=False)
            
            for user in pBad.Rank.keys():
                    #spamrank[user]=float(antiRank[user])/float(trustRank[user])
                    pBad.Rank[user]=float(pBad.Rank[user])-float(pGood.Rank[user])
                    #print pBad.Rank[user]
                    #print antiRank[user],trustRank[user],spamrank[user]
            pBad.orderRank()    
            
            
            
            
            tgood = [ pGood.order[x][0] for x in range(0,int(goodeta*len(pGood.order))) if pGood.order[x][0] not in trainedset ]
            tbad = [ pBad.order[x][0] for x in range(0,int(badeta*len(pBad.order))) if pBad.order[x][0] not in trainedset]
            tempgood = list(set(tgood)-set(tbad))
            tempbad = list(set(tbad)-set(tgood))
            
            tempclass = c.Predict([ userfeature[usermap[tempgood[x]]] for x in range(0,len(tempgood)) ])
            goodcount=0
            
            labelgood=[]
            for x in range(0,len(tempclass)):
                if tempclass[x] <  goodclass:
                    ## add trainset
                    labelgood.append(tempgood[x])
                    #===========================================================
                    # Labelset[tempgood[x]]=0
                    # temptrainset[tempgood[x]]=userfeature[usermap[tempgood[x]]]
                    # ## add seeds
                    # goodseeds.append(tempgood[x])
                    # goodcount+=1 
                    #===========================================================

            #print 'Temp good user %d, add good seeds %d' %(len(tempgood),goodcount)
            
            #deal with bad
           # tempbad = [ pBad.order[x][0] for x in range(0,int(badeta*len(pBad.order))) if pBad.order[x][0] not in trainedset]
            tempclass = c.Predict([ userfeature[usermap[tempbad[x]]] for x in range(0,len(tempbad)) ])
            badcount = 0
            labelbad=[]
            for x in range(0,len(tempclass)):
                if tempclass[x] >  badclass:
                    labelbad.append(tempbad[x])
                    #===========================================================
                    # Labelset[tempbad[x]]=1
                    # temptrainset[tempbad[x]]=userfeature[usermap[tempbad[x]]]
                    # badseeds.append(tempbad[x])
                    # badcount += 1
                    #===========================================================
            #print 'Temp bad user %d, add bad seeds %d' %(len(tempbad),badcount)
            lengood = len(labelgood)
            lenbad = len(labelbad)
            print 'Temp good user %d, Temp bad user %d' %(len(tempgood),len(tempbad))
            print 'Predict: good %d, bad  %d' %(lengood,lenbad)

            if (lenbad * ratioT) < lengood:
                for user in labelbad:
                    Labelset[user]=1
                    temptrainset[user]=userfeature[usermap[user]]
                    badseeds.append(user)
                    badcount+=1
                for x in range(int(lenbad*ratioT)):
                #for x in range(lengood):
                    Labelset[labelgood[x]]=0
                    temptrainset[labelgood[x]]=userfeature[usermap[labelgood[x]]]
                    goodseeds.append(labelgood[x])
                    goodcount+=1 
                   # print x
            else:
                for x in range(int(lengood/ratioT)):
                    Labelset[labelbad[x]]=1
                    temptrainset[labelbad[x]]=userfeature[usermap[labelbad[x]]]
                    badseeds.append(labelbad[x])
                    badcount+=1 
                for x in range(lengood):
                    Labelset[labelgood[x]]=0
                    temptrainset[labelgood[x]]=userfeature[usermap[labelgood[x]]]
                    goodseeds.append(labelgood[x])
                    goodcount+=1 

            print 'Sample: good %d, bad  %d' %(goodcount,badcount)
            goodeta += 0.1
            badeta += 0.1*ratio
            c.addtrainset(temptrainset,Labelset)
            #===================================================================
            # for u in Labelset.keys():
            #     outfile.write(str(u)+'\t'+str(Labelset[u])+'\n')
            #===================================================================
            #trainedset = trainedset | set(Labelset.keys())
            print 'Trainset' ,len(c.trainset)
            c.Training()
            if badeta >0.3:
                print 'done'
                break
   
        
       
    except Exception, e:
        print e
    finally:
       # outfile.close()  
        test = [ u for u in usermap.keys() if u not in trainedset ]
        
        testall = len(test)
        print '测试集:',testall
        testgood = 0
        testgoodr = 0
        testgoodw = 0
        testbad = 0
        testbadr = 0
        testbadw = 0
        testbadall = 0 #测试集中有多少个spam
        testclass =  c.Predict([ userfeature[usermap[test[x]]] for x in range(0,len(test)) ])
        for x in range(0,len(test)):
            if test[x] in newspam or test[x] in spamset:
                testbadall += 1
            if testclass[x] < goodclass:
                if test[x] in newspam or test[x] in spamset:
                    testbadw += 1
                else:
                    testgoodr += 1
                testgood += 1
            if testclass[x] > badclass:
                if test[x] in newspam or test[x] in spamset:
                    testbadr += 1
                else:
                    testgoodw += 1
                testbad += 1 
        print 'spam准确率:', float(testbadr)/testbad,testbadr,testbad
        print 'spam召回率:', float(testbadr)/testbadall,testbadr,testbadall
        print 'normal准确率', float(testgoodr)/testgood,testgoodr,testgood
        print 'normal召回率', float(testgoodr)/(testall-testbadall), testgoodr,(testall-testbadall)
        pass

def runsssd4():
    usermap,userfeature=pre.loadfeature('../../../sssddata/14wan/feature/13wan-metric.txt')
    userLabel = pre.getallLabel('../../../sssddata/14wan/feature/13wan-metric.txt')
    outfile = open('../../../sssddata/14wan/predict.txt','w')
   # fin = open('../../../sssddata/14wan/newspam_3times_tree&svm','rb')
    fin = open('../../../sssddata/14wan/newspam_4times','rb')
    newspam = pickle.load(fin)
    fin.close()
    
    fbad = open('../../../sssddata/14wan/spamset_bio','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    
    netname = '1-smallnet-bio.txt'

    #初始化rank模型、种子
    pr=PR.PageRank(rankname='reversPR')
    pr.initNet('../../../sssddata/14wan/rank/'+netname,reverse=True)
    pr.initRank(spamset)
    pr.run(100, good=1.0, TrustRank=False)
    order = pr.orderRank()
    
    ratioT = 4.2
    Trainset = {}
    spamseeds = 700
    badseeds=[]
    badcount = 0
    spamcount = 0
    for item in order:
        user, score = item
        if user in spamset:
            
            if spamcount ==spamseeds:
                break
            Trainset[user] = userfeature[usermap[user]]
            badseeds.append(user)
            spamcount += 1
            badcount += 1
            
            
    goodseeds=[]
    goodcount = 0
    base_goodseeds = ratioT*spamcount
    for item in order:
        user, score = item
        if user not in spamset and user not in newspam and goodcount < base_goodseeds:
            Trainset[user] = userfeature[usermap[user]]
            goodseeds.append(user)
            goodcount += 1
    print len(goodseeds),len(badseeds)        
   
    pGood = PR.PageRank(rankname='TrustRank') 
    pGood.initNet('../../../sssddata/14wan/rank/'+netname,reverse=False)
    pBad = PR.PageRank(rankname='AntiRank')
    pBad.initNet('../../../sssddata/14wan/rank/'+netname,reverse=True)
    #初始化训练集、分类器
    c = Classifier.Classifier('svm')
    trainedset=set()
    trainedset= trainedset | set(Trainset.keys())
    restset = set(usermap.keys()) - trainedset
    c.addtrainset(Trainset,userLabel)
    print 'Trainset' ,len(c.trainset)
    c.Training()
    
    #一些参数
    count = 0
    ratio = float(c.spam)/c.normal
    goodeta = 0.1
    badeta = goodeta*ratio
    goodclass = 0.5
    badclass = 0.5
    
    #测试参数
    tbadseeds = []
    tgoodseeds = []
    
    try:
        while 1: 
            count += 1    
            print 'Iteration ',count
            Labelset={}
            temptrainset={}
            
            ##deal with good
            pGood.initRank(goodseeds)
            pGood.run(100, good=1.0, TrustRank=True) 
            pGood.orderRank()   
            pBad.initRank(badseeds)
            pBad.run(100, good=1.0, TrustRank=False)
            
            for user in pBad.Rank.keys():
                    #spamrank[user]=float(antiRank[user])/float(trustRank[user])
                    pBad.Rank[user]=float(pBad.Rank[user])-float(pGood.Rank[user])
                    #print pBad.Rank[user]
                    #print antiRank[user],trustRank[user],spamrank[user]
            pBad.orderRank()    
            
            
            
            tgood = [ pGood.order[x][0] for x in range(0,int(goodeta*len(pGood.order))) if pGood.order[x][0] not in trainedset ]
            tbad = [ pBad.order[x][0] for x in range(0,int(badeta*len(pBad.order))) if pBad.order[x][0] not in trainedset]
            tempgood = list(set(tgood)-set(tbad))
            tempbad = list(set(tbad)-set(tgood))
            
            #tempclass = c.Predict([ userfeature[usermap[tempgood[x]]] for x in range(0,len(tempgood)) ])
            goodcount=0
            
            labelgood=[]
            for x in tempgood:
                ctemp = c.Predict(userfeature[usermap[x]])
                if ctemp < goodclass:
                    labelgood.append(x)
            print 'tempclass good'
            #===================================================================
            # for x in range(0,len(tempclass)):
            #     if tempclass[x] <  goodclass:
            #         ## add trainset
            #         labelgood.append(tempgood[x])
            #===================================================================


            #print 'Temp good user %d, add good seeds %d' %(len(tempgood),goodcount)
            
            #deal with bad
           # tempbad = [ pBad.order[x][0] for x in range(0,int(badeta*len(pBad.order))) if pBad.order[x][0] not in trainedset]
            #tempclass = c.Predict([ userfeature[usermap[tempbad[x]]] for x in range(0,len(tempbad)) ])
            
            badcount = 0
            labelbad=[]
            for x in tempbad:
                ctemp = c.Predict(userfeature[usermap[x]])
                if ctemp > badclass:
                    labelbad.append(x)
            print 'tempclass bad'
            #===================================================================
            # for x in range(0,len(tempclass)):
            #     if tempclass[x] >  badclass:
            #         labelbad.append(tempbad[x])
            #===================================================================

            #print 'Temp bad user %d, add bad seeds %d' %(len(tempbad),badcount)
            lengood = len(labelgood)
            lenbad = len(labelbad)
            print 'Temp good user %d, Temp bad user %d' %(len(tempgood),len(tempbad))
            print 'Predict: good %d, bad  %d' %(lengood,lenbad)
            
            
            tbadseeds = []
            tgoodseeds = []
            if (lenbad * ratioT) < lengood:
                for user in labelbad:
                    Labelset[user]=1
                    temptrainset[user]=userfeature[usermap[user]]
                    tbadseeds.append(user)
                    badcount+=1
                for x in range(int(lenbad*ratioT)):
                #for x in range(lengood):
                    Labelset[labelgood[x]]=0
                    temptrainset[labelgood[x]]=userfeature[usermap[labelgood[x]]]
                    tgoodseeds.append(labelgood[x])
                    goodcount+=1 
                   # print x
            else:
                for x in range(int(lengood/ratioT)):
                    Labelset[labelbad[x]]=1
                    temptrainset[labelbad[x]]=userfeature[usermap[labelbad[x]]]
                    tbadseeds.append(labelbad[x])
                    badcount+=1 
                for x in range(lengood):
                    Labelset[labelgood[x]]=0
                    temptrainset[labelgood[x]]=userfeature[usermap[labelgood[x]]]
                    tgoodseeds.append(labelgood[x])
                    goodcount+=1 

            print 'Sample: good %d, bad  %d' %(goodcount,badcount)
            goodeta += 0.1
            badeta += 0.1*ratio
            c.trainsetclear()
            restset = restset - set(temptrainset.keys())
            c.addtrainset(Trainset,userLabel)
            c.addtrainset(temptrainset,Labelset)
            #===================================================================
            # for u in Labelset.keys():
            #     outfile.write(str(u)+'\t'+str(Labelset[u])+'\n')
            #===================================================================
            #trainedset = trainedset | set(Labelset.keys())
            print 'Trainset' ,len(c.trainset)
            c.Training()
            
            if badeta+goodeta>1:#badeta >0.3 or goodeta >0.8:
                print 'done'
                break
   
        
       
    except Exception, e:
        print e
    finally:
       # outfile.close()  
        trainedset = trainedset | set(Labelset.keys())
        #test = [ u for u in usermap.keys() if u not in trainedset ]
        test = list(restset)
        
        usercount = len(userLabel.keys())
        testall = len(test)
        testall = usercount/7
        print '测试集:',testall
        testgood = 0
        testgoodr = 0
        testgoodw = 0
        testbad = 0
        testbadr = 0
        testbadw = 0
        testbadall = 0 #测试集中有多少个spam
        testclass =  c.Predict([ userfeature[usermap[test[x]]] for x in range(0,len(test)) ])
        for x in range(0,testall):
            if test[x] in newspam or test[x] in spamset:
                testbadall += 1
            if testclass[x] < goodclass:
                if test[x] in newspam or test[x] in spamset:
                    testbadw += 1
                else:
                    testgoodr += 1
                testgood += 1
            if testclass[x] > badclass:
                if test[x] in newspam or test[x] in spamset:
                    testbadr += 1
                else:
                    testgoodw += 1
                testbad += 1 
        print 'spam准确率:', float(testbadr)/testbad,testbadr,testbad
        print 'spam召回率:', float(testbadr)/testbadall,testbadr,testbadall
        print 'normal准确率', float(testgoodr)/testgood,testgoodr,testgood
        print 'normal召回率', float(testgoodr)/(testall-testbadall), testgoodr,(testall-testbadall)
        pass

def runsssd5():
    usermap,userfeature=pre.loadfeature('../../../sssddata/14wan/feature/13wan-metric.txt')
    userLabel = pre.getallLabel('../../../sssddata/14wan/feature/13wan-metric.txt')
    outfile = open('../../../sssddata/14wan/predict.txt','w')
   # fin = open('../../../sssddata/14wan/newspam_3times_tree&svm','rb')
    fin = open('../../../sssddata/14wan/newspam_55times_tree&svm_and_TRSR','rb')
    newspam = pickle.load(fin)
    fin.close()
    
    fbad = open('../../../sssddata/14wan/14spamsuspend','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    
    netname = '1-smallnet-bio.txt'

    #初始化rank模型、种子
    pr=PR.PageRank(rankname='reversPR')
    pr.initNet('../../../sssddata/14wan/rank/'+netname,reverse=True)
    pr.initRank(spamset)
    pr.run(100, good=1.0, TrustRank=False)
    order = pr.orderRank()
    
    ratioT =4
    Trainset = {}
    spamseeds = 600
    badseeds=[]
    badcount = 0
    spamcount = 0
    for item in order:
        user, score = item
        if user in spamset:
            
            if spamcount ==spamseeds:
                break
            Trainset[user] = userfeature[usermap[user]]
            badseeds.append(user)
            spamcount += 1
            badcount += 1
            
            
    goodseeds=[]
    goodcount = 0
    base_goodseeds = ratioT*spamcount
    for item in order:
        user, score = item
        if user not in spamset and user not in newspam and goodcount < base_goodseeds:
            Trainset[user] = userfeature[usermap[user]]
            goodseeds.append(user)
            goodcount += 1
    print len(goodseeds),len(badseeds)        
   
    pGood = PR.PageRank(rankname='TrustRank') 
    pGood.initNet('../../../sssddata/14wan/rank/'+netname,reverse=False)
    pBad = PR.PageRank(rankname='AntiRank')
    pBad.initNet('../../../sssddata/14wan/rank/'+netname,reverse=True)
    #初始化训练集、分类器
    c = Classifier.Classifier('svm')
    trainedset=set()
    trainedset= trainedset | set(Trainset.keys())
    restset = set(usermap.keys()) - trainedset
    c.addtrainset(Trainset,userLabel)
    print 'Trainset' ,len(c.trainset)
    print 'restset',len(restset)
    c.Training()
    
    #一些参数
    count = 0
    ratio = float(c.spam)/c.normal
    goodeta = 0.1
    badeta = goodeta/ratioT
    goodclass = 0.5
    badclass = 0.5
    
    #测试参数
    tbadseeds = []
    tgoodseeds = []
    loopbad = 0
    try:
        while 1: 
            count += 1    
            print 'Iteration ',count
            Labelset={}
            temptrainset={}
            
            ##deal with good
            pGood.initRank(goodseeds+tbadseeds)
            pGood.run(100, good=1.0, TrustRank=True) 
            pGood.orderRank()   
            pBad.initRank(badseeds+tbadseeds)
            pBad.run(100, good=1.0, TrustRank=False)
            
            for user in pBad.Rank.keys():
                    #pBad.Rank[user]=float(pBad.Rank[user])/float(pGood.Rank[user])
                    pBad.Rank[user]=float(pBad.Rank[user])-float(pGood.Rank[user])
            pBad.orderRank()    
            
            
            
            tgood = [ pGood.order[x][0] for x in range(0,int(goodeta*len(pGood.order))) if pGood.order[x][0] not in trainedset ]
            tbad = [ pBad.order[x][0] for x in range(0,int(badeta*len(pBad.order))) if pBad.order[x][0] not in trainedset]
            tempgood = list(set(tgood)-set(tbad))
            tempbad = list(set(tbad)-set(tgood))
            
            #tempclass = c.Predict([ userfeature[usermap[tempgood[x]]] for x in range(0,len(tempgood)) ])
            goodcount=0
            
            labelgood=[]
            for x in tempgood:
                ctemp = c.Predict(userfeature[usermap[x]])
                if ctemp < goodclass:
                    labelgood.append(x)
            print 'tempclass good'

            
            badcount = 0
            labelbad=[]
            for x in tempbad:
                ctemp = c.Predict(userfeature[usermap[x]])
                if ctemp > badclass:
                    labelbad.append(x)
            print 'tempclass bad'
            #===================================================================
            # for x in range(0,len(tempclass)):
            #     if tempclass[x] >  badclass:
            #         labelbad.append(tempbad[x])
            #===================================================================

            #print 'Temp bad user %d, add bad seeds %d' %(len(tempbad),badcount)
            lengood = len(labelgood)
            lenbad = len(labelbad)
            print 'Temp good user %d, Temp bad user %d, good : %f, bad : %f ' %(len(tempgood),len(tempbad),float(lengood)/(len(tempgood)+1),float(lenbad)/(1+len(tempbad)))
            print 'Predict: good %d, bad  %d' %(lengood,lenbad)
            
            
            tbadseeds = []
            tgoodseeds = []
            if (lenbad * ratioT) < lengood:
                for user in labelbad:
                    Labelset[user]=1
                    temptrainset[user]=userfeature[usermap[user]]
                    tbadseeds.append(user)
                    badcount+=1
                #for x in range(int(lenbad*ratioT)):
                for x in range(lengood):
                    Labelset[labelgood[x]]=0
                    temptrainset[labelgood[x]]=userfeature[usermap[labelgood[x]]]
                    tgoodseeds.append(labelgood[x])
                    goodcount+=1 
                   # print x
            else:
                for x in range(int(lengood/ratioT)):
                    Labelset[labelbad[x]]=1
                    temptrainset[labelbad[x]]=userfeature[usermap[labelbad[x]]]
                    tbadseeds.append(labelbad[x])
                    badcount+=1 
                for x in range(lengood):
                    Labelset[labelgood[x]]=0
                    temptrainset[labelgood[x]]=userfeature[usermap[labelgood[x]]]
                    tgoodseeds.append(labelgood[x])
                    goodcount+=1 

            print 'Sample: good %d, bad  %d' %(goodcount,badcount)
            if badcount ==0 :
                break
            if badcount>=150:
                loopbad = badcount
            else:
                pass
                

            goodeta += 0.1
            badeta += 0.1*ratio
            if badeta+goodeta>1:#badeta >0.3 or goodeta >0.8:
                print 'done'
                break
            c.trainsetclear()
            restset = restset - set(temptrainset.keys())
            print 'restset',len(restset)
            c.addtrainset(Trainset,userLabel)
            c.addtrainset(temptrainset,Labelset)
            #===================================================================
            # for u in Labelset.keys():
            #     outfile.write(str(u)+'\t'+str(Labelset[u])+'\n')
            #===================================================================
            #trainedset = trainedset | set(Labelset.keys())
            print 'Trainset' ,len(c.trainset)
            c.Training()
            

   
        
       
    except Exception, e:
        print e
    finally:
       # outfile.close()  
       # trainedset = trainedset | set(Labelset.keys())
        #test = [ u for u in usermap.keys() if u not in trainedset ]
        test = list(restset)
        
        usercount = len(userLabel.keys())
        testall = len(test)
        #testall = usercount
        print '测试集:',testall
        testgood = 0
        testgoodr = 0
        testgoodw = 0
        testbad = 0
        testbadr = 0
        testbadw = 0
        testbadall = 0 #测试集中有多少个spam
        testclass =  c.Predict([ userfeature[usermap[test[x]]] for x in range(0,len(test)) ])
        for x in range(0,testall):
            if test[x] in newspam or test[x] in spamset:
                testbadall += 1
            if testclass[x] < goodclass:
                if test[x] in newspam or test[x] in spamset:
                    testbadw += 1
                else:
                    testgoodr += 1
                testgood += 1
            if testclass[x] > badclass:
                if test[x] in newspam or test[x] in spamset:
                    testbadr += 1
                else:
                    testgoodw += 1
                testbad += 1 
        print 'spam准确率:', float(testbadr)/testbad,testbadr,testbad
        print 'spam召回率:', float(testbadr)/testbadall,testbadr,testbadall
        print 'normal准确率', float(testgoodr)/testgood,testgoodr,testgood
        print 'normal召回率', float(testgoodr)/(testall-testbadall), testgoodr,(testall-testbadall)
        pass

if __name__ == '__main__':
    #runsssd()
    runsssd5()
        
        
        
        
        
        