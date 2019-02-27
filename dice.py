# coding=utf-8
#!/usr/bin/env python

import random

def throwDice(num_dices):
  res=[]
  for i in range(num_dices):res.append(random.randint(1,6))
  return res

def makeDic():
  d={}
  x=[0,0,0,0,0,0]
  for i in range(1,7):d[i]={}
  for d1 in range(1,7):
    x[d1-1]+=1
    d[1][tuple(x)]={}
    for d2 in range(1,7):
      x[d2-1]+=1
      d[2][tuple(x)]={}
      for d3 in range(1,7):
        x[d3-1]+=1
        d[3][tuple(x)]={}
        for d4 in range(1,7):
          x[d4-1]+=1
          d[4][tuple(x)]={}
          for d5 in range(1,7):
            x[d5-1]+=1
            d[5][tuple(x)]={}
            for d6 in range(1,7):
              x[d6-1]+=1
              d[6][tuple(x)]={}
              x[d6-1]-=1
            x[d5-1]-=1
          x[d4-1]-=1
        x[d3-1]-=1
      x[d2-1]-=1
    x[d1-1]-=1
  return d

def computeScore(selection):
  selection=[0]+selection
  score=0
  flush=False
  if(selection[1]>0 and selection[2]>0 and selection[3]>0 and selection[4]>0 and selection[5]>0 and selection[6]>0):score+=1500;flush=True
  else:
    if(selection[1]>0 and selection[2]>0 and selection[3]>0 and selection[4]>0 and selection[5]>0):score+=750;flush=True
    if(selection[2]>0 and selection[3]>0 and selection[4]>0 and selection[5]>0 and selection[6]>0):score+=750;flush=True
  
  if(selection[1]>2): score+=1000*(2**(selection[1]-3))
  else: 
    score+=100*selection[1]
    if(flush): score-=100
  
  if(selection[2]>2): score+=200*(2**(selection[2]-3))
  else:
    if(selection[2]>0 and flush==False):return 0
  
  if(selection[3]>2): score+=300*(2**(selection[3]-3))
  else:
    if(selection[3]>0 and flush==False): return 0
  
  if(selection[4]>2): score+=400*(2**(selection[4]-3))
  else:
    if(selection[4]>0 and flush==False): return 0
  
  if(selection[5]>2): score+=500*(2**(selection[5]-3))
  else:
    score+=50*selection[5] 
    if(flush): score-=50
  
  if(selection[6]>2): score+=600*(2**(selection[6]-3))
  else:
    if(selection[6]>0 and flush==False): return 0

  return score

if __name__ == "__main__":
  d=makeDic()
  computeScore(throwDice(6))
  print(computeScore([3,0,0,0,0,1]))
