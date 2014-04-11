


import datetime
import sys, os

startdate = '2011-05-01 00:00:00'

global urlcount
global usercount

def timedelta(startdate,curtime):
    #starttime = datetime.datetime.strptime(startdate, '%Y-%m-%d %H:%M:%S')
    starttime = datetime.datetime.strptime(startdate, '%a %b %d %H:%M:%S %Y')
    d = datetime.datetime.strptime(curtime,'%a %b %d %H:%M:%S %Y')
    delta= d - starttime
    return delta.total_seconds()

def istime(temp):
    time = ' '.join(temp[1:5])
    time += ' '+temp[6]
    timejiange = timedelta(startdate,time)
    return timejiange


def geturltweets(infilename,outfile,uid):
    infile = open (infilename+'\\'+str(uid),'r')
    
    global usercount
    usercount += 1
    flag=0
    
    ## metrics
    ntweets = 0.0
    ninterval = 0.0
    nurl = 0.0
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
    else:
        ntweets = len(tweetsid)
        delta = timedelta(min,max)
        if delta == 0:
            delta = 1
        ninterval = delta/3600.0/ntweets
        ntf = ntweets/(delta/86400.0)
        list = [uid, str(ntweets), str(nurl/ntweets), str(nmention/ntweets), str(nhash/ntweets),str(nret/ntweets),str(ninterval),str(ntf)]
        #print usercount,'\t'.join(list)
        outfile.write('\t'.join(list)+'\n')
        
##            print item
    infile.close()
                    
            

def run():
    try:
        global urlcount
        global usercount
        urlcount=0
        usercount=0
        file=open(r'../../../sssddata/14wan/14wanfeature.txt','w')
        infile_dir = r'E:\dataset\tweets'
        Filelist = os.listdir(infile_dir)
        for uid in Filelist:
            geturltweets(infile_dir, file, uid)
            if usercount%100 == 0:
                print str(usercount)  
    finally:
        print 'user:\t'+str(usercount),uid
        file.close()
    



if __name__=='__main__':
    run()
    
