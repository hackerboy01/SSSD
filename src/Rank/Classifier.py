'''
Created on 2014-3-18

@author: Administrator
'''
import Precessor as pre
from sklearn import svm
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier as RFC
import pagerank as pg
import pickle

class Classifier:
    def __init__(self,name='svm'):
        self.name = name
        self.trainset=[]
        self.label=[]
        self.trainuserid=[]
        if name == 'svm':
            self.clf = svm.SVC(kernel='rbf')
        elif name =='tree':
            self.clf = tree.DecisionTreeClassifier()
        elif name =='forest':
            self.clf=RFC(n_estimators=10)
        self.weight=[]
        self.spam = 0
        self.normal = 0
    def trainsetclear(self):
        self.trainset=[]
        self.label=[]
        self.trainuserid=[]
        self.spam = 0
        self.normal = 0
    def addtrainset(self,training={},Label={}):
        for userid in training.keys():
            self.trainset.append(list(training[userid]))
            self.trainuserid.append(userid)
            self.label.append(Label[userid])
            if Label[userid]>0.5:
                self.spam += 1
            else :
                self.normal += 1
        if __name__=='__main__':
            print 'training set build!'
    def Training(self):   
         self.clf.fit(self.trainset,self.label)
         print 'spam: %d, normal: %d, all: %d'%(self.spam,self.normal,len(self.label))
         if __name__=='__main__':
             print 'Training complete!'
    def TrainingB(self):   
        self.weight=[]
        print self.spam,self.normal,len(self.label)
        for it in range(0,len(self.label)):
            if self.label[it]<0.5:
                self.weight.append(1.0)
            else :
                self.weight.append(float(self.normal)/self.spam)
         
        self.clf.fit(self.trainset,self.label,sample_weight=self.weight)
        print self.clf.class_weight
        print 'TrainingB complete!'         
    def Predict(self,test):
        return self.clf.predict(test)


if __name__ == '__main__':
    #load features of all users including training set. username[i] corresponding feature userfeature[i]
    #usernames,userfeature=pre.loadfeature('../../../sssddata/spamleusers.txt')
    #userLabel={userID:Label}
    #userLabel = pre.getLabel('../../../sssddata/finalseeds.txt')
    usermap,userfeature=pre.loadfeature('../../../sssddata/14wan/feature/13wan-metric.txt')
    userLabel = pre.getallLabel('../../../sssddata/14wan/feature/13wan-metric.txt')
    fbad = open('../../../sssddata/14wan/14spamsuspend','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    netname = '1-smallnet-bio.txt' 
    PR=pg.PageRank()
    PR.initNet('../../../sssddata/14wan/rank/'+netname,reverse=False)
    PR.initRank(spamset)
    PR.run(200, good=1.0, TrustRank=False)
    print 'pagerank'
    order = PR.orderRank(reverse=False)
    

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
            if count < 1.5*spamcount:
                count+=1
                Trainset[user] = userfeature[usermap[user]]
    
    c = Classifier('forest')
    c.addtrainset(Trainset,userLabel)
    c.Training()
   # for user in Trainset.keys()
   # print Trainset
    predict = {}
    spam = 0
    normal = 0
    for user in userLabel:
        if user not in Trainset.keys():
            predict[user]=c.Predict(userfeature[usermap[user]])
           # print predict[user]
            if predict[user] == 1:
                spam +=1
            else:
                normal += 1
    print spam,normal        
         
    #print c.Predict([0.1,1,0.1,0.1,0.2])
    pass