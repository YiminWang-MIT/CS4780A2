import os
import random
from math import *

#---reading input---
train=[]
ctgTrain=[]
with open("groups.train") as f:
  index=0
  #genreCountTrainStd=[0]*5
  for line in f:
    #if index>=limit: break
    org=line
    train.append([0]*2000)
    sep=line.partition(' ')
    ctgTrain.append(sep[0]) #add genre
    #genreCountTrainStd[int(sep[0])]=genreCountTrainStd[int(sep[0])]+1
    line=sep[2]
    while line.find(':')>=0:
      sep=line.partition(':')
      vocabID=int(sep[0])
      line=sep[-1]
      sep=line.partition(' ')
      train[index][vocabID]=int(sep[0])
      line=sep[-1]
      #*************************print***************************
      #print sep[0]
    index=index+1

test=[]
ctgTest=[]
with open("groups.test") as f:
  index=0
  #genreCountTrainStd=[0]*5
  for line in f:
    #if index>=limit: break
    org=line
    test.append([0]*2000)
    sep=line.partition(' ')
    ctgTest.append(sep[0]) #add genre
    #genreCountTrainStd[int(sep[0])]=genreCountTrainStd[int(sep[0])]+1
    line=sep[2]
    while line.find(':')>=0:
      sep=line.partition(':')
      vocabID=int(sep[0])
      line=sep[-1]
      sep=line.partition(' ')
      test[index][vocabID]=int(sep[0])
      line=sep[-1]
      #*************************print***************************
      #print sep[0]
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

#---helper functions---
def entropy(s):
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

def bestSpl(s): 
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

def TDIDT(s,depth):
  #print depth
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

def gridplot(fun,name,tree):
  grid=200
  data=name+".pdata"
  gnucmd=name+",gcmd"
  plotdata=file(data,'w')
  for i in range(grid):
    for j in range(grid):
      x=i*10.0/grid
      y=j*10.0/grid
      point=[x,y,-1]
      cl=0
      for t in tree:
        if fun(t,point)==1: cl+=1
        else: cl-=1
      if cl>=0: cl=1
      else: cl=0
      plotdata.write("%f %f %d\n"%(x,y,cl))
  plotdata.close()
  gnuc=file(gnucmd,'w')
  gnuc.write("\
set size ratio -1\n\
set terminal png\n\
set out '%s.png'\n\
set palette model RGB defined (0 \"green\",1 \"blue\")\n\
plot '%s.pdata' u 1:2:3 notitle with points pt 0 palette\n\
unset out"%(name,name))
  gnuc.close()
  startgnuplot="gnuplot "+gnucmd
  os.system(startgnuplot)
