# coding=utf-8
#!/usr/bin/env python

import random
from operator import add

#import sys,tty,termios
#
#class _Getch:
#  def __call__(self):
#    fd = sys.stdin.fileno()
#    old_settings = termios.tcgetattr(fd)
#    try:
#      tty.setraw(sys.stdin.fileno())
#      ch = sys.stdin.read(3)
#    finally:
#      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#    return ch
#
#def getInput():
#  inkey = _Getch()
#  while(1):
#    k=inkey()
#    if k!='':break
#  if k=='\x1b[A':
#    print("up")
#  elif k=='\x1b[B':
#    prin("down")
#  elif k=='\x1b[C':
#    print("right")
#  elif k=='\x1b[D':
#    print("left")
#  else:
#    print("not an arrow key!")
#
#def main():
#  for i in range(0,20):
#    get()

class bcolors:
    HEADER = '\033[95m'
    RED = '\033[31m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def makeGrid():
  G=[ [' '] * gSize for _ in range(gSize) ]
  return generateObstacles(G)
#  if(not isPlayable(G)):return makeGrid()
#  else: return G

def isPlayable(G):
  aux=[True]*gSize
  for i in range(gSize):
    if(G[i]==(['X']*gSize)):return False
    for j in range(gSize): aux[j]=aux[j] and G[i][j]=='X'
  return True not in aux

def generateObstacles(G):
  Gt=G
  for _ in range(gSize-1):Gt[random.randint(0,gSize-1)][random.randint(0,gSize-1)]='X'
  r1,r2,r3,r4=0,0,0,0
  while([r1,r2]==[r3,r4]):
    r1,r2,r3,r4=random.randint(0,gSize-1),random.randint(0,gSize-1),random.randint(0,gSize-1),random.randint(0,gSize-1)
  Gt[r1][r2]='1'
  Gt[r3][r4]='2'
  global pos
  pos[0]=[r1,r2]
  pos[1]=[r3,r4]
  return Gt

def paintGrid(G):
  for _ in range(2*gSize+1):print('-',end='  ')
  print('\n')
  for i in range(gSize):
    print('|',end='  ')
    for j in range(gSize):
      if(G[i][j] in ['1','2']):print(bcolors.HEADER+bcolors.BOLD+bcolors.OKGREEN+G[i][j]+bcolors.ENDC,end='  ');print('|',end='  ')
      else:print(bcolors.OKBLUE+G[i][j]+bcolors.ENDC,end='  ');print('|',end='  ')
    print('\n')
    for _ in range(2*gSize+1):print('-',end='  ')
    print('\n')

def paintInfo():
  print(bcolors.UNDERLINE+'Player        bullets      HP '+bcolors.ENDC)
  print('1            ',bcolors.WARNING+str(bullets[0])+bcolors.ENDC,'          ',bcolors.RED+str(hp[0])+bcolors.ENDC)
  print('2            ',bcolors.WARNING+str(bullets[1])+bcolors.ENDC,'          ',bcolors.RED+str(hp[1])+bcolors.ENDC)
  print('\n')

def paintActionsInfo(a1,d1,a2,d2):
  if(d1==[ 0, 1]):d1s='right'
  if(d1==[ 0,-1]):d1s='left'
  if(d1==[ 1, 0]):d1s='down'
  if(d1==[-1, 0]):d1s='up'
  if(d1==[ 0, 0]):d1s=''

  if(a1=='a'):print('Player 1 advanced ',d1s)
  if(a1=='s'):print('Player 1 shot ',d1s)
  if(a1=='w'):print('Player 1 fisted ',d1s)
  if(a1=='d'):print('Player 1 defended')

  if(d2==[ 0, 1]):d2s='right'
  if(d2==[ 0,-1]):d2s='left'
  if(d2==[ 1, 0]):d2s='down'
  if(d2==[-1, 0]):d2s='up'
  if(d2==[ 0, 0]):d2s=''

  if(a2=='a'):print('Player 2 advanced ',d2s)
  if(a2=='s'):print('Player 2 shot ',d1s)
  if(a2=='w'):print('Player 2 fisted ',d1s)
  if(a2=='d'):print('Player 2 defended')

