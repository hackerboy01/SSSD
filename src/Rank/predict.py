'''
Created on 2014-5-7

@author: Administrator
'''

import Classifier 
import pagerank as pg
import Precessor as pre
import pickle

ratioc = 2
ratio = 5.5
tao = 600
def PredictWithPagerank():
        
    spamPR=set()
    netname = '1-smallnet-bio.txt' 
    fbad = open('../../../sssddata/14wan/14spamsuspend','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    #print len(spamset)
    PR=pg.PageRank()
    PR.initNet('../../../sssddata/14wan/rank/'+netname,reverse=False)
    print len(PR.users)
    PR.initRank(spamset)
    PR.run(200, good=1.0, TrustRank=False)
    print 'pagerank'
    order = PR.orderRank()
    #order = PR.orderRank(False)
    

    #===========================================================================
    # count  = 0
    # seeds=set()
    # for item in order:
    #     uid,pr=item
    #     if uid not in spamset:
    #         count += 1
    #         if count < tao:
    #             seeds.add(uid)
    #              
    # 
    # PR.initNet('../../../sssddata/14wan/rank/'+netname,reverse=False)
    # PR.initRank(seeds)
    # PR.run(200, good=1.0, TrustRank=True)
    # order = PR.orderRank()
    #===========================================================================
    
    
    
    usermap,userfeature=pre.loadfeature('../../../sssddata/14wan/feature/13wan-metric.txt')
    userLabel = pre.getallLabel('../../../sssddata/14wan/feature/13wan-metric.txt')
    #Trainset = pre.getTrainset(userfeature, usermap, userLabel)
    Trainset = {}
    for user in userLabel:
        if userLabel[user] == 1:
            Trainset[user] = userfeature[usermap[user]]
    spamcount = len(Trainset.keys())
    Trainset.clear()
    count = 0
    #for uid in userLabel.keys() :
    for item in order:
        uid,tr = item
        if userLabel[uid] == 0:
            if count < ratio*spamcount:
                count+=1
                Trainset[uid] = userfeature[usermap[uid]]
        else:
            Trainset[uid] = userfeature[usermap[uid]]
    
    csvm = Classifier.Classifier('svm')
    csvm.addtrainset(Trainset,userLabel)
    csvm.Training()
    ctree= Classifier.Classifier('tree')
    ctree.addtrainset(Trainset,userLabel)
    ctree.Training()
   # for user in Trainset.keys()
   # print Trainset
    predict_svm = {}
    predict_tree={}
    spam = 0
    normal = 0
    spamPR_svm=set()
    spamPR_tree =set()
    for user in userLabel:
        if user not in Trainset.keys():
            predict_svm[user]=csvm.Predict(userfeature[usermap[user]])
            predict_tree[user]=ctree.Predict(userfeature[usermap[user]])
           # print predict[user]
            if predict_svm[user] == 1 and predict_tree[user]==1:
                spam +=1
                spamPR.add(user)
            else:
                normal += 1
            if predict_svm[user]==1:
                spamPR_svm.add(user)
            if predict_tree[user]==1:
                spamPR_tree.add(user)
                
    print 'spamPR:',spam,normal 
    print len(spamPR_svm),len(spamPR_tree)
    return spamPR       
         
def PredictWithTrustrank():
        
    spamTR=set()
    netname = '1-smallnet-bio.txt' 

    fbad = open('../../../sssddata/14wan/14spamsuspend','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    #print len(spamset)
    PR=pg.PageRank()
    PR.initNet('../../../sssddata/14wan/rank/'+netname,reverse=True)
    PR.initRank(spamset)
    PR.run(200, good=1.0, TrustRank=False)
    print 'pagerank'
    order = PR.orderRank()
    

    count  = 0
    seeds=set()
    for item in order:
        uid,pr=item
        if uid not in spamset:
            count += 1
            if count < tao:
                seeds.add(uid)
                  
     
    PR.initNet('../../../sssddata/14wan/rank/'+netname,reverse=False)
    PR.initRank(seeds)
    PR.run(200, good=1.0, TrustRank=True)
    order = PR.orderRank()
    
    
    
    usermap,userfeature=pre.loadfeature('../../../sssddata/14wan/feature/13wan-metric.txt')
    userLabel = pre.getallLabel('../../../sssddata/14wan/feature/13wan-metric.txt')
    #Trainset = pre.getTrainset(userfeature, usermap, userLabel)
    Trainset = {}
    for user in userLabel:
        if userLabel[user] == 1:
            Trainset[user] = userfeature[usermap[user]]
    spamcount = len(Trainset)
    
    count = 0
    #for uid in userLabel.keys() :
    for item in order:
        uid,tr = item
        if userLabel[uid] == 0:
            if count < ratio*spamcount:
                count+=1
                Trainset[uid] = userfeature[usermap[uid]]
    
    csvm = Classifier.Classifier('svm')
    csvm.addtrainset(Trainset,userLabel)
    csvm.Training()
    ctree= Classifier.Classifier('tree')
    ctree.addtrainset(Trainset,userLabel)
    ctree.Training()
   # for user in Trainset.keys()
   # print Trainset
    predict_svm = {}
    predict_tree={}
    spam = 0
    normal = 0
    spamTR_svm=set()
    spamTR_tree =set()
    for user in userLabel:
        if user not in Trainset.keys():
            predict_svm[user]=csvm.Predict(userfeature[usermap[user]])
            predict_tree[user]=ctree.Predict(userfeature[usermap[user]])
           # print predict[user]
            if predict_svm[user] == 1 and predict_tree[user]==1:
                spam +=1
                spamTR.add(user)
            else:
                normal += 1
            if predict_svm[user]==1:
                spamTR_svm.add(user)
            if predict_tree[user]==1:
                spamTR_tree.add(user)
                
    print 'spamTR:',spam,normal 
    print len(spamTR_svm),len(spamTR_tree)
    return spamTR  

def PredictWithSpamrank():
    spamSR=set()
    netname = '1-smallnet-bio.txt'
    fbad = open('../../../sssddata/14wan/14spamsuspend','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    antiRank,seeds = pg.runAntiTrustrank(netname = netname , tao = tao)
   # print "anti Rank!"
    
    trustRank = pg.runTrustrank(netname = netname , tao = tao)
    #trustRank = pg.runPageRank(netname = netname , tao = tao)
   # print "trust rank"
    print len(antiRank.keys()),len(trustRank.keys())
    spamrank={}
    for user in antiRank.keys():
        if trustRank[user]==0:
            print user
        #spamrank[user]=float(antiRank[user])/float(trustRank[user])
        spamrank[user]=float(antiRank[user])-float(trustRank[user])
        #print antiRank[user],trustRank[user],spamrank[user]
    order = sorted(spamrank.iteritems(), key=lambda pair: pair[1], reverse=False)  
    

    #===========================================================================
    # count  = 0
    # seeds=set()
    # for item in order:
    #     uid,pr=item
    #     if uid not in spamset:
    #         count += 1
    #         if count < tao:
    #             seeds.add(uid)
    #              
    # 
    # PR.initNet('../../../sssddata/14wan/rank/'+netname,reverse=False)
    # PR.initRank(seeds)
    # PR.run(200, good=1.0, TrustRank=True)
    # order = PR.orderRank()
    #===========================================================================
    
    
    
    usermap,userfeature=pre.loadfeature('../../../sssddata/14wan/feature/13wan-metric.txt')
    userLabel = pre.getallLabel('../../../sssddata/14wan/feature/13wan-metric.txt')
    #Trainset = pre.getTrainset(userfeature, usermap, userLabel)
    Trainset = {}
    for user in userLabel:
        if userLabel[user] == 1:
            Trainset[user] = userfeature[usermap[user]]
    spamcount = len(Trainset)
    
    count = 0
    #for uid in userLabel.keys() :
    for item in order:
        uid,tr = item
        if userLabel[uid] == 0:
            if count < ratio*spamcount:
                count+=1
                Trainset[uid] = userfeature[usermap[uid]]
    
    csvm = Classifier.Classifier('svm')
    csvm.addtrainset(Trainset,userLabel)
    csvm.Training()
    ctree= Classifier.Classifier('tree')
    ctree.addtrainset(Trainset,userLabel)
    ctree.Training()
   # for user in Trainset.keys()
   # print Trainset
    predict_svm = {}
    predict_tree={}
    spam = 0
    normal = 0
    spamSR_svm=set()
    spamSR_tree =set()
    for user in userLabel:
        if user not in Trainset.keys():
            predict_svm[user]=csvm.Predict(userfeature[usermap[user]])
            predict_tree[user]=ctree.Predict(userfeature[usermap[user]])
           # print predict[user]
            if predict_svm[user] == 1 and predict_tree[user]==1:
                spam +=1
                spamSR.add(user)
            else:
                normal += 1
            if predict_svm[user]==1:
                spamSR_svm.add(user)
            if predict_tree[user]==1:
                spamSR_tree.add(user)
                
    print 'spamSR:',spam,normal 
    print len(spamSR_svm),len(spamSR_tree)
    return spamSR  


def PredictWithSVM():
    usermap,userfeature=pre.loadfeature('../../../sssddata/14wan/feature/13wan-metric.txt')
    userLabel = pre.getallLabel('../../../sssddata/14wan/feature/13wan-metric.txt')
    fbad = open('../../../sssddata/14wan/14spamsuspend','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    #===========================================================================
    # netname = '1-smallnet-bio.txt' 
    # PR=pg.PageRank()
    # PR.initNet('../../../sssddata/14wan/rank/'+netname,reverse=False)
    # PR.initRank(spamset)
    # PR.run(200, good=1.0, TrustRank=False)
    # print 'pagerank'
    # order = PR.orderRank(reverse=False)
    #===========================================================================
    
    
    #Trainset = pre.getTrainset(userfeature, usermap, userLabel)
    Trainset = {}
    for user in userLabel:
        if userLabel[user] == 1:
            Trainset[user] = userfeature[usermap[user]]
    spamcount = len(Trainset)
    
    count = 0
    #===========================================================================
    # for item in order:
    #     user,pr = item
    #     if userLabel[user] == 0:
    #          if count < 2.0*spamcount:
    #             count+=1
    #             Trainset[user] = userfeature[usermap[user]]           
    #===========================================================================
    for user in userLabel:
        if userLabel[user] == 0:
            if count < ratioc*spamcount:
                count+=1
                Trainset[user] = userfeature[usermap[user]]
    
    c = Classifier.Classifier('svm')
    c.addtrainset(Trainset,userLabel)
    c.Training()
   # for user in Trainset.keys()
   # print Trainset
    predict = {}
    spam = 0
    normal = 0
    SVMspam = set()
    for user in userLabel:
        if user not in Trainset.keys():
            predict[user]=c.Predict(userfeature[usermap[user]])
           # print predict[user]
            if predict[user] == 1:
                SVMspam.add(user)
                spam +=1
            else:
                normal += 1
    print 'SVM:',spam,normal  
    return SVMspam
def PredictWithTree():
    usermap,userfeature=pre.loadfeature('../../../sssddata/14wan/feature/13wan-metric.txt')
    userLabel = pre.getallLabel('../../../sssddata/14wan/feature/13wan-metric.txt')
    fbad = open('../../../sssddata/14wan/14spamsuspend','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    #===========================================================================
    # netname = '1-smallnet-bio.txt' 
    # PR=pg.PageRank()
    # PR.initNet('../../../sssddata/14wan/rank/'+netname,reverse=False)
    # PR.initRank(spamset)
    # PR.run(200, good=1.0, TrustRank=False)
    # print 'pagerank'
    # order = PR.orderRank(reverse=False)
    #===========================================================================
    
    
    #Trainset = pre.getTrainset(userfeature, usermap, userLabel)
    Trainset = {}
    for user in userLabel:
        if userLabel[user] == 1:
            Trainset[user] = userfeature[usermap[user]]
    spamcount = len(Trainset)
    
    count = 0
    #===========================================================================
    # for item in order:
    #     user,pr = item
    #     if userLabel[user] == 0:
    #          if count < 2.0*spamcount:
    #             count+=1
    #             Trainset[user] = userfeature[usermap[user]]           
    #===========================================================================
    for user in userLabel:
        if userLabel[user] == 0:
            if count < ratioc*spamcount:
                count+=1
                Trainset[user] = userfeature[usermap[user]]
    
    c = Classifier.Classifier('tree')
    c.addtrainset(Trainset,userLabel)
    c.Training()
   # for user in Trainset.keys()
   # print Trainset
    predict = {}
    spam = 0
    normal = 0
    Treespam = set()
    for user in userLabel:
        if user not in Trainset.keys():
            predict[user]=c.Predict(userfeature[usermap[user]])
           # print predict[user]
            if predict[user] == 1:
                Treespam.add(user)
                spam +=1
            else:
                normal += 1
    print 'Tree:',spam,normal  
    return Treespam
    
def PredictWithForest():
    usermap,userfeature=pre.loadfeature('../../../sssddata/14wan/feature/13wan-metric.txt')
    userLabel = pre.getallLabel('../../../sssddata/14wan/feature/13wan-metric.txt')
    fbad = open('../../../sssddata/14wan/14spamsuspend','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    #===========================================================================
    # netname = '1-smallnet-bio.txt' 
    # PR=pg.PageRank()
    # PR.initNet('../../../sssddata/14wan/rank/'+netname,reverse=False)
    # PR.initRank(spamset)
    # PR.run(200, good=1.0, TrustRank=False)
    # print 'pagerank'
    # order = PR.orderRank(reverse=False)
    #===========================================================================
    
    
    #Trainset = pre.getTrainset(userfeature, usermap, userLabel)
    Trainset = {}
    for user in userLabel:
        if userLabel[user] == 1:
            Trainset[user] = userfeature[usermap[user]]
    spamcount = len(Trainset)
    
    count = 0
    #===========================================================================
    # for item in order:
    #     user,pr = item
    #     if userLabel[user] == 0:
    #          if count < 2.0*spamcount:
    #             count+=1
    #             Trainset[user] = userfeature[usermap[user]]           
    #===========================================================================
    for user in userLabel:
        if userLabel[user] == 0:
            if count < ratioc*spamcount:
                count+=1
                Trainset[user] = userfeature[usermap[user]]
    
    c = Classifier.Classifier('forest')
    c.addtrainset(Trainset,userLabel)
    c.Training()
   # for user in Trainset.keys()
   # print Trainset
    predict = {}
    spam = 0
    normal = 0
    Forestspam = set()
    for user in userLabel:
        if user not in Trainset.keys():
            predict[user]=c.Predict(userfeature[usermap[user]])
           # print predict[user]
            if predict[user] == 1:
                Forestspam.add(user)
                spam +=1
            else:
                normal += 1
    print 'Forest:',spam,normal  
    return Forestspam


def PredictRank():
    spamTR=PredictWithTrustrank()
    print len(spamTR)
    #spamPR=PredictWithPagerank()
    spamSR=PredictWithSpamrank()
    #spamlast = spamTR&spamPR&spamSR
    spamlast = spamTR&spamSR
    fout = open('../../../sssddata/14wan/newspam_55times_tree&svm_and_TRSR','wb')
    pickle.dump(spamlast, fout)
    fout.close()
    print len(spamlast)

def PredictClass():
    svmset = PredictWithSVM()
    #treeset = PredictWithTree()
    forestset = PredictWithForest()
    spamset = svmset | forestset
    #spamset = forestset
    fout = open('../../../sssddata/14wan/newspam_forest_or_svm','wb')
    pickle.dump(spamset, fout)
    fout.close()
    print len(spamset)
    
if __name__ == '__main__':
    PredictClass()