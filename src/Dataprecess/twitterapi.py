# -*- coding: utf-8 -*-
'''
Created on 2014-4-7

@author: Administrator
'''
from twitter import *
import twitter
import sys
import time

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

fuids = open("../../../sssddata/badorder-1.txt", "r")
fspam = open("../../../sssddata/badorder-3.txt", "w")

try:    
    counter = 0
    spamcounter = 0
    tflag = 0
    for line in fuids:
        flag = True
        tm = 30
        temp = line.strip().split()
        uname = temp[0]
        while flag:
            try:     
                if tflag == 1:
                    print 'user 1'
                    t = twitter
                else :
                    print 'user 2'
                    t = twitter1
                profile = t.users.show(screen_name = uname)
                name = profile['screen_name']
                if name.strip():
                    fspam.write('\t'.join(temp)+'\t0\n')
                else:
                    fspam.write('\t'.join(temp)+'\t1\n')
                    print '********'
                    spamcounter += 1
                flag = False
            except Exception, e:
                print >> sys.stderr, 'on_status: Encountered Exception:', e
                if str(e).find('Rate limit')>0:
                    flag = True
                    print 'sleep',tm
                    time.sleep(float(tm))
                    tm= tm*2
                    if tflag == 1:
                        tflag =0
                    else:
                        tflag =1
                elif str(e).find('not exist')>0:
                    fspam.write('\t'.join(temp)+'\t1\n')  
                    spamcounter += 1
                    flag = False
                    print 'Sorry, that page does not exist'
                    print "spam =", spamcounter
                else :
                    fspam.write('\t'.join(temp)+'\t2\n')  
                    spamcounter += 1
                    flag = False
                    print "spam =", spamcounter
        counter += 1
        print counter,temp[0]
except Exception, e:
     print e   
finally:
    fspam.close()
    fuids.close()
