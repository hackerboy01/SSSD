'''
Created on 2014-1-3

@author: Administrator
'''
import math



global Rank
Rank ={}

class PageRank:
    def __init__(self, seeds, outnetwork,innetwork,users):
        self.seeds = seeds
        self.outnetwork = outnetwork
        self.innetwork = innetwork
        self.users = users
        self.Rank={}
        self.a = 0.85
        self.b = 1-self.a
        
    def run(self,iteration=1):
        self.initRank()
        count = 0
        while count < iteration:
            sigma = 0.0
            tempRank = self.Rank.copy()
            for user in self.users:
                temp = 0.0
                for inuser in self.innetwork[user]:
                    temp += tempRank[inuser]/len(self.outnetwork[inuser])
                self.Rank[user] = self.a*temp + self.b*1.0/len(self.users)
            for user in self.users:
                sigma += abs(self.Rank[user]-tempRank[user])
            del tempRank
            count += 1
            print count,sigma
           # if sigma < 1e-10:
                #break
        return self.Rank   

    def initRank(self):
        for user in self.users:
            self.Rank[user]=0.0
            if user in self.seeds:
                self.Rank[user]=1.0/len(self.seeds)
    def showRank(self):
        global Rank
        Rank ={}
        Rank=dict(sorted(self.Rank.iteritems(), key=lambda pair: pair[1], reverse=True))
        all = 0.0
        for it in Rank.keys():
            all += Rank[it]
            
        print all
        print Rank




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
    file = open('../../../sssddata/normalprofile.txt','r')
    goodseeds=[]
    badseeds=[]

    while 1:
        line = file.readline()
        if line == '':
            break
        temp = line.strip().split()
        if len(temp) > 1:
            goodseeds.append(temp[0])
    file.close()
    print "goodSeeds Loaded!"
    file = open('../../../sssddata/spamprofile.txt','r')
    while 1:
        line = file.readline()
        if line == '':
            break
        temp = line.strip().split()
        if len(temp) > 1:
            badseeds.append(temp[0])
    file.close()
    print "badSeeds Loaded!"
    return goodseeds,badseeds

def loadusers():
    users = []
    file = open('../../../sssddata/spamleusers.txt','r')
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
    PR = PageRank(seeds,outnet,innet,users)
    PR.run(300)
    PR.showRank()
    
    