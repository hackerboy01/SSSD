'''
Created on 2014-4-17

@author: Administrator
'''
import pickle

def runTrustrank():
    file = open('../../../sssddata/14wan/rank/Trustrank_seeds50','r')
    count = 0
    spamdic={}
    spamnum = 0
    for line in file:
        count += 1
        temp = line.strip().split()
        if len(temp)==3:
            spamnum+=1
        if count%1000==0:
            spamdic[count]=spamnum
            spamnum=0
    spamdic[count]=spamnum
    keys = spamdic.keys()
    keys.sort()
    for it in keys:
        print  spamdic[it]
    print sum(spamdic.values())

def runAntiTrustrank():
    file = open('../../../sssddata/14wan/rank/2-anti-Trustrank_seeds200','r')
    count = 0
    spamdic={}
    spamnum = 0
    for line in file:
        count += 1
        temp = line.strip().split()
        if len(temp)==3:
            spamnum+=1
        if count%100==0:
            spamdic[count]=spamnum
            spamnum=0
    file.close()
    spamdic[count]=spamnum
    keys = spamdic.keys()
    keys.sort()
    for it in keys:
        print  spamdic[it]
    print sum(spamdic.values())

def runSpamRank():
    #file = open('../../../sssddata/14wan/rank/2-spamrank_seeds50','r')
    file = open('../../../sssddata/14wan/rank/2-spamrank_linear_seeds50','r')
    count = 0
    spamdic={}
    spamnum = 0
    for line in file:
        count += 1
        temp = line.strip().split()
        if len(temp)==3:
            spamnum+=1
        if count%1000==0:
            spamdic[count]=spamnum
            spamnum=0
    file.close()
    spamdic[count]=spamnum
    keys = spamdic.keys()
    keys.sort()
    for it in keys:
        print  spamdic[it]
    print sum(spamdic.values())

def temp():
    import pagerank as PR
    p1=PR.PageRank(rankname='a')
    p1.Rank['a']=1
    p2=PR.PageRank(rankname='b')
    p2.Rank['a']=2
    print p1.rankname,p2.rankname
    print p1.Rank['a'],p2.Rank['a']
 
def spampredict():
    fin = open('../../../sssddata/14wan/newspam_3times','rb')
    newspam1 = pickle.load(fin)
    fin.close()    
    fin = open('../../../sssddata/14wan/newspam_4times','rb')
    newspam2 = pickle.load(fin)
    fin.close()    
    newspam = newspam1 &newspam2
    print len(newspam1),len(newspam2),len(newspam)
    
    fuser = open(r'../../../sssddata/users.txt','r')
    fout = open('../../../sssddata/14wan/newspam_label','w')
    for line in fuser:
        temp = line.strip().split()
        if len(temp)>0:
           if temp[0] in newspam:
               fout.write(temp[1]+'\n')
    fout.close() 
    fuser.close()  
    
    
    
if __name__ == '__main__':
    #runAntiTrustrank()
    #runTrustrank()
    #runSpamRank()
    #temp()
    spampredict()
    pass