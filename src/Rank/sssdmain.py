# -*- coding: utf-8 -*-
'''
Created on 2014-3-20

@author: Administrator
'''
import Precessor as pre
import pagerank as PR
import Classifier
import pickle



def runsssdgoodseeds_svm():
    usermap,userfeature=pre.loadfeature('../../../sssddata/14wan/feature/13wan-metric.txt')
    #usermap,userfeature=pre.loadfeature_2compare('../../../sssddata/14wan/feature/13wan-metric.txt')
    userLabel = pre.getallLabel('../../../sssddata/14wan/feature/13wan-metric.txt')
    outfile = open('../../../sssddata/14wan/predict.txt','w')
    #fin = open('../../../sssddata/14wan/newspam_4times','rb')
    fin = open('../../../sssddata/14wan/newspam_svm2','rb')
    newspam = pickle.load(fin)
    fin.close()
    fnew = open('../../../sssddata/14wan/newspam_relate.txt','rb')
    newspam2 = set()
    for line in fnew:
        newspam2.add(line.strip())
    fnew.close()
    print len(set(usermap.keys()) & newspam2)
    
    print len(newspam),len(newspam&newspam2)
    fbad = open('../../../sssddata/14wan/14spamsuspend','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    #newspam = newspam | newspam2
    netname = '1-smallnet-bio.txt'

    #------------------初始化rank模型、种子
    ratioT = 1.9
    Trainset = {}
    spamseeds =800
    badseeds=[]
    badcount = 0
    spamcount = 0
    
    #===========================================================================
    # for user in userLabel.keys():
    #     if user in spamset:# or user in newspam:
    #         if spamcount == spamseeds:
    #             break
    #         Trainset[user] = userfeature[usermap[user]]
    #         userLabel[user] = 1
    #         badseeds.append(user)
    #         spamcount += 1
    #         badcount += 1
    #===========================================================================
    
    pr=PR.PageRank(rankname='PR')
    pr.initNet('../../../sssddata/14wan/rank/'+netname,reverse=False)
    pr.initRank(spamset)
    pr.run(100, good=1.0, TrustRank=False)
    order = pr.orderRank()
    for item in order:
        user, score = item
        if user in spamset :#or user in newspam:
                    
            if spamcount ==spamseeds:
                break
            Trainset[user] = userfeature[usermap[user]]
            badseeds.append(user)
            spamcount += 1
            badcount += 1
     
    
    
    if spamcount< spamseeds:
        for item in order:
            user, score = item
            if user in newspam:
                     
                if spamcount ==spamseeds:
                    break
                Trainset[user] = userfeature[usermap[user]]
                userLabel[user] = 1
                badseeds.append(user)
                spamcount += 1
                badcount += 1 
    
    #--------goodseeds selecting    
    goodseeds=[]
    goodcount = 0
    base_goodseeds = ratioT*spamcount      
          
    #===========================================================================
    # Rpr=PR.PageRank(rankname='reversPR')
    # Rpr.initNet('../../../sssddata/14wan/rank/'+netname,reverse=True)
    # Rpr.initRank(spamset)
    # Rpr.run(100, good=1.0, TrustRank=False)
    # Rorder = pr.orderRank()         
    # for item in Rorder:
    #     user, score = item
    #     if goodcount == base_goodseeds:
    #         break
    #     if user not in spamset and user not in newspam :
    #         Trainset[user] = userfeature[usermap[user]]
    #         goodseeds.append(user)
    #         goodcount +=1
    #===========================================================================
    
    for user in userLabel.keys():
        if goodcount == base_goodseeds:
            break
        if user not in spamset and user not in newspam :
            Trainset[user] = userfeature[usermap[user]]
            goodseeds.append(user)
            goodcount +=1
            
    print len(badseeds),len(goodseeds)
    
    #----------------------------------
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

            #===================================================================
            # if badcount>=loopbad:
            #     loopbad = badcount
            # else:
            #     break
            #===================================================================
                

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
        testall = len(test)/4
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
        print '预测准确率',float(testbadr+testgoodr)/testall
        
def runsssdgoodseeds_svm1():
    usermap,userfeature=pre.loadfeature('../../../sssddata/14wan/feature/13wan-metric.txt')
    userLabel = pre.getallLabel('../../../sssddata/14wan/feature/13wan-metric.txt')
    outfile = open('../../../sssddata/14wan/predict.txt','w')
    #fin = open('../../../sssddata/14wan/newspam_4times','rb')
    fin = open('../../../sssddata/14wan/newspam_svm2','rb')
    newspam = pickle.load(fin)
    fin.close()
    fnew = open('../../../sssddata/14wan/newspam_relate.txt','rb')
    newspam2 = set()
    for line in fnew:
        newspam2.add(line.strip())
    fnew.close()
    print len(set(usermap.keys()) & newspam2)
    
    print len(newspam),len(newspam&newspam2)
    fbad = open('../../../sssddata/14wan/14spamsuspend','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    #newspam = newspam | newspam2
    netname = '1-smallnet-bio.txt'

    #初始化rank模型、种子
    pr=PR.PageRank(rankname='reversPR')
    pr.initNet('../../../sssddata/14wan/rank/'+netname,reverse=True)
    pr.initRank(spamset)
    pr.run(100, good=1.0, TrustRank=False)
    order = pr.orderRank()
    
    ratioT = 2
    Trainset = {}
    spamseeds = 800
    badseeds=[]
    badcount = 0
    spamcount = 0
    for user in userLabel.keys():
        if user in spamset :#or user in newspam:
            if spamcount == spamseeds:
                break
            Trainset[user] = userfeature[usermap[user]]
            userLabel[user] = 1
            badseeds.append(user)
            spamcount += 1
            badcount += 1
    #===========================================================================
    # for item in order:
    #     user, score = item
    #     if user in spamset:
    #           
    #         if spamcount ==spamseeds:
    #             break
    #         Trainset[user] = userfeature[usermap[user]]
    #         badseeds.append(user)
    #         spamcount += 1
    #         badcount += 1
    #===========================================================================
            
            
    goodseeds=[]
    goodcount = 0
    base_goodseeds = ratioT*spamcount
    for user in userLabel.keys():
        if user not in spamset and user not in newspam and goodcount < base_goodseeds:
            Trainset[user] = userfeature[usermap[user]]
            goodseeds.append(user)
            goodcount += 1
            
    print len(badseeds),len(goodseeds)
   
    pGood = PR.PageRank(rankname='TrustRank') 
    pGood.initNet('../../../sssddata/14wan/rank/'+netname,reverse=False)
    pBad = PR.PageRank(rankname='AntiRank')
    pBad.initNet('../../../sssddata/14wan/rank/'+netname,reverse=True)
    pGood.initRank(goodseeds)
    pBad.initRank(badseeds)
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
            pGood.reloadseeds(goodseeds+tbadseeds)
            pGood.run(10, good=1.0, TrustRank=True) 
            pGood.orderRank()   
            pBad.reloadseeds(badseeds+tbadseeds)
            pBad.run(10, good=1.0, TrustRank=False)
            
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
            #===================================================================
            # if badcount ==0 :
            #     break
            #===================================================================
            #===================================================================
            # if badcount>=loopbad:
            #     loopbad = badcount
            # else:
            #     break
            #===================================================================
                

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
        print Exception,e
    finally:
        test = list(restset)
          
        usercount = len(userLabel.keys())
        testall = len(test)/3
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

def runsssdgoodseeds_forest():
    usermap,userfeature=pre.loadfeature('../../../sssddata/14wan/feature/13wan-metric.txt')
    userLabel = pre.getallLabel('../../../sssddata/14wan/feature/13wan-metric.txt')
    outfile = open('../../../sssddata/14wan/predict.txt','w')
    #fin = open('../../../sssddata/14wan/newspam_4times','rb')
    fin = open('../../../sssddata/14wan/newspam_svm2','rb')
    newspam = pickle.load(fin)
    fin.close()
    
    fbad = open('../../../sssddata/14wan/14spamsuspend','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    
    netname = '1-smallnet-bio.txt'

    #初始化rank模型、种子
    #===========================================================================
    # pr=PR.PageRank(rankname='reversPR')
    # pr.initNet('../../../sssddata/14wan/rank/'+netname,reverse=True)
    # pr.initRank(spamset)
    # pr.run(100, good=1.0, TrustRank=False)
    # order = pr.orderRank()
    #===========================================================================
    
    ratioT = 4
    Trainset = {}
    spamseeds = 800
    badseeds=[]
    badcount = 0
    spamcount = 0
    for user in userLabel.keys():
        if user in spamset or user in newspam:
            if spamcount == spamseeds:
                break
            Trainset[user] = userfeature[usermap[user]]
            userLabel[user] = 1
            badseeds.append(user)
            spamcount += 1
            badcount += 1
    #===========================================================================
    # for item in order:
    #     user, score = item
    #     if user in spamset:
    #         
    #         if spamcount ==spamseeds:
    #             break
    #         Trainset[user] = userfeature[usermap[user]]
    #         badseeds.append(user)
    #         spamcount += 1
    #         badcount += 1
    #===========================================================================
            
            
    goodseeds=[]
    goodcount = 0
    base_goodseeds = ratioT*spamcount
    for user in userLabel.keys():
        if user not in spamset and user not in newspam and goodcount < base_goodseeds:
            Trainset[user] = userfeature[usermap[user]]
            goodseeds.append(user)
            goodcount += 1
    print len(badseeds),len(goodseeds)
   
    pGood = PR.PageRank(rankname='TrustRank') 
    pGood.initNet('../../../sssddata/14wan/rank/'+netname,reverse=False)
    pBad = PR.PageRank(rankname='AntiRank')
    pBad.initNet('../../../sssddata/14wan/rank/'+netname,reverse=True)
    #初始化训练集、分类器
    c = Classifier.Classifier('tree')
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
            #===================================================================
            # if badcount ==0 :
            #     break
            #===================================================================
            if badcount>=loopbad:
                loopbad = badcount
            else:
                break
                

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
        testall = len(test)/3
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

def runsssd_last():
    usermap,userfeature=pre.loadfeature('../../../sssddata/14wan/feature/13wan-metric.txt')
    
    fnew = open('../../../sssddata/14wan/newspam_relate.txt','rb')
    newspam2 = set()
    for line in fnew:
        newspam2.add(line.strip())
    fnew.close()
    
    fin = open('../../../sssddata/14wan/network/newlinkspam-1','rb')
    newspam = pickle.load(fin)
    fin.close()
    fbad = open('../../../sssddata/14wan/14spamsuspend','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    fgood = open('../../../sssddata/14wan/network/goodseeds','rb')
    goodset = pickle.load(fgood)
    fgood.close()
    
    netname = '2-smallnet-bio.txt'
     #初始化rank模型、种子
    #===========================================================================
    # pr=PR.PageRank(rankname='reversPR')
    # pr.initNet('../../../sssddata/14wan/rank/'+netname,reverse=True)
    # pr.initRank(spamset)
    # pr.run(100, good=1.0, TrustRank=False)
    # order = pr.orderRank()
    #===========================================================================
    
    ratioT = 2
    Trainset = {}
    spamseeds = 800
    badseeds=[]
    badcount = 0
    spamcount = 0
    userLabel={}
    for user in spamset:
        if spamcount == spamseeds:
            break
        if user in usermap.keys():
            Trainset[user] = userfeature[usermap[user]]
            userLabel[user] = 1
            badseeds.append(user)
            spamcount += 1
            badcount += 1
            
            
    goodseeds=[]
    goodcount = 0
    base_goodseeds = ratioT*spamcount
    for user in goodset:
        if  goodcount < base_goodseeds:
            Trainset[user] = userfeature[usermap[user]]
            goodseeds.append(user)
            userLabel[user] = 0
            goodcount += 1
    print len(badseeds),len(goodseeds)
   
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
#     Labelset={}
#     temptrainset={}
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
            #===================================================================
            # if badcount ==0 :
            #     break
            #===================================================================
            #===================================================================
            # if badcount>=loopbad:
            #     loopbad = badcount
            # else:
            #     break
            #===================================================================
                

            goodeta += 0.1
            badeta += 0.1*ratio
            if badeta+goodeta>1:#badeta >0.3 or goodeta >0.8:
                print 'done'
                break
            c.trainsetclear()
            
            print 'restset',len(restset)
            c.addtrainset(Trainset,userLabel)

            trainedset = trainedset | set(Labelset.keys())
            c.addtrainset(temptrainset,Labelset)
           # restset = restset - set(temptrainset.keys())
            restset = restset - set(trainedset)
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
        
        
def runsssd_last1():
    usermap,userfeature=pre.loadfeature('../../../sssddata/14wan/feature/13wan-metric.txt')
    fin = open('../../../sssddata/14wan/network/newlinkspam-2','rb')
    newspam = pickle.load(fin)
    fin.close()
    fbad = open('../../../sssddata/14wan/14spamsuspend','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    fgood = open('../../../sssddata/14wan/network/goodseeds','rb')
    goodset = pickle.load(fgood)
    fgood.close()
    
    netname = '2-smallnet-bio.txt'
     #初始化rank模型、种子
    #===========================================================================
    # pr=PR.PageRank(rankname='reversPR')
    # pr.initNet('../../../sssddata/14wan/rank/'+netname,reverse=True)
    # pr.initRank(spamset)
    # pr.run(100, good=1.0, TrustRank=False)
    # order = pr.orderRank()
    #===========================================================================
    
    ratioT = 6
    Trainset = {}
    spamseeds = 600
    badseeds=[]
    badcount = 0
    spamcount = 0
    userLabel={}
    for user in spamset:
        if spamcount == spamseeds:
            break
        if user in usermap.keys():
            Trainset[user] = userfeature[usermap[user]]
            userLabel[user] = 1
            badseeds.append(user)
            spamcount += 1
            badcount += 1
            
            
    goodseeds=[]
    goodcount = 0
    base_goodseeds = ratioT*spamcount
    for user in goodset:
        if  goodcount < base_goodseeds:
            Trainset[user] = userfeature[usermap[user]]
            goodseeds.append(user)
            userLabel[user] = 0
            goodcount += 1
    print len(badseeds),len(goodseeds)
   
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
#     Labelset={}
#     temptrainset={}
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
            #===================================================================
            # if badcount ==0 :
            #     break
            #===================================================================
            #===================================================================
            # if badcount>=loopbad:
            #     loopbad = badcount
            # else:
            #     break
            #===================================================================
                

            goodeta += 0.1
            badeta += 0.1*ratio
            if badeta+goodeta>1:#badeta >0.3 or goodeta >0.8:
                print 'done'
                break
            c.trainsetclear()
            
            print 'restset',len(restset)
            c.addtrainset(Trainset,userLabel)

            trainedset = trainedset | set(Labelset.keys())
            c.addtrainset(temptrainset,Labelset)
           # restset = restset - set(temptrainset.keys())
            restset = restset - set(trainedset)
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

if __name__ == '__main__':
    #runsssd()
    runsssdgoodseeds_svm()
    #runsssdgoodseeds_forest()
    #runsssd_last()
        
        
        
        
        
        