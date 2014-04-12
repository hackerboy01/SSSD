


import datetime
import sys, os
import cPickle as pickle 

startdate = '2011-05-01 00:00:00'

global userurls
global urlcount
global usercount
global urlsset

urlsset=set()



def geturltweets(infilename,uid):
    infile = open (infilename+'\\'+str(uid),'r')
    global userurls
    global usercount
    usercount += 1
    flag=0
    global urlsset
    ## metrics

    nurl = 0.0
    
    tweetsid =set()
    urlset = set()
    
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
        urlone = []
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
                    urlone = temp[1:]                    
                    urlsset.update(urlone)
               # if temp[0]=='ID:' and len(temp)>1:
                #    if temp[1] not in tweetsid:
                #        tweetsid.add(temp[1])
                        #urlset.update(urlone)
               #     else :
               #         chongfu = 1
            except:
                chongfu = 1
##                    print url

    #userurls[uid]=urlset
   # print usercount,uid, len(urlset)
##            print item
    infile.close()
                    
def UrlSimilarity(fout,uidlist):
    global userurls
    for x in range(0,len(uidlist)-1):
        share = 0
        nshare = 0
        for y in range(x+1,len(uidlist)):
            share = len(userurls[uidlist[x]] & userurls[uidlist[y]])
            if share>0:
                nshare+=1
                fout.write(str(uidlist[x])+'\t'+str(uidlist[y])+'\t'+str(float(share)/(len(userurls[uidlist[x]] | userurls[uidlist[y]])))+'\n')
        print x,nshare    

def run():
    try:
        global userurls
        global usercount
        global urlcount
        global urlsset
        usercount=0
        userurls={}
        urltoid={}
        usernet = {}
        #file=open(r'../../../sssddata/14wan/14userurls.txt','r')
        fsimi = open(r'../../../sssddata/14wan/14wanurlshare.txt','r')
        for line in fsimi:
            usercount +=1
            if usercount %100000 ==0:
                print usercount
            temp = line.strip().split()
            try:
                usernet[temp[0]][temp[1]]=float(temp[2])
            except:
                usernet[temp[0]]={}
                usernet[temp[0]][temp[1]]=float(temp[2])
            try:
                usernet[temp[1]][temp[0]]=float(temp[2])
            except:
                usernet[temp[1]]={}
                usernet[temp[1]][temp[0]]=float(temp[2])
        
        
        #=======================================================================
        # for line in file:
        #     usercount += 1
        #     temp = line.strip().split()
        #     userurls[temp[0]]=set(temp[1:])
        #     if usercount %100==0:
        #         print usercount
        # UrlSimilarity(fsimi,userurls.keys())
        #=======================================================================
        
        
        #=======================================================================
        # infile_dir = r'E:\dataset\tweets'
        # temp = open(r'../../../sssddata/14wan/urltoid','wb')
        # Filelist = os.listdir(infile_dir)
        # for uid in Filelist:
        #     geturltweets(infile_dir, uid)
        #     if usercount%100 == 0:
        #         print str(usercount),len(urlsset),sys.getsizeof(urlsset)
        # urlcount=0
        # for u in urlsset:
        #     urltoid[u]=urlcount
        #     if urlcount%5000==0:
        #         print urlcount,'url to id'
        #         pickle.dump(urltoid, temp)
        #     urlcount+=1
        # 
        #=======================================================================
            #if usercount%1000 == 0:
            #    pickle.dump(userurls, temp)
        
        #userurls = pickle.load(temp)
       # print userurls
        
        
    finally:
        #print 'user:\t'+str(usercount),uid
       # temp.close()
       print usercount
       fsimi.close()
    



if __name__=='__main__':
    run()
    
