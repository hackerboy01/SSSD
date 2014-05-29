'''
Created on 2014-1-3

@author: Administrator
'''
import math
import cPickle as pickle 


global Rank
Rank ={}



class PageRank:
    def __init__(self,outnetwork={},innetwork={},users=set(),Rank={},rankname=''):
        self.seeds = set()
        self.outnetwork = outnetwork
        self.innetwork = innetwork
        self.users = users
        if len(Rank.keys())==0:
            self.Rank={}
        else:
            self.Rank=Rank
        self.a = 0.85
        self.b = 1-self.a
        self.order=[]
        self.netweight={}
        self.rankname=rankname
        
    def run(self,iteration=1,good=1.0,TrustRank=False):
        #self.initRank()
        count = 0
        while count < iteration:
            sigma = 0.0
            tempRank = self.Rank.copy()
            for user in self.users:
                temp = 0.0
                flag=False
                try:
                    indegree=self.innetwork[user]
                except:
                    indegree=[]
                    flag = True
                for inuser in indegree:
                    temp += tempRank[inuser]/len(self.outnetwork[inuser])
                    
                    
                if TrustRank:
                    if user in self.seeds:
                        good = 1.0
                    else :
                        good = 0.0
                    #===========================================================
                    # if flag:
                    #     temp = tempRank[user]
                    #===========================================================
                    self.Rank[user] = self.a*temp + self.b*good/len(self.seeds)
                else:
                    #===========================================================
                    # if flag:
                    #     temp = tempRank[user]
                    #===========================================================
                    self.Rank[user] = self.a*temp + self.b*good/len(self.users)
                    
            for user in self.users:
                sigma += abs(self.Rank[user]-tempRank[user])
            del tempRank
            count += 1
            if __name__ == '__main__':
                print count,sigma#,self.showRank()
            
            if sigma < 1e-8:
                break
        return self.Rank   

    def runwithweight(self,iteration=1,good=1.0):
        count = 0
        while count < iteration:
            sigma = 0.0
            tempRank = self.Rank.copy()
            for user in self.users:
                temp = 0.0
                for inuser in self.network[user]:
                    temp += tempRank[inuser] * self.network[user][inuser]  
                if user in self.seeds:
                    good = 1.0
                else :
                    good = 0.0                             
                self.Rank[user] = self.a*temp + self.b*good/len(self.seeds)                 
            for user in self.users:
                sigma += abs(self.Rank[user]-tempRank[user])
            del tempRank
            count += 1
            if __name__ == '__main__':
                print count,sigma#,self.showRank()
            if sigma < 1e-8:
                break
        return self.Rank 
        
        
    def loadweight(self,filename):
        network = {}
        allweight = {}
        with open(filename,'r') as file:
            for line in file:
                temp = line.strip().split()
                self.users.update(temp[0:2])
                try:
                    network[temp[0]][temp[1]]=float(temp[2])
                except:
                    network[temp[0]]={}
                    network[temp[0]][temp[1]]=float(temp[2])
                try:
                    network[temp[1]][temp[0]]=float(temp[2])
                except:
                    network[temp[1]]={}
                    network[temp[1]][temp[0]]=float(temp[2])
            
        for uid in network.keys():
            nor = sum(network[uid].values())
            for u in network[uid]:
                network[uid][u]=network[uid][u]/nor
        print 'net with weight load'
        self.netweight=network
    def initNet(self,file,reverse=False):
        net = open(file,'r')
        self.outnetwork ={}
        self.innetwork = {}
        for line in net:
            temp = line.strip().split()
            self.users.update(temp)
            if reverse==False:
                try:
                    self.outnetwork[temp[0]].append(temp[1])
                except:
                    self.outnetwork[temp[0]]=[]
                    self.outnetwork[temp[0]].append(temp[1])
                try:
                    self.innetwork[temp[1]].append(temp[0])
                except:
                    self.innetwork[temp[1]]=[]
                    self.innetwork[temp[1]].append(temp[0])
            else:
                try:
                    self.outnetwork[temp[1]].append(temp[0])
                except:
                    self.outnetwork[temp[1]]=[]
                    self.outnetwork[temp[1]].append(temp[0])
                try:
                    self.innetwork[temp[0]].append(temp[1])
                except:
                    self.innetwork[temp[0]]=[]
                    self.innetwork[temp[0]].append(temp[1])
        net.close()
        print 'Net load!'
                 
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
        #print self.showRank()
    def orderRank(self,reverse=True):
        self.order=sorted(self.Rank.iteritems(), key=lambda pair: pair[1], reverse=reverse)  
        return self.order       
    def showRank(self):
        return self.Rank
        




