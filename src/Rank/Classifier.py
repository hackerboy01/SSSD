'''
Created on 2014-3-18

@author: Administrator
'''
import Precessor as pre
from sklearn import svm

class Classifier:
    def __init__(self,name):
        self.name = name
        self.trainset=[]
        self.label=[]
        self.trainuserid=[]
        self.clf = svm.SVC(kernel='linear')
    def addtrainset(self,training={},Label={}):
        for userid in training.keys():
            self.trainset.append(list(training[userid]))
            self.trainuserid.append(userid)
            self.label.append(Label[userid])
        print 'training set build!'
    def Training(self):   
         self.clf.fit(self.trainset,self.label)
         print 'Training complete!'
    def Predict(self,test):
        return self.clf.predict(test)


if __name__ == '__main__':
    #load features of all users including training set. username[i] corresponding feature userfeature[i]
    usernames,userfeature=pre.loadfeature('../../../sssddata/spamleusers.txt')
    #userLabel={userID:Label}
    userLabel = pre.getLabel('../../../sssddata/finalseeds.txt')
    Trainset = pre.getTrainset(userfeature, usernames, userLabel)
    c = Classifier('svm')
    c.addtrainset(Trainset,userLabel)
    c.Training()
   # for user in Trainset.keys()
   # print Trainset
    print c.Predict([0.1,1,0.1,0.1,0.2])
    pass