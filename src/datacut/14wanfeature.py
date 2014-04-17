


import datetime
from datetime import *
import sys, os
import cPickle as pickle 
import math

startdate = '2011-05-01 00:00:00'

global urlcount
global usercount

def timedelta(startdate,curtime):
    #starttime = datetime.datetime.strptime(startdate, '%Y-%m-%d %H:%M:%S')
    starttime = datetime.strptime(startdate, '%a %b %d %H:%M:%S %Y')
    d = datetime.strptime(curtime,'%a %b %d %H:%M:%S %Y')
    delta= d - starttime
    return delta.total_seconds()

def istime(temp):
    time = ' '.join(temp[1:5])
    time += ' '+temp[6]
    timejiange = timedelta(startdate,time)
    return timejiange

def monthder(date1,date2):  
    temp=0
    if int(date2.month) - int(date1.month) <0:
        temp=1
    der=int(date2.month)+(int(date2.year)-int(date1.year))*12-int(date1.month)   
    #der = abs(date1-date2)
    return der

def getcontentfeature(infilename,outfile,uid):
    ##feature: url_ratio oneurl_ratio  mention_raio hash_ratio ret_ratio interval tweet_per_day   
    
    infile = open (infilename+'\\'+str(uid),'r')
    
    global usercount
    usercount += 1
    flag=0
    
    ## metrics
    ntweets = 0.0
    ninterval = 0.0
    nurl = 0.0
    nurl_one = 0.0
    nmention = 0.0
    nret = 0.0
    nhash = 0.0
    ntf = 0.0
    max =''
    min =''
    tweetsid =set()
    first = 1
    empty =True
##    print infile.readline()
    while 1:
        line = infile.readline().strip()
##        print line
        if line=='':
            break
        if line=='***' and flag == 0:
            empty =False
            flag = 1
            continue
        chongfu = 0
        urlcount = 0
        while flag:

            line = infile.readline().strip()
            if line=='***':
                flag = 0
                break
            temp = line.split()
           
            if len(temp)<1 or chongfu ==1:
                continue
            try:
                if temp[0]=='URL:' and len(temp)>1:
                    urlcount= len(temp)-1
                if temp[0]=='ID:' and len(temp)>1:
                    if temp[1] not in tweetsid:
                        tweetsid.add(temp[1])
                        nurl+=urlcount
                        if urlcount == 1:
                            nurl_one += 1
                    else :
                        chongfu = 1
                if temp[0]=='Time:' and len(temp)>0:
                    if first:
                        max = min = ' '.join(temp[1:5])+' '+temp[6]
                        first =0
                    else:
                        time = ' '.join(temp[1:5])+' '+temp[6]
                        if timedelta(max,time)>0:
                            max = time
                        if timedelta(time,min)>0:
                            min = time
                if temp[0]=='RetCount:' and len(temp)>1:
                    nret += int(temp[1])
                    
                if temp[0]=='MentionedEntities:' and len(temp)>1:
                    nmention += len(temp)-1
                    
                if temp[0]=='Hashtags:' and len(temp)>1:
                    nhash += len(temp)-1
            except:
                chongfu = 1
##                    print url
    if empty:
        outfile.write(uid+'\t0\t0\t0\t0\t0\t0\t0\n')
        list = [uid, '0','0','0', '0','0','0','0']
    else:
        ntweets = len(tweetsid)
        delta = timedelta(min,max)
        if delta == 0:
            delta = 1
        ninterval = delta/3600.0/ntweets
        ntf = ntweets/(delta/86400.0)
        list = [uid,  str(nurl/ntweets),str(nurl_one/ntweets),str(nmention/ntweets), str(nhash/ntweets),str(nret/ntweets),str(ninterval),str(ntf)]
        #print usercount,'\t'.join(list)
        outfile.write('\t'.join(list)+'\n')      
##            print item
    infile.close()
    return list
       
def getprofile(file,userset):
    
    
    ## feature: friends follower status ff_ratio age following_rate tweet_rate
    
    fpro = open(r'../../../sssddata/14wan/feature/user_smallnet.txt','r')
    fout = open(file,'w')
    
    today = date(2011,8,1)
    for line in fpro:
        feature=[]
        temp = line.strip().split()
        if temp[0] in userset:
            feature.append(str(math.log(1+float(temp[2]))))
            feature.append(str(math.log(1+float(temp[3]))))
            feature.append(str(math.log(1+float(temp[4]))))
           # feature+=temp[2:5]
            der = 0
            if int(temp[8])>31:
                curdate = ' '.join(temp[6:10]) 
                curtime = datetime.strptime(curdate, '%d %b %Y %H:%M:%S')
                d=curtime.date()
                der = monthder(d,today)
                #print d,today,der
            else:
                c = temp[7:10]
                c.append(temp[11])
                curdate =' '.join(c)
                curtime = datetime.strptime(curdate, '%b %d %H:%M:%S %Y')
                d=curtime.date()
                der = monthder(d,today)
                #print d,today,der
            feature.append(str((float(temp[2])+1)/(float(temp[3])+1)))
            feature.append(str(der))
            feature.append(str(float(temp[2])/der))
            feature.append(str(float(temp[4])/der))
            fout.write(temp[0]+'\t'+'\t'.join(feature)+'\n')
    fpro.close()
    fout.close()       
           

