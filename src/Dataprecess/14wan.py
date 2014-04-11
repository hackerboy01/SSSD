# -*- coding: utf-8 -*-
'''
Created on 2014-4-7

@author: Administrator
'''
from twitter import *
import twitter
import sys
import time
import os
import cPickle as cp

consumer_key = "m2JZ46Fqku01WXHwiSwfVA"
consumer_secret = "VR4qrsasxySSVr1CoHIGsnXdSR2ETbtticB6lLzbrs"
access_key = "1420145084-CyV5adA1fBL9ROSVACbhBE60gzwPljHRxFqfx4L"
access_secret = "Ru1jwyNrtmRVTFnR9VV5j6CaZcOjbXcO1wv5bJNQSQ"
auth = OAuth(access_key, access_secret, consumer_key, consumer_secret)
twitter = Twitter(auth = auth)

consumer_key1 = "pu8XMWkCatUfkcRSr1rmEA"
consumer_secret1 = "xzDm3XJdfPJngP4zQZudi4NCZVDDVQ45Hat1UtIvZM"
access_key1 = "1420145084-w8CZnp1R8ssZl0MferAZzdOX5ibgWpzBPAwPpqQ"
access_secret1 = "jfO2lw8PU6NQbDw8KbHben9CVrRsBl6O20tr2riFez0HH"
auth1 = OAuth(access_key1, access_secret1, consumer_key1, consumer_secret1)
twitter1 = Twitter(auth = auth1)

consumer_key2 = "3nDGkzmFz8gqDYkKwVlHXBbEM"
consumer_secret2 = "negXCyUUW5zqmSsP11zW4aD0tStlp6gFRrjvcy8THXc5CHVavf"
access_key2 = "1420145084-kRgSt3VVllQ950Ep8dazQnvuzdnCJQ03UIOMMr1"
access_secret2 = "fnJDseH5el73wBpUnWqzrb2T7ch6I3hP4ql8C7qVYrLqn"
auth2 = OAuth(access_key2, access_secret2, consumer_key2, consumer_secret2)
twitter2 = Twitter(auth = auth2)

consumer_key3 = "GTC73QeOy4txZogymAawfbzLW"
consumer_secret3 = "bpQcKgkJWDZIsXa28VKeGNNWAnG2FurYTDJdyZTWTlie5D5REe"
access_key3 = "1420145084-zVaOiJQQNJjUBbTOXgUXLOqUdcAvI4Wj6vplnKz"
access_secret3 = "2ne94U6mgPEhVoUtytyiFcK0SB3fDDUR0HXB8drsQAdfi"
auth3 = OAuth(access_key3, access_secret3, consumer_key3, consumer_secret3)
twitter3 = Twitter(auth = auth3)



flist = os.listdir("E:/dataset/tweets/")
ftemp = open("../../../sssddata/14wan/14wanlabel-new1.txt", "r")
fspam = open("../../../sssddata/14wan/14wanlabel-spam.txt", "w")

fsuspend = open("../../../sssddata/14wan/14spamsuspend.txt", "wb")
suspend = set()

fnotexist = open("../../../sssddata/14wan/14spamnotexist.txt", "wb")
notexist = set()

L = 0
userlabel={}
for line in ftemp:
    temp = line.strip().split()
    userlabel[temp[0]] = int(temp[1])
    #fspam.write(line)
    L+=1
    
ftemp.close()

print L

count = 0
for uid in flist:
    count += 1
    a=userlabel[uid]
    if count%10000==0:
        print count

try:    
    counter = 0
    spamcounter = 0
    tflag = 0
    for uid in flist:
        counter += 1
        try:
            if userlabel[uid]==0:
                continue
        except:
            print counter,uid
            continue
##	if counter <= L:
##            continue
        flag = True
        tm = 10
        while flag:
            try:     
                if tflag%4==0:
                    #print 'user 1'
                    t = twitter3
                elif tflag%4 == 1:
                    #print 'user 2'
                    t = twitter2
                elif tflag%4 == 2:
                    t = twitter1
                    #print 'user 3'
                else:
                    t = twitter
                    #print 'user 4'
                profile = t.users.show(user_id = uid)
                name = profile['screen_name']
                if name.strip():
                    print uid
                    fspam.write(uid+'\t0\n')
                else:
                    fspam.write(uid+'\t1\n')
                    print '********'
                    spamcounter += 1
                flag = False
            except Exception, e:
                #print >> sys.stderr, 'on_status: Encountered Exception:', e
                if str(e).find('Rate limit')>0:
                    flag = True
                    print 'sleep',tm
                    time.sleep(float(tm))
                    tm= tm*2
                    tflag+=1
                elif str(e).find('not exist')>0:
                    notexist.add(uid)
                    fspam.write(uid+'\t'+str(userlabel[uid])+'\t1\n')  
                    spamcounter += 1
                    flag = False
                    #print 'Sorry, that page does not exist'
                    print uid,userlabel[uid],'1', spamcounter
                else :
                    suspend.add(uid)
                    fspam.write(uid+'\t'+str(userlabel[uid])+'\t2\n')  
                    spamcounter += 1
                    flag = False
                    print uid,userlabel[uid],'2', spamcounter
        #print counter,uid
except Exception, e:
     print e   
finally:
    cp.dump(suspend,fsuspend)
    cp.dump(notexist,fnotexist)
    fsuspend.close()
    fnotexist.close()
    fspam.close()
