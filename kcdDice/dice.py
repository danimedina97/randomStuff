# coding=utf-8
#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import random
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
from sys import exit,argv

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

def printRules():
  print('===================================================================================')
  print('USE THE ARROWS AND THE SPACE TO SELECT THE DICE, PRESS ENTER TO CONFIRM YOUR ACTION')
  print('THIS GAME IS PLAYED WITH 6 DICE')
  print('YOU WILL HAVE 2 SCORES, THE GLOBAL SCORE AND THE TURN SCORE')
  print('YOUR OBJECTIVE IS TO SCORE 4000 POINTS IN THE GLOBAL SCORE BEFORE YOUR RIVAL')
  print('SCORING SYSTEM:')
  print('ROLLING 1-2-3-4-5 OR 2-3-4-5-6 IS WORTH 750 POINTS')
  print('ROLLING 1-2-3-4-5-6 IS WORTH 1500 POINTS')
  print('A SINGLE ROLL OF 1 IS WORTH 100 POINTS')
  print('A SINGLE ROLL OF 5 IS WORTH 50 POINTS')
  print('3 ROLLS OF THE SAME NUMBER[2-6] ARE WORTH 100*THAT_NUMBER POINTS')
  print('EG. ROLLING 4-4-4 IS WORTH 400 POINTS')
  print('3 ROLLS OF 1 ARE WORTH 1000 POINTS')
  print('EACH ROLL OF THE SAME NUMBER AFTER THE THIRD ONE DOUBLES THE SCORE OF THE 3 ROLLS')
  print('EG. ROLLING 4-4-4-4 IS WORTH 800 POINTS AND ROLLING 4-4-4-4-4 IS WORTH 1600 POINTS')
  print('THIS ROLLS OF 3 TO 6 OF THE SAME NUMBER MUST BE MADE IN THE SAME THROW')
  print('AFTER DECIDING WHICH DICE YOU KEEP, YOU CAN REROLL THE UNUSED ONES, OR SKIP THE TURN')
  print('YOU CAN REROLL AS LONG AS YOU HAVE DICE UNUSED')
  print('EACH TIME YOU THROW THE DICE, YOU MUST SCORE POINTS')
  print('IF YOU DO NOT SCORE IN A THROW, YOU ARE BUSTED')
  print('IF YOU ARE BUSTED YOUR TURN SCORE BECOMES 0 AND YOUR TURN ENDS')
  print('IF YOU SCORE WITH ALL OF YOUR DICE, YOU REROLL ALL OF THEM AGAIN')
  print('===================================================================================')

def usage():
  print('USAGE: python dice.py mode training_steps alfa gamma')
  print('  1 for PVP 0 for PVE -|                    |    |')
  print('                       learning rate {0-1} -|    |')
  print('                 weight given to future actions -|')


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
    for item in combineRoll(x):
      d[1][tuple(x)][tuple([False]+item)]=computeScore(item)
      d[1][tuple(x)][tuple([True]+item)]=computeScore(item)
    for d2 in range(1,7):
      x[d2-1]+=1
      d[2][tuple(x)]={}
      for item in combineRoll(x):
        d[2][tuple(x)][tuple([False]+item)]=computeScore(item)
        d[2][tuple(x)][tuple([True]+item)]=computeScore(item)
      for d3 in range(1,7):
        x[d3-1]+=1
        d[3][tuple(x)]={}
        for item in combineRoll(x):
          d[3][tuple(x)][tuple([False]+item)]=computeScore(item)
          d[3][tuple(x)][tuple([True]+item)]=computeScore(item)
        for d4 in range(1,7):
          x[d4-1]+=1
          d[4][tuple(x)]={}
          for item in combineRoll(x):
            d[4][tuple(x)][tuple([False]+item)]=computeScore(item)
            d[4][tuple(x)][tuple([True]+item)]=computeScore(item)
          for d5 in range(1,7):
            x[d5-1]+=1
            d[5][tuple(x)]={}
            for item in combineRoll(x):
              d[5][tuple(x)][tuple([False]+item)]=computeScore(item)
              d[5][tuple(x)][tuple([True]+item)]=computeScore(item)
            for d6 in range(1,7):
              x[d6-1]+=1
              d[6][tuple(x)]={}
              for item in combineRoll(x):
                d[6][tuple(x)][tuple([False]+item)]=computeScore(item)
                d[6][tuple(x)][tuple([True]+item)]=computeScore(item)
              x[d6-1]-=1
            x[d5-1]-=1
          x[d4-1]-=1
        x[d3-1]-=1
      x[d2-1]-=1
    x[d1-1]-=1
  return d

def computeScore(selection):
  #print(selection)
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
    if(flush): score-=100*(selection[1]-1)
  
  if(selection[2]>2): score+=200*(2**(selection[2]-3))
  else:
    if(selection[2]==1 and flush==False):return 0
    if(selection[2]==2):return 0
  
  if(selection[3]>2): score+=300*(2**(selection[3]-3))
  else:
    if(selection[3]==1 and flush==False): return 0
    if(selection[3]==2):return 0
  
  if(selection[4]>2): score+=400*(2**(selection[4]-3))
  else:
    if(selection[4]==1 and flush==False): return 0
    if(selection[4]==2):return 0
  
  if(selection[5]>2): score+=500*(2**(selection[5]-3))
  else:
    score+=50*selection[5] 
    if(flush): score-=50*selection[5]
  
  if(selection[6]>2): score+=600*(2**(selection[6]-3))
  else:
    if(selection[6]==1 and flush==False): return 0
    if(selection[6]==2):return 0

  return score

