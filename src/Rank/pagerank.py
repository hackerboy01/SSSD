'''
Created on 2014-1-3

@author: Administrator
'''
import math



global Rank
Rank ={}

class PageRank:
    def __init__(self,outnetwork,innetwork,users,Rank={}):
        self.seeds = []
        self.outnetwork = outnetwork
        self.innetwork = innetwork
        self.users = users
        self.Rank=Rank
        self.a = 0.85
        self.b = 1-self.a
        self.order=[]
        
    def run(self,iteration=1,good=1.0):
        #self.initRank()
        count = 0
        while count < iteration:
            sigma = 0.0
            tempRank = self.Rank.copy()
            for user in self.users:
                temp = 0.0
                for inuser in self.innetwork[user]:
                    temp += tempRank[inuser]/len(self.outnetwork[inuser])
                if user in self.seeds:
                    good = 1.0
                else :
                    good = 0.0
                self.Rank[user] = self.a*temp + self.b*good/len(self.seeds)
            for user in self.users:
                sigma += abs(self.Rank[user]-tempRank[user])
            del tempRank
            count += 1
            #print count,sigma,self.showRank()
            if sigma < 1e-7:
                break
        return self.Rank   

    def initRank(self,seeds,good=True):
        if good:
            good=1.0
        else :
            good = -1.0
        self.seeds=seeds
        for user in self.users:     
            self.Rank[user]=0.0  
            if user in self.seeds:
                self.Rank[user]=good/len(self.seeds)
    def orderRank(self,reverse=True):
        self.order=sorted(self.Rank.iteritems(), key=lambda pair: pair[1], reverse=reverse)
        #print Rank   
    def showRank(self):
        sum = 0
        for x in self.Rank.keys():
            sum+=self.Rank[x]   
        return sum
        




def loadnet(outdegree,indegree):
    follow = {}
    follower = {}
    file = open(outdegree,'r')
    count = 0
    while 1:
        line = file.readline()
        if line == '':
            break
        temp = line.strip().split()
        if len(temp)>1:
                follow[temp[0]]=temp[1:]
    print "out Network Loaded!"
    file.close()
    file = open(indegree,'r')
    count = 0
    while 1:
        line = file.readline()
        if line == '':
            break
        temp = line.strip().split()
        if len(temp)>1:
                follower[temp[0]]=temp[1:]
    print "in Network Loaded!"
    file.close()
    return follow, follower

def loadnet1(outdegree,indegree):
    follow = {}
    follower = {}
    users = set()
    file = open(outdegree,'r')
    count = 0
    while 1:
        line = file.readline()
        if line == '':
            break
        temp = line.strip().split()
        if len(temp)>1:
                follow[temp[0]]=temp[1:]
    print "out Network Loaded!"
    file.close()
    file = open(indegree,'r')
    count = 0
    while 1:
        line = file.readline()
        if line == '':
            break
        temp = line.strip().split()
        if len(temp)>1:
                follower[temp[0]]=temp[1:]
    print "in Network Loaded!"
    file.close()
   
    return follow, follower

def loadseeds():
    file = open('../../../sssddata/finalseeds.txt','r')
    goodseeds=[]
    badseeds=[]

    while 1:
        line = file.readline()
        if line =='':
            break
        temp = line.strip().split()
        if temp[2]=='1':
            badseeds.append(temp[0])
        else:
            goodseeds.append(temp[0])
    file.close()
    print "badSeeds Loaded!"
    return goodseeds,badseeds

def loadusers():
    users = []
    file = open('../../../sssddata/sampleusers.txt','r')
    while 1:
        line = file.readline()
        if line == '':
            break
        temp = line.strip().split()
        if len(temp) > 1:
            users.append(temp[0])
    file.close()
    print "Users Loaded!"
    return users


if __name__ == '__main__':
    outnet,innet =loadnet1('../../../sssddata/following2.txt','../../../sssddata/follower2.txt')
#     global seeds
    goodseeds,badseeds = loadseeds()
    seeds = goodseeds + badseeds
    users = loadusers()
    PR = PageRank(outnet,innet,users)
    PR.initRank(badseeds)
    PR.run(60,1)
    PR.orderRank()
    print PR.order

    
    