'''
Created on 2013-12-24

@author: Administrator
'''

def run():
    infile = open(r'E:\dataset\UDI-TwitterCrawl-Aug2012-Network\network.txt','r')
    #infile1 = ('','r')
    follow = {}
    count = 0
    try:
        while 1:
            if count%100000==0:
                print count
            count += 1
            line = infile.readline()
            if line=='':
                break
            temp = line.strip().split()
            try:
                follow[temp[0]].append(temp[1])
            except:
                follow[temp[0]]=[]          
                follow[temp[0]].append(temp[1])
    finally:
        print len(follow.keys())
        infile.close()

if __name__ == '__main__':
    run()