def showDice(dice):
  res=[]
  for die in dice:
    res+=['\u2683']
  return res

def combineRoll(roll):
  combinations=[]
  for i in range(roll[0]+1):
      for j in range(roll[1]+1):
          for k in range(roll[2]+1):
              for l in range(roll[3]+1):
                  for m in range(roll[4]+1):
                      for n in range(roll[5]+1):
                        combinations+=[[i,j,k,l,m,n]]
  return combinations

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
        Separator('= Keep score or roll again? (please select only one) ='),
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

def computerTurn(training):
  continuePlay=True
  turnScore=0
  diceRemaining=6
  decisions=[]
  while continuePlay==True:
    rolled=rolled2template(rollDice(diceRemaining))
    answers=computerSelectAction(rolled) #[continue?, #of1s, #of2s, #of3s, #of4s, #of5s, #of6s, #ofDiceSpent]
    decisions+=[[diceRemaining]+rolled+answers] #[diceRolled, 1rolled, 2rolled, 3rolled, 4rolled, 5rolled, 6rolled, continue?, 1kept, 2kept, 3kept, 4kept, 5kept, 6kept, diceSpent]
    continuePlay=answers[0]
    diceRemaining-=answers[-1]
    rollScore=computeScore(answers[1:7])
    if(rollScore==0):return 0
    else:
      if(diceRemaining==0): diceRemaining=6
      turnScore+=rollScore
  for decision in decisions: #[diceRolled, 1rolled, 2rolled, 3rolled, 4rolled, 5rolled, 6rolled, continue?, 1kept, 2kept, 3kept, 4kept, 5kept, 6kept, diceSpent]
    nd=decision[0] #number of dice rolled
    rll=decision[1:7] #roll
    slc=decision[7:14] #selection
    prevValue=rewards[nd][tuple(rll)][tuple(slc)]
    diceRemaining=decision[0]-decision[-1]
    if(training):rewards[nd][tuple(rll)][tuple(slc)]=qFunc(prevValue,turnScore,diceRemaining,alfa,gamma)
  return turnScore

def qFunc(prevValue,turnScore,diceRemaining,alpha,gamma):
  potential=1000*2**(diceRemaining-3) if diceRemaining>2 else 100*diceRemaining
  aux=0
  if(turnScore==0): aux-=1000 
  else: aux=turnScore
  newValue=(1-alpha)*prevValue+alpha*(aux+gamma*potential)
  #print(newValue)
  return newValue

def computerSelectAction(rolled):
  answers=[0,0,0,0,0,0,0,0] #[continue?, #of1s, #of2s, #of3s, #of4s, #of5s, #of6s, #ofDiceSpent]
  diceSpent=0
  diceRolled=sum(rolled)
  bestOption=[False]+rolled
  bestOptionScore=computeScore(rolled)
  for option, optionScore in rewards[diceRolled][tuple(rolled)].items():
    if(optionScore>bestOptionScore): bestOption=option;bestOptionScore=optionScore
  #print(rolled,bestOption)
  return list(bestOption)+[sum(bestOption[1:])]

def computerTrain(steps):
  tot=0
  for i in range(steps):
    turn=computerTurn(False)
    tot+=turn
  return(tot/steps)

def computerTest():
  res={}
  i=0.0
  for i in [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]:
    alfa=i
    res[i]={}
    for j in [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]:
      gamma=j
      res[i][j]={}
      for k in [1,10,100,1000,10000,100000]:
        temp=0
        for m in range(10):temp+=computerTrain(k);print('training: alpha= ',alfa,', gamma= ',gamma,', steps= ',k)
        print(temp/10)
        res[i][j][k]=temp/10
  print(res)


def newGame(maxScore,mode):
  p1score=0
  p2score=0
  maxScore=maxScore
  mode=mode #true=PVP, false=PVE
  #if(mode):d=initDic()
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
        p2score+=computerTurn(False)
      else:
        p1score+=computerTurn(False)
        p2score+=playerTurn(p2score)

#alfa=0.5
#gamma=0.8
#training_steps=1000
#rewards={}

if __name__ == "__main__":
  if(len(argv)!=5):usage();exit(0)
  rewards=initDic()
  mode=int(argv[1])==1            # 1=PVP 0=PVE
  training_steps=argv[2]          #          
  alfa=float(argv[3])               # Learning rate {0-1}
  gamma=float(argv[4])              # Weight given to future actions
  if(int(argv[1])==3):computerTest()
  printRules()
  if(mode==False):computerTrain(int(training_steps))
  exit(0)
  #newGame(4000,True)
  #print(computeScore([False,1,1,1,1,1,1,6][1:7]))