# -*- coding: utf-8 -*-
'''
Created on 2014-4-10

@author: Administrator
'''



import datetime
import sys, os

startdate = '2011-07-01 00:00:00'

global urlcount
global usercount

def timedelta(curtime):
    starttime = datetime.datetime.strptime(startdate, '%Y-%m-%d %H:%M:%S')
    d = datetime.datetime.strptime(curtime,'%a %b %d %H:%M:%S %Y')
    delta= d - starttime
    return delta.total_seconds()

def istime(temp):
    time = ' '.join(temp[1:5])
    time += ' '+temp[6]
    timejiange = timedelta(time)
    return timejiange


def geturltweets(infilename,outfile,uid):
    infile = open (infilename+'\\'+str(uid),'r')
    global urlcount
    global usercount
    flag=0
    urllist=[]
    url=''
##    print infile.readline()
    while 1:
        line = infile.readline().strip()
##        print line
        if line=='':
            break
        if line=='***' and flag == 0:
            flag = 1
            url=''
            continue
        if line=='***' and flag == 1:
            flag = 0
            continue
        if flag == 1:
            temp = line.split()
            if temp[0]=='URL:' and len(temp)>1:
                urllist += temp[1:]
##                print url
            #if temp[0]=='Time:' and len(url)>0:
            #    jiange = istime(temp)
            #    if jiange > 0 :
            #        urllist.append(url+'\t'+str(jiange))
##                    print url
    if len(urllist)>0:
        usercount += 1
        outfile.write(str(uid)+'\t'+'\t'.join(urllist)+'\n')
##            print item
    infile.close()
                    
            

def run():
    try:
        global urlcount
        global usercount
        urlcount=0
        usercount=0
        file=open(r'../../../sssddata/14wan/14userurls.txt','w')
        infile_dir = r'E:\dataset\tweets'
        Filelist = os.listdir(infile_dir)
        for uid in Filelist:
            geturltweets(infile_dir, file, uid)
            if usercount%100==0:
                print (usercount) 
    finally:
        print 'user:\t'+str(usercount)
        print 'url:\t'+str(urlcount)
        file.close()

    



if __name__=='__main__':
    run()
    
