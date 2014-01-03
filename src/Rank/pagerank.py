'''
Created on 2014-1-3

@author: Administrator
'''

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
            tempRank = self.Rank.copy()
            for user in self.users:
                temp = 0.0
                for inuser in self.innetwork[user]:
                    temp += tempRank[inuser]/len(self.outnetwork[inuser])
                self.Rank[user] = self.a*temp + self.b*1.0/len(self.users)
            del tempRank
        return self.Rank   

    def initRank(self):
        for user in self.users:
            self.Rank[user]=0.0
            if user in self.seeds:
                self.Rank[user]=1.0/len(self.seeds)




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
    users = []
    while 1:
        line = file.readline()
        if line == '':
            break
        temp = line.strip().split()
        if len(temp) > 1:
            goodseeds.append(temp[0])
    file.close()
    file = open('../../../sssddata/spamprofile.txt','r')
    print "goodSeeds Loaded!"
    while 1:
        line = file.readline()
        if line == '':
            break
        temp = line.strip().split()
        if len(temp) > 1:
            badseeds.append(temp[0])
    file.close()
    print "badSeeds Loaded!"
    
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
    return goodseeds,badseeds


if __name__ == '__main__':
    network,network2 =loadnet1('../../../sssddata/following2.txt','../../../sssddata/follower2.txt')
#     global seeds
    goodseeds,badseeds = loadseeds()

    