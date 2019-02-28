# coding=utf-8
#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import random
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

questions = [
    {
        'type': 'checkbox',
        'message': 'Select toppings',
        'name': 'toppings',
        'choices': [
            Separator('= The Meats ='),
            {
                'name': 'Ham'
            },
            {
                'name': 'Ground Meat'
            },
            {
                'name': 'Bacon'
            },
            Separator('= The Cheeses ='),
            {
                'name': 'Mozzarella',
                'checked': True
            },
            {
                'name': 'Cheddar'
            },
            {
                'name': 'Parmesan'
            },
            Separator('= The usual ='),
            {
                'name': 'Mushroom'
            },
            {
                'name': 'Tomato'
            },
            {
                'name': 'Pepperoni'
            },
            Separator('= The extras ='),
            {
                'name': 'Pineapple'
            },
            {
                'name': 'Olives',
                'disabled': 'out of stock'
            },
            {
                'name': 'Extra cheese'
            }
        ],
        'validate': lambda answer: 'You must choose at least one topping.' \
            if len(answer) == 0 else True
    }
]

answers = prompt(questions, style=style)
pprint(answers)

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

def showDice(dice):
  res=[]
  for die in dice:
    res+=["\u2680"]
  return res

if __name__ == "__main__":
  d=makeDic()
  computeScore(throwDice(6))
  print(computeScore([3,0,0,0,0,1]))
  print(showDice([1,1]))
