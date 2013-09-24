#CS4780 Assignemt2 Problem3
#Data Structure for TDIDT
#The tree is implemented as a list of nodes.
#Each node of the tree is a list which is in the following format
#[int value, list split, int leftindex, int rightindex, int depth]
#value: the prediction of the node: 1=+ 0=- -1=undecided
#split: list in format [int,int] the first entry: 0=x 1=7
#                                the second entry: the threshold value
#leftindex: the relative index of the root node of left subtree (currentindex+leftindex gives the index in the tree list) 
#rightindex: the relative index of the root node of right subtree 
import os
import os
import random
from math import *

#---reading input---
train=[]
with open("groups.train") as f:
  index=0
  for line in f:
    org=line
    train.append([0]*2001)
    sep=line.partition(' ')
    train[index][0]=int(sep[0])
    line=sep[2]
    while line.find(':')>=0:
      sep=line.partition(':')
      vocabID=int(sep[0])
      line=sep[-1]
      sep=line.partition(' ')
      train[index][vocabID+1]=int(sep[0])
      line=sep[-1]
    index=index+1

test=[]
with open("groups.test") as f:
  index=0
  for line in f:
    org=line
    test.append([0]*2001)
    sep=line.partition(' ')
    test[index][0]=int(sep[0])
    line=sep[2]
    while line.find(':')>=0:
      sep=line.partition(':')
      vocabID=int(sep[0])
      line=sep[-1]
      sep=line.partition(' ')
      test[index][vocabID+1]=int(sep[0])
      line=sep[-1]
    index=index+1

wordlist=[]
with open("groups.vocab") as f:
  for line in f:
    word=[]
    sep=line.partition('\t')
    word.append(int(sep[0]))
    sep=sep[2].partition('\t')
    word.append(sep[0])
    word.append(int(sep[2]))
    wordlist.append(word)
wordlist=sorted(wordlist, key=lambda x:x[0])
#input parsing finished

ctgmap=[0,1,2,-1,3] #helper list (real category=0,1,2,4)

#---helper functions---
def entropy(s): #tested
  ctg=[0.0,0.0,0.0,0.0]
  for element in s:
    ctg[ctgmap[element[0]]] += 1
  en=0
  for i in range(len(ctg)):
    if ctg[i]!=0:
      en = en - ctg[i] / len(s)  * log((ctg[i]/len(s)),2)
  return en

def bestSpl(s,x):#finished not tested
  base=entropy(s)
  if base==0: return [-1,-1] # return -1 when no more splitting is necessary
  #split in 
  maxgain=0
  split=[-1,-1]
  for i in range(x):
    for j in range(len(wordlist)):
      s1=[]
      s2=[]
      for element in s:
        if element[j+1]>i: s1.append(element)
        else: s2.append(element)
      if (len(s1)*len(s2)>0):
        gain=base-(entropy(s1)*len(s1)/len(s)+entropy(s2)*len(s2)/len(s))
        if gain>maxgain:
          maxgain=gain
          split=[j,i]
  return split

def TDIDT(s,depth,x):
  #print depth
  node=[]
  if (depth==depthe):
    ctg=[0.0,0.0,0.0,0.0]
    for element in s:
      ctg[ctgmap[element[0]]] += 1
    ctg=sorted(enumerate(ctg), key=lambda x:x[1], reverse=True)
    node.append([ctgmap.index(ctg[0][0]),[-1,-1],-1,-1,depth])
  else:
    split=bestSpl(s,x)
    s1=[]
    s2=[]
    if (split[0]==-1): node.append([s[0][0],[-1,-1],-1,-1,depth])
    else:
      for element in s:
        if element[split[0]+1]>split[1]: s1.append(element)
        else: s2.append(element)
      node.append([-1,split,1,0,depth])
      left=TDIDT(s1,depth+1,x)
      node[0][3]=1+len(left)
      node=node+left
      right=TDIDT(s2,depth+1,x)
      node=node+right
  return node

def predict(tree,point):
  index=0
  while 1:
    if tree[index][1][0]==-1: return tree[index][0]
    if point[tree[index][1][0]+1]>tree[index][1][1]:
      index+=tree[index][2]
    else: index+=tree[index][3]
  