def selectActions():
  actions=[]
  for i in range(nActions):
    a=input('Select your action (a=advance, s=shoot, d=defend, w=melee attack):')
    if(a != 'd'):
      d=input('select the direction of your action (w=up, s=down, a=left, d=right):')
      if d=='w':d=[-1, 0]
      if d=='a':d=[0 ,-1]
      if d=='s':d=[1 , 0]
      if d=='d':d=[0 , 1]
    else: d=[0,0]
    actions+=[[a,d]]
  return actions

def advance(player,direction):
  global pos,grid
  oldpos=pos[player-1]
  newpos=list(map(add, oldpos,direction))
  if(newpos[0]<0 or newpos[0]>=gSize or newpos[1]<0 or newpos[1]>=gSize):return
  if(grid[newpos[0]][newpos[1]]==' '):
    grid[newpos[0]][newpos[1]]=str(player)
    grid[oldpos[0]][oldpos[1]]=' '
    pos[player-1]=newpos

def checkMovement(direction1, direction2):
  newpos1=list(map(add, pos[0], direction1))
  newpos2=list(map(add, pos[1], direction2))
  return newpos2==newpos1

def attack(player, direction, mode): #mode: True=range, False=melee
  global pos, grid, hp, bullets
  st=pos[player-1]
  n=list(map(add,st,direction))
  if(mode):
    for i in range(gSize):
      if(n[0]<0 or n[1]<0 or n[0]>gSize-1 or n[1]>gSize-1 or grid[n[0]][n[1]]=='X'):break
      if(grid[n[0]][n[1]] !=' '):hp[int(grid[n[0]][n[1]])-1]-=bulletDmg;print(bcolors.RED+'A PLAYER WAS SHOT IN THE FACE!!'+bcolors.ENDC)
      n=list(map(add,n,direction))
  else:
    if(n[0]<0 or n[1]<0 or n[0]>gSize-1 or n[1]>gSize-1):return null
    if(grid[n[0]][n[1]] not in [' ','X']):hp[int(grid[n[0]][n[1]])-1]-=fistDmg;print(bcolors.RED+'A PLAYER WAS PUNCHED IN THE FACE!!'+bcolors.ENDC)

def resolveTurn(actions): 
  #[[(action1,direction),(action2,direction),...,(actionN,direction)],[(action1,direction),(action2,direction),...,(actionN,direction)]]
  #actions: 'a'=advance, 's'=shoot, 'd'=defend, 'w'=fist attack
  #directions: [-1,0]=up, [1,0]=down, [0,-1]=left, [0,1]=right
  paintInfo()
  paintGrid(grid)
  for i in range(len(actions[0])):
    if(checkEnded()):endGame(hp.index(max(hp))+1)
    a1=actions[0][i][0]
    d1=actions[0][i][1]
    a2=actions[1][i][0]
    d2=actions[1][i][1]
    isDefending=[a1=='d',a2=='d']
    if(a1=='s' or a1=='f'): attack(1,d1,a1=='s')
    if(a2=='s' or a2=='f'): attack(2,d2,a2=='s')
    if(a1=='a' and a2=='a'): 
      if(checkMovement(d1,d2)): advance(1,d1);advance(2,d2)
    else: 
      if(a1=='a'): advance(1,d1)
      if(a2=='a'): advance(2,d2)
    print('Action ',i,':')
    paintActionsInfo(a1,d1,a2,d2)
    paintInfo()
    paintGrid(grid)

def newGame():
  global hp, bullets, grid
  hp=[5,5]
  bullets=[2,2]
  grid=makeGrid()
  paintInfo()
  paintGrid(grid)
  while (not checkEnded()):
    actions=[]
    #print(clear)
    #paintInfo()
    #paintGrid(grid)
    print('player 1, input your actions\n')
    actions+=[selectActions()]
    print(clear)
    paintInfo()
    paintGrid(grid)
    print('player 2, input your actions\n')
    actions+=[selectActions()]
    print(actions)
    resolveTurn(actions)

def checkEnded():
  alive=0
  for playerhp in hp:
    if(playerhp>0):alive+=1
  return alive<=1


def endGame(player):
  print('PLAYER',player,'WON!!!')
  exit(0)

gSize=5
hp=[5,5]
bullets=[2,2]
pos=[[],[]]
grid=[]
bulletDmg=3
fistDmg=6
nActions=5
clear='\n'*100

if __name__ == "__main__":
  newGame()