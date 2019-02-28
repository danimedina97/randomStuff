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

#questions = [
#    {
#        'type': 'checkbox',
#        'message': 'Select toppings',
#        'name': 'toppings',
#        'choices': [
#            Separator('= The Meats ='),
#            {
#                'name': '\u2680'
#            },
#            {
#                'name': 'Ground Meat'
#            },
#            {
#                'name': 'Bacon'
#            },
#            Separator('= The Cheeses ='),
#            {
#                'name': 'Mozzarella',
#                'checked': True
#            },
#            {
#                'name': 'Cheddar'
#            },
#            {
#                'name': 'Parmesan'
#            },
#            Separator('= The usual ='),
#            {
#                'name': 'Mushroom'
#            },
#            {
#                'name': 'Tomato'
#            },
#            {
#                'name': 'Pepperoni'
#            },
#            Separator('= The extras ='),
#            {
#                'name': 'Pineapple'
#            },
#            {
#                'name': 'Olives',
#                'disabled': 'out of stock'
#            },
#            {
#                'name': 'Extra cheese'
#            }
#        ],
#        'validate': lambda answer: 'You must choose at least one topping.' \
#            if len(answer) == 0 else True
#    }
#]

#answers = prompt(questions, style=style)
#pprint(answers)

def rollDice(num_dices):
  res=[]
  for i in range(num_dices):res.append(random.randint(1,6))
  return res

def rolled2template(rolled):
  res=[0,0,0,0,0,0]
  for item in rolled: res[item-1]+=1
  return res

def initDic():
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
    res+=['\u2683']
  return res

def combineRoll(roll):
  combinations=[]
  for i in range(roll[0]):
    if(len(roll)>1):
      for j in range(roll[1]):
        if(len(roll)>2):
          for k in range(roll[2]):
            if(len(roll)>3):
              for l in range(roll[3]):
                if(len(roll)>4):
                  for m in range(roll[4]):
                    if(len(roll)>5):
                      for n in range(roll[5]):
                        combinations+=[i,j,k,l,m,n]
                    else:
                      combinations+=[i,j,k,l,m]
                else:
                  combinations+=[i,j,k,l]
            else:
              combinations+=[i,j,k]
        else:
          combinations+=[i,j]
    else:
      combinations+=[i,j,k,l,m,n]
  return combinations

def computeFitness(selection):
  return computeScore(selection)

def selectDice(roll):
  slected=[0,0,0,0,0,0]
  fitness_selected=0
  for selection in combineRoll(roll):
    f=computeFitness(selection)
    if (f>fitness_selected): selected=selection;fitness_selected=f
  return selected

def formatAnswers(answer):
  res=['roll'==answer[-1]]+[0,0,0,0,0,0,0]
  for i in range(len(answer)-1):res[int(answer[i][-1])]+=1;res[-1]+=1
  return res

def getAnswers6(rolled):
  questions = [
    {
      'type': 'checkbox',
      'message': 'Select dice',
      'name': 'dice',
      'choices': [
        Separator('= Dice ='),
        {
          'name': 'die 1: '+str(rolled[0])
        },
        {
          'name': 'die 2: '+str(rolled[1])
        },
        {
          'name': 'die 3: '+str(rolled[2])
        },
        {
          'name': 'die 4: '+str(rolled[3])
        },
        {
          'name': 'die 5: '+str(rolled[4])
        },
        {
          'name': 'die 6: '+str(rolled[5])
        },
        Separator('= Keep score or roll again? ='),
        {
          'name': 'keep',
          'checked': True
        },
        {
          'name': 'roll'
        }
      ],
    }
  ]
  answers = prompt(questions, style=style)
  return answers

def getAnswers5(rolled):
  questions = [
    {
      'type': 'checkbox',
      'message': 'Select dice',
      'name': 'dice',
      'choices': [
        Separator('= Dice ='),
        {
          'name': 'die 1: '+str(rolled[0])
        },
        {
          'name': 'die 2: '+str(rolled[1])
        },
        {
          'name': 'die 3: '+str(rolled[2])
        },
        {
          'name': 'die 4: '+str(rolled[3])
        },
        {
          'name': 'die 5: '+str(rolled[4])
        },
        Separator('= Keep score or roll again? ='),
        {
          'name': 'keep',
          'checked': True
        },
        {
          'name': 'roll'
        }
      ],
    }
  ]
  answers = prompt(questions, style=style)
  return answers

