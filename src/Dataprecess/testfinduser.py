'''
Created on 2013-12-24

@author: Administrator
'''
import os

def run():
    infile = open('../../sssddata/evaluateResult.txt','r')
    infile2 = open('../../sssddata/restGroups.txt','r')
    infile3 = open('../../sssddata/users.txt','r')
    outfile = open('../../sssddata/spamprofile.txt','w')
    outfile1 = open('../../sssddata/normalprofile.txt','w')
    
    spamlist=[]
    normallist=[]
    mixlist = []
    snlist = []
    while 1:
        line = infile.readline()
        if line=='':
            break
        line = line.strip()
        if len(line)>0:
            temp = line.split()
            if temp[0]=='spam':
                spamlist += temp[2:]
                
            if temp[0]=='normal':
                normallist += temp[2:]  
            if temp[0]=='mixed':
                mixlist += temp[2:]        
            #print temp
    print 'spam:\t',len(spamlist)
    print 'normal:\t',len(normallist)
    print 'mix:\t',len(mixlist)
    snlist = spamlist + normallist
    testlist = []
    while 1:
      line = infile2.readline()
      if line=='':
          break
      line = line.strip()
      if len(line)>0:
          temp = line.split()
          testlist += temp
    
    print len(testlist)
    
    userlist = []
    filelist = os.listdir(r'E:\dataset\tweets')
    while 1:
      line = infile3.readline()
      if line=='':
          break
      line = line.strip()
      if len(line)>0:
          temp = line.split()
          if len(temp)>2:
              if temp[1] in spamlist:
                  outfile.write('\t'.join(temp)+'\n')
                  userlist.append(temp[0])
                  print temp[1]
              if temp[1] in normallist:
                  outfile1.write('\t'.join(temp)+'\n')
                  userlist.append(temp[0])
                  print temp[1]
    lastlist = list(set(userlist)&set(filelist))            
    
    print len(lastlist)
    outfile.close()
    outfile1.close()
    infile2.close()
    infile.close()



if __name__ == '__main__':
    run()