def runcontent(file,userset):
    try:
        global urlcount
        global usercount
        urlcount=0
        usercount=0
        infile_dir = r'E:\dataset\tweets'
        fcontent=open(file,'w')
        for uid in userset:
            content=getcontentfeature(infile_dir, fcontent, uid)
            if usercount%100 == 0:
                print str(usercount)  
                
    finally:
        print 'user:\t'+str(usercount),uid
        fcontent.close()
    
def getGraph(file,user):
    # bi-links
    # bi-links_raio
    # Clustering_Coefficient
    # Eccentricity
    # Closeness
    # Betweenness    
    str2id,id2str = getid2str()
    idfeature = loadgraphfeature('../../../sssddata/14wan/feature/graph/graphfeature.csv')
    graph = {}
    follow, follower = loadnet('../../../sssddata/14wan/1-smallnet.txt')
    fgraph = open(file,'w')
    for uid in follow.keys():
        if uid in user:
            if uid in follower.keys():
                bio = len( follow[uid] & follower[uid] )
            else:
                bio = 0
            graph[uid] = [ str(bio), str( float(bio) / len(follow[uid]) ) ]
            graph[uid] += idfeature[ int(str2id[uid]) ]
            fgraph.write(uid+'\t'+'\t'.join(graph[uid])+'\n')
    for uid in set(follower.keys())-set(follow.keys()):
        if uid in user:
            bio = 1
            graph[uid] = [ '1','1']
            graph[uid] += idfeature[ int(str2id[uid]) ]
            fgraph.write(uid+'\t'+'\t'.join(graph[uid])+'\n')
    fgraph.close()
    print 'get graph feature'
        
    
def getid2str():
    f = open('../../../sssddata/14wan/feature/graph/id2str.txt','r')
    str2id={}
    id2str={}
    for line in f:
        temp = line.strip().split()
        str2id[temp[1]]=temp[0]
        id2str[temp[0]]=temp[1]
    f.close()
    return str2id,id2str

        
def loadgraphfeature(file):
    feature = {}
    for line in open(file,'r'):
        temp=line.strip().split()
        if len(temp)==5:
            feature[int(float(temp[0]))]=temp[1:]
    return feature    

def loadnet(file):
    follow={}
    follower={}
    fsmallnet = open(file,'r')
    for line in fsmallnet:
        temp = line.strip().split()
        try:
            follow[temp[0]].add(temp[1])
        except:
            follow[temp[0]]=set()    
            follow[temp[0]].add(temp[1])  
        try:
            follower[temp[1]].add(temp[0])
        except:
            follower[temp[1]]=set()         
            follower[temp[1]].add(temp[0])
    fsmallnet.close()
    
    return follow,follower

def getNbor(file,user):
    #avg_nbor_followers
    #avg_nbor_tweets
    #fings2_median_followers
    follow, follower = loadnet('../../../sssddata/14wan/1-smallnet.txt')
    fuser = open(r'../../../sssddata/14wan/feature/user_smallnet.txt','r')
    Nr_follow = {}
    Nr_follower = {}
    Nr_status = {}
    for line in fuser:
        temp = line.strip().split()
        if temp[0] in user:
            Nr_follow[temp[0]] = temp[2]
            Nr_follower[temp[0]] = temp[3]
            Nr_status[temp[0]] = temp[4]
    fuser.close()
    
    fnbor = open(file,'w')
    for uid in follow.keys():
        if uid in user:
            nrfor = [ int(Nr_follower[u]) for u in follow[uid] if u in user ]
            nrfor.sort()
            if len(nrfor)==0:
                avg_for = Nr_follower[uid]
            else:
                avg_for = float(sum(nrfor))/len(nrfor)
            
            nrtwt = [int(Nr_status[u]) for u in follow[uid] if u in user]
            nrtwt.sort()
            if len(nrtwt)==0:
                avg_twt = Nr_status[uid]
            else:
                avg_twt = float(sum(nrtwt))/len(nrtwt)
            
            if len(nrfor)==0:
                f2mnf = float(Nr_follow[uid])/float(Nr_follower[uid])
            else:
                m = len(nrfor)/2
                f2mnf = float(Nr_follow[uid]) / nrfor[m]
            fnbor.write('%s\t%s\t%s\t%s\n' %( uid, str(avg_for),str(avg_twt),str(f2mnf) ) )
        
    for uid in set(follower.keys())-set(follow.keys()):
        if uid in user:
            avg_for = Nr_follower[uid]
            avg_twt = Nr_status[uid]
            f2mnf = float(Nr_follow[uid])/float(Nr_follower[uid])
            fnbor.write('%s\t%s\t%s\t%s\n' %( uid, str(avg_for),str(avg_twt),str(f2mnf) ) )
    fnbor.close()
    print 'neighbor feature geted'

if __name__=='__main__':
    user='../../../sssddata/14wan/feature/testset'
    fbad = open(user,'rb')
    userset = pickle.load(fbad)
    fbad.close()
    print len(userset)
    
    runcontent(r'../../../sssddata/14wan/feature/2-content.txt',userset)
    #getprofile(r'../../../sssddata/14wan/feature/2-profile.txt',userset)
    #getGraph('../../../sssddata/14wan/feature/2-graph.txt',userset)
    #getNbor('../../../sssddata/14wan/feature/2-neighbor.txt',userset)
    