def getAnswers4(rolled):
  questions = [
    {
      'type': 'checkbox',
      'message': 'Select dice',
      'name': 'dice',
      'choices': [
        Separator('= Dice ='),
        {
          'name': 'die 1: '+str(rolled[0])
        },
        {
          'name': 'die 2: '+str(rolled[1])
        },
        {
          'name': 'die 3: '+str(rolled[2])
        },
        {
          'name': 'die 4: '+str(rolled[3])
        },
        Separator('= Keep score or roll again? ='),
        {
          'name': 'keep',
          'checked': True
        },
        {
          'name': 'roll'
        }
      ],
    }
  ]
  answers = prompt(questions, style=style)
  return answers

def getAnswers3(rolled):
  questions = [
    {
      'type': 'checkbox',
      'message': 'Select dice',
      'name': 'dice',
      'choices': [
        Separator('= Dice ='),
        {
          'name': 'die 1: '+str(rolled[0])
        },
        {
          'name': 'die 2: '+str(rolled[1])
        },
        {
          'name': 'die 3: '+str(rolled[2])
        },
        Separator('= Keep score or roll again? ='),
        {
          'name': 'keep',
          'checked': True
        },
        {
          'name': 'roll'
        }
      ],
    }
  ]
  answers = prompt(questions, style=style)
  return answers

def getAnswers2(rolled):
  questions = [
    {
      'type': 'checkbox',
      'message': 'Select dice',
      'name': 'dice',
      'choices': [
        Separator('= Dice ='),
        {
          'name': 'die 1: '+str(rolled[0])
        },
        {
          'name': 'die 2: '+str(rolled[1])
        },
        Separator('= Keep score or roll again? ='),
        {
          'name': 'keep',
          'checked': True
        },
        {
          'name': 'roll'
        }
      ],
    }
  ]
  answers = prompt(questions, style=style)
  return answers

def getAnswers1(rolled):
  questions = [
    {
      'type': 'checkbox',
      'message': 'Select dice',
      'name': 'dice',
      'choices': [
        Separator('= Dice ='),
        {
          'name': 'die 1: '+str(rolled[0])
        },
        Separator('= Keep score or roll again? ='),
        {
          'name': 'keep',
          'checked': True
        },
        {
          'name': 'roll'
        }
      ],
    }
  ]
  answers = prompt(questions, style=style)
  return answers

def getAnswers(rolled):
  if(1==len(rolled)): return getAnswers1(rolled)
  if(2==len(rolled)): return getAnswers2(rolled)
  if(3==len(rolled)): return getAnswers3(rolled)
  if(4==len(rolled)): return getAnswers4(rolled)
  if(5==len(rolled)): return getAnswers5(rolled)
  if(6==len(rolled)): return getAnswers6(rolled)

def playerTurn(playerScore):
  continuePlay=True
  turnScore=0
  diceRemaining=6
  while continuePlay==True:
    rolled=rollDice(diceRemaining)
    answers=getAnswers(rolled)
    answers=formatAnswers(answers['dice']) #[continue?, #of1s, #of2s, #of3s, #of4s, #of5s, #of6s, #ofDiceSpent]
    continuePlay=answers[0]
    diceRemaining-=answers[-1]
    rollScore=computeScore(answers[1:])
    if(rollScore==0): print('BUSTED!!');return 0
    else:
      if(diceRemaining==0): diceRemaining=6
      turnScore+=rollScore
      print('----------------')
      print('Player Score', playerScore)
      print('Turn Score: ', turnScore)
  return turnScore

def computerTurn():
  return null

def newGame(maxScore,mode):
  p1score=0
  p2score=0
  maxScore=maxScore
  mode=mode #true=PVP, false=PVE
  if(mode):d=initDic()
  while(p1score<maxScore and p2score<maxScore):
    if(mode):
      print('\n\nplayer 1 turn, score: ', p1score)
      p1score+=playerTurn(p1score)
      if(p1score>=maxScore):print('¡¡¡YOU WIN!!!');break
      print('\n\nplayer 2 turn, score: ', p2score)
      p2score+=playerTurn(p2score)
      if(p2score>=maxScore):print('¡¡¡YOU WIN!!!');break
    else:
      if(random.randint(1,2)==1):
        p1score+=playerTurn(p1score)
        p2score+=computerTurn(p2score)
      else:
        p1score+=computerTurn(p1score)
        p2score+=playerTurn(p2score)

if __name__ == "__main__":
  newGame(1000,True)