import os
from math import *

depthe=10000
#---reading training input---
# tested 
train=[]
with open("circle.train") as f:
  for line in f:
    sep=line.partition(' ')
    cl=int(sep[0])
    line=sep[2]
    sep=line.partition(' ')
    x=float(sep[0].partition(':')[2])
    y=float(sep[2].partition(':')[2])
    train.append([x,y,cl]) 

#---helper functions---
def entropy(s):#tested
  pos=0.0
  neg=0.0
  for element in s:
    if element[2]: pos+=1
    else: neg+=1
  pos=pos/len(s)
  neg=neg/len(s)
  if (neg*pos==0): return 0
  en=-pos*log(pos,2)-neg*log(neg,2)
  #print pos,' ',neg
  return en

def bestSpl(s): #tested on trainmini
  base=entropy(s)
  if base==0: return [-1,-1] # return -1 when no more splitting is necessary
  #split in x
  maxgain=0
  split=[-1,-1]
  for x in range (1,10):
    s1=[]
    s2=[]
    for element in s:
      if element[0]<x: s1.append(element)
      else: s2.append(element)
    if (len(s1)*len(s2)>0):
      gain=base-(entropy(s1)*len(s1)/len(s)+entropy(s2)*len(s2)/len(s))
      if gain>maxgain:
        maxgain=gain
        split=[0,x]
    
  #split in y
  for y in range (1,10):
    s1=[]
    s2=[]
    for element in s:
      if element[1]<y: s1.append(element)
      else: s2.append(element)
    if (len(s1)*len(s2)>0):
      gain=base-(entropy(s1)*len(s1)/len(s)+entropy(s2)*len(s2)/len(s))
      if gain>maxgain:
        maxgain=gain
        split=[1,y]
  #print maxgain,' ',base
  return split

def TDIDT(s,depth): #tested on trainmini
  print depth
  node=[]
  if (depth==depthe):
    count=0
    for element in s:
      if element[2]==1: count+=1
      else: count-=1
    if count>=0: node.append([1,[-1,-1],-1-1])
    else: node.append([0,[-1,-1],-1,1])
  else:
    split=bestSpl(s)
    s1=[]
    s2=[]
    if (split[0]==-1): node.append([s[0][2],[-1,-1],-1,-1])
    else:
      for element in s:
        if element[split[0]]<split[1]: s1.append(element)
        else: s2.append(element)
      node.append([-1,split,1,0])
      left=TDIDT(s1,depth+1)
      node[0][3]=1+len(left)
      node=node+left
      right=TDIDT(s2,depth+1)
      node=node+right
  return node

def predict(tree,point):
  index=0
  while 1:
    if tree[index][1][0]==-1: return tree[index][0]
    if point[tree[index][1][0]]<tree[index][1][1]:
      index+=tree[index][2]
    else: index+=tree[index][3]

tree1 = TDIDT(train,0)
correct=0
wrong=0
for element in train:
  if predict(tree1,element)==element[2]:
    correct+=1
  else: wrong+=1
    
print correct,' ',wrong