def partition(s,k):
  snew=list(s)
  num=len(s)/k
  result=[]
  ssl=[]
  for i in range(k):
    stmp=[]
    for j in range(num):
      index=int(floor(random.uniform(0,len(snew))))
      stmp.append(snew[index])
      del snew[index]
    result.append([snew+ssl,stmp])
    ssl=ssl+stmp
  return result

#---partA---
print '\n====partA'
depthe=10000
tree1=TDIDT(train,0,1)
wrong=0.0
for element in test:
  ctgr=predict(tree1,element)
  if ctgr!=element[0]: wrong+=1
print 'Accuracy=',1.0-wrong/len(test)
maxdp=0
for node in tree1:
  if node[4]>maxdp: maxdp=node[4] 
print 'Max depth',maxdp
#---partB---
print '\n====partB'
print 'top 2 levels'
leftroot=tree1[tree1[0][2]]
rightroot=tree1[tree1[0][3]]
print 'level1:'
print '    '+wordlist[tree1[0][1][0]][1]
print 'level2:'
print '    '+wordlist[rightroot[1][0]][1]
print '    '+wordlist[leftroot[1][0]][1]
print 'bottom 2 levels'
print 'level-2:'
for node in tree1:
  if node[4]==(maxdp-2): 
    print '    '+wordlist[node[1][0]][1]
print 'level-1:'
for node in tree1:
  if node[4]==(maxdp-1): 
    print '    '+wordlist[node[1][0]][1]

#---partC---
print '\n====partC'
depthe=10
tree2=TDIDT(train,0,1)
wrong=0.0
for element in train:
  ctgr=predict(tree2,element)
  if ctgr!=element[0]: wrong+=1
print 'Train Accuracy=',1.0-wrong/len(test)
wrong=0.0
for element in test:
  ctgr=predict(tree2,element)
  if ctgr!=element[0]: wrong+=1
print 'Test Accuracy=',1.0-wrong/len(test)

#---partD---
print '\n====partD'
miss=[[0.0,0.0],[0.0,0.0]]
for element in test:
  c1=int(predict(tree1,element)==element[0])
  c2=int(predict(tree2,element)==element[0])
  miss[c1][c2]+=1
print miss
chisq=(miss[1][0]-miss[0][1])**2/(miss[0][1]+miss[1][0])
print chisq

#---partE---
print '\n====partE'
depthe=10
tree3=TDIDT(train,0,2)
wrong=0.0
for element in train:
  ctgr=predict(tree3,element)
  if ctgr!=element[0]: wrong+=1
print 'Train Accuracy=',1.0-wrong/len(test)
wrong=0.0
for element in test:
  ctgr=predict(tree3,element)
  if ctgr!=element[0]: wrong+=1
print 'Test Accuracy=',1.0-wrong/len(test)
print '\n---k-fold----'
k=5
sets=partition(train+test,k)
sigma=[]
for aset in sets:
  tmptrain=aset[0]
  tmptest=aset[1]
  treeC=TDIDT(tmptrain,0,1)
  treeE=TDIDT(tmptrain,0,2)
  wrongC=0.0
  wrongE=0.0
  for element in tmptest:
    ctgr=predict(treeC,element)
    if ctgr!=element[0]: wrongC+=1
    ctgr=predict(treeE,element)
    if ctgr!=element[0]: wrongE+=1
  sigma.append(((wrongC-wrongE)/len(tmptest)))
sigmamean=0.0
for sig in sigma: sigmamean+=sig/len(sigma)
sigmastd=0.0
for sig in sigma: sigmastd+=(sig-sigmamean)**2
sigmastd=(sigmastd/(k**2-k))**0.5
print sigma
print 'mean=', sigmamean
print 'std=', sigmastd

#---partF---
print '\n====partF'
depthset=[2,3,5,10,50,80]
accset=[]
for depthe in depthset:
  print depthe
  err=0.0
  for aset in sets:
    tmptrain=aset[0]
    tmptest=aset[1]
    treeF=TDIDT(tmptrain,0,1)
    wrongF=0.0
    for element in tmptest:
      ctgr=predict(treeF,element)
      if ctgr!=element[0]: wrongF+=1
    err+=wrongF/len(tmptest)/k
  accset.append(1.0-err)
print depthset
print accset

