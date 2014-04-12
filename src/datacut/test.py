# -*- coding: utf-8 -*-
'''
Created on 2014-4-12

@author: Administrator
'''
import sys, os
import cPickle as pickle 

outfspam = open(r'../../../sssddata/14wan/14spamsuspend','rb')
fout = open(r'../../../sssddata/14wan/spamsuspend.txt','w')
fuser = open(r'../../../sssddata/users.txt','r')
allusers = set()
for line in fuser:
    temp = line.strip().split()
    if len(temp)>0:
        allusers.add(temp[0])

spamset =pickle.load(outfspam)
spamset = spamset&allusers
for user in spamset:
    fout.write(user+'\n')
fout.close()
outfspam.close()