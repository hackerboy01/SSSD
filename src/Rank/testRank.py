'''
Created on 2014-4-17

@author: Administrator
'''


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


if __name__ == '__main__':
    #runAntiTrustrank()
    runTrustrank()
    pass