def loadnet(outdegree,indegree):
    follow = {}
    follower = {}
    userset = set()
    file = open(outdegree,'r')
    count = 0
    while 1:
        line = file.readline()
        if line == '':
            break
        temp = line.strip().split()
        if len(temp)>1:
            userset.update(temp)
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
            userset.update(temp)
            follower[temp[0]]=temp[1:]
    print "in Network Loaded!"
    file.close()
    return follow, follower,userset

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



def netweight(filename):
    fbad = open('../../../sssddata/14wan/rank/14spamsuspend','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    print len(spamset)
    network = {}
    allweight = {}
    userset=set()
    with open(filename,'r') as file:
        for line in file:
            temp = line.strip().split()
            userset.update(temp[0:2])
            try:
                network[temp[0]][temp[1]]=float(temp[2])
            except:
                network[temp[0]]={}
                network[temp[0]][temp[1]]=float(temp[2])
            try:
                network[temp[1]][temp[0]]=float(temp[2])
            except:
                network[temp[1]]={}
                network[temp[1]][temp[0]]=float(temp[2])
        
    for uid in network.keys():
        nor = sum(network[uid].values())
        if uid in spamset:
            print nor,len(network[uid].keys()),'spam'
        else:
            print nor,len(network[uid].keys())
        for u in network[uid]:
            network[uid][u]=network[uid][u]/nor
        #print network[uid]
    print 'net with weight load',len(userset),len(userset&spamset)
    return network
    
    
def runTrustrank(netname = '1-smallnet-bio.txt' ,tao = 200):   
    #netname = '2-smallnet-bio.txt' 
    fbad = open('../../../sssddata/14wan/spamset_bio','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    #print len(spamset)
    PR=PageRank()
    PR.initNet('../../../sssddata/14wan/rank/'+netname,reverse=True)
    PR.initRank(spamset)
    PR.run(100, good=1.0, TrustRank=False)
    order = PR.orderRank()
    
    ftest = open('../../../sssddata/14wan/rank/pagerank','w')
    count  = 0
    seeds=set()
    for item in order:
        uid,pr=item
        if uid not in spamset:
            count += 1
            if count < tao:
                seeds.add(uid)
            #ftest.write(str(uid)+'\t'+str(pr)+'\tspam\n')
        else:
            #ftest.write(str(uid)+'\t'+str(pr)+'\n')
            pass
    ftest.close()    
    
    PR.initNet('../../../sssddata/14wan/rank/'+netname,reverse=False)
    PR.initRank(seeds)
    PR.run(100, good=1.0, TrustRank=True)
    order = PR.orderRank()
    
    ftest = open('../../../sssddata/14wan/rank/2-Trustrank_seeds'+str(tao),'w')
    for item in order:
        uid,pr=item
        if uid in spamset:
            if uid not in seeds:
                ftest.write(str(uid)+'\t'+str(pr)+'\tspam\n')
            else:
                ftest.write(str(uid)+'\t'+str(pr)+'\tspam\n')
        else:
            if uid in seeds:
                ftest.write(str(uid)+'\t'+str(pr)+'\tgood seeds\n')
            else:
                ftest.write(str(uid)+'\t'+str(pr)+'\n')
    ftest.close()    
    return PR.showRank().copy()
 
def runPageRank(netname = '1-smallnet-bio.txt',tao = 200):
    fbad = open('../../../sssddata/14wan/spamset_bio','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    #print len(spamset)
    PR=PageRank()
    PR.initNet('../../../sssddata/14wan/rank/'+netname,reverse=False)
    PR.initRank(spamset)
    #print len(PR.users)
    PR.run(100, good=1.0, TrustRank=False)    
    return PR.showRank().copy()
    
def runAntiTrustrank(netname = '1-smallnet-bio.txt',tao = 200):    
    
    #netname = '2-smallnet-bio.txt'
    fbad = open('../../../sssddata/14wan/spamset_bio','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    #print len(spamset)
    PR=PageRank()
    PR.initNet('../../../sssddata/14wan/rank/'+netname,reverse=False)
    PR.initRank(spamset)
    #print len(PR.users)
    PR.run(100, good=1.0, TrustRank=False)
    order = PR.orderRank()
    
    ftest = open('../../../sssddata/14wan/rank/pagerank','w')
    count  = 0
    seeds=set()
    for item in order:
        uid,pr=item
        if uid in spamset:
            count += 1
            if count < tao:
                seeds.add(uid)
            ftest.write(str(uid)+'\t'+str(pr)+'\tspam\n')
        else:
            ftest.write(str(uid)+'\t'+str(pr)+'\n')
            pass
    ftest.close()    
    
    PR.initNet('../../../sssddata/14wan/rank/'+netname,reverse=True)
    PR.initRank(spamset)
    PR.run(100, good=1.0, TrustRank=True)
    order = PR.orderRank()
    
    
    
    
    ftest = open('../../../sssddata/14wan/rank/2-anti-Trustrank_seeds'+str(tao),'w')
    for item in order:
        uid,pr=item
        if uid in spamset:
            if uid in seeds:
                ftest.write(str(uid)+'\t'+str(pr)+'\tspam\tspam\n')
            else:
                ftest.write(str(uid)+'\t'+str(pr)+'\tspam\n')
        else:
            ftest.write(str(uid)+'\t'+str(pr)+'\n')
    ftest.close()    
    return PR.showRank().copy(),seeds

def runAntiTrustrank_new(netname = '1-smallnet-bio.txt',tao = 200):    
    
    #netname = '2-smallnet-bio.txt'
    fbad = open('../../../sssddata/14wan/spamset_bio','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    #print len(spamset)
    PR=PageRank()
    PR.initNet('../../../sssddata/14wan/rank/'+netname,reverse=False)
    PR.initRank(spamset)
    #print len(PR.users)
    PR.run(100, good=1.0, TrustRank=False)
    order = PR.orderRank()
    
    #===========================================================================
    # ftest = open('../../../sssddata/14wan/rank/pagerank','w')
    # count  = 0
    # seeds=set()
    # for item in order:
    #     uid,pr=item
    #     if uid in spamset:
    #         count += 1
    #         #if count < tao:
    #         seeds.add(uid)
    #         ftest.write(str(uid)+'\t'+str(pr)+'\tspam\n')
    #     else:
    #         ftest.write(str(uid)+'\t'+str(pr)+'\n')
    #         pass
    # ftest.close()    
    #===========================================================================
    
    PR.initNet('../../../sssddata/14wan/rank/'+netname,reverse=True)
    PR.initRank(spamset)
    PR.run(100, good=1.0, TrustRank=True)
    order = PR.orderRank()
    
    fin = open('../../../sssddata/14wan/newspam_4times','rb')
    newspam = pickle.load(fin)
    fin.close()
    
    
    
    ftest = open('../../../sssddata/14wan/rank/3-anti-Trustrank_seeds785','w')
    for item in order:
        uid,pr=item
        if uid in spamset:
            #if uid in seeds:
            ftest.write(str(uid)+'\t'+str(pr)+'\tspam\tspam\n')
        elif uid in newspam:
                ftest.write(str(uid)+'\t'+str(pr)+'\tspam\n')
        else:
            ftest.write(str(uid)+'\t'+str(pr)+'\n')
    ftest.close()    
    return PR.showRank().copy()
 
 
def SpamRank():
    tao = 800
    netname = '1-smallnet-bio.txt'
    fbad = open('../../../sssddata/14wan/spamset_bio','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    antiRank,seeds = runAntiTrustrank(netname = netname , tao = tao)
    print "anti Rank!"
    
    #trustRank = runTrustrank(netname = netname , tao = tao)
    trustRank = runPageRank(netname = netname , tao = tao)
    print "trust rank"
    print len(antiRank.keys()),len(trustRank.keys())
    spamrank={}
    for user in antiRank.keys():
        if trustRank[user]==0:
            print user
        #spamrank[user]=float(antiRank[user])/float(trustRank[user])
        spamrank[user]=float(antiRank[user])-float(trustRank[user])
        #print antiRank[user],trustRank[user],spamrank[user]
    order = sorted(spamrank.iteritems(), key=lambda pair: pair[1], reverse=False)  
    ftest = open('../../../sssddata/14wan/rank/2-spamrank_linear_seeds'+str(tao),'w')
    for item in order:
        uid,pr=item
        if uid in spamset:
            if uid in seeds:
                ftest.write(str(uid)+'\t'+str(pr)+'\tspam\tspam\n')
            else:
                ftest.write(str(uid)+'\t'+str(pr)+'\tspam\n')
        else:
            ftest.write(str(uid)+'\t'+str(pr)+'\n')
    ftest.close()    
def SpamRank_new():
    tao = 800
    netname = '1-smallnet-bio.txt'
    fbad = open('../../../sssddata/14wan/spamset_bio','rb')
    spamset = pickle.load(fbad)
    fbad.close()
    antiRank = runAntiTrustrank_new(netname = netname , tao =tao)
    print "anti Rank!"
    
    trustRank = runTrustrank(netname = netname , tao = tao)
    #trustRank = runPageRank(netname = netname , tao = tao)
    print "trust rank"
    print len(antiRank.keys()),len(trustRank.keys())
    spamrank={}
    for user in antiRank.keys():
        if trustRank[user]==0:
            print user
        #spamrank[user]=float(antiRank[user])/float(trustRank[user])
        spamrank[user]=float(antiRank[user])-float(trustRank[user])
        #print antiRank[user],trustRank[user],spamrank[user]
    order = sorted(spamrank.iteritems(), key=lambda pair: pair[1], reverse=True)  
    
    fin = open('../../../sssddata/14wan/newspam_4times','rb')
    newspam = pickle.load(fin)
    fin.close()
    
    ftest = open('../../../sssddata/14wan/rank/2-spamrank_linear_seeds'+str(tao),'w')
    for item in order:
        uid,pr=item
        if uid in spamset:
           # if uid in seeds:
            ftest.write(str(uid)+'\t'+str(pr)+'\tspam\tspam\n')
        elif uid in newspam:
                ftest.write(str(uid)+'\t'+str(pr)+'\tspam\n')
        else:
            ftest.write(str(uid)+'\t'+str(pr)+'\n')
    ftest.close()    
    
    
    
    
if __name__ == '__main__':
#===============================================================================
#     outnet,innet =loadnet1('../../../sssddata/following2.txt','../../../sssddata/follower2.txt')
# #     global seeds
#     goodseeds,badseeds = loadseeds()
#     seeds = goodseeds + badseeds
#     users = loadusers()
#     PR = PageRank(outnet,innet,users)
#     PR.initRank(badseeds)
#     PR.run(200,1)
#     PR.orderRank()
#     fbadorder = open('../../../sssddata/badorder.txt','w')
#     for item in PR.order:
#         if item[0] not in seeds:
#             fbadorder.writelines(str(item[0])+'\n')
#     fbadorder.close()
#===============================================================================
    #===========================================================================
    # fbad = open('../../../sssddata/14wan/spamset_bio','rb')
    # spamset = pickle.load(fbad)
    # fbad.close()
    # print len(spamset)
    #===========================================================================
    
    #===========================================================================
    # outnet,innet,users =loadnet('../../../sssddata/14wan/1-outnet.txt','../../../sssddata/14wan/1-innet.txt')
    # print len(users)
    # PR=PageRank(outnetwork = outnet,innetwork = innet,users=users)
    #===========================================================================   
   # SpamRank_new()
    runTrustrank()
    #runAntiTrustrank_new()
    #network=netweight('../../../sssddata/14wan/rank/urlsharenet.txt')
    #print len(network.keys())


    