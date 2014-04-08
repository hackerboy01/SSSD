'''
Created on 2014-3-24

@author: Administrator
'''

if __name__ == '__main__':
    inbad = open('../../../sssddata/badorder.txt','r')
    inlabel = open('../../../sssddata/Label-1.txt','r')
    outlabel = open('../../../sssddata/badorder-1.txt','w')
    inuser = open('../../../sssddata/sampleusers.txt','r')
    
    users={}
    for line in inuser:
        temp=line.strip().split()
        users[temp[0]]=temp[1]
 
    label = {}
    for line in inlabel:
        temp = line.strip().split()
        label[temp[1]]=temp[2:]
    
    for line in inbad:
        temp=line.strip().split()
        outlabel.write(str(users[temp[0]])+'\t'+str(temp[0])+'\t\t\t'+str('\t'.join(label[temp[0]]))+'\n')
    
    inlabel.close()
    outlabel.close()
    inuser.close()
    inbad.close()