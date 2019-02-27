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

if __name__ == "__main__":
  print(throwDice(6))
  d=makeDic()
  print(d)
  print(len(d[6]))