import os
import ast
import time as t
import tkinter as tk
import pygame
import threading as th
import lvlMaker as lM
os.system("color")

class Player:
    def __init__(self, symb, pos, keySymb, endSymb):
        self.symb, self.pos, self.bullets, self.lastHead, self.keyPos, self.keySymb, self.endPos, self.endSymb = symb, pos, 2, '', -1, keySymb, -1, endSymb
        self.finished=False
        self.dead=False
        
    def __eq__(self,p): return self.pos==p
    def __add__(self,n): return self.pos+n
    def __sub__(self,n): return self.pos-n
    def __floordiv__(self,n): return self.pos//n
    def __mod__(self,n): return self.pos%n

    def move(self,field):
        w=len(field[0])-2
        h=len(field)-2
        heading=input(self.symb+"'s turn: ")
        if heading in ('w','a','s','d') and not self.finished:
            self.lastHead=heading
            field[self.pos//w+1][self.pos%w+1]=' '
            if heading=='w' and self-w>=0 and field[(self-w)//w+1][(self-w)%w+1] in [' ',self.keySymb] or field[(self-w)//w+1][(self-w)%w+1]==self.endSymb and self.keyPos==-1: self.pos-=w
            elif heading=='a' and self//w==(self-1)//w and field[(self-1)//w+1][(self-1)%w+1] in [' ',self.keySymb] or field[(self-1)//w+1][(self-1)%w+1]==self.endSymb and self.keyPos==-1: self.pos-=1
            elif heading=='s' and self+w<w*h and field[(self+w)//w+1][(self+w)%w+1] in [' ',self.keySymb] or field[(self+w)//w+1][(self+w)%w+1]==self.endSymb and self.keyPos==-1: self.pos+=w
            elif heading=='d' and self//w==(self+1)//w and field[(self+1)//w+1][(self+1)%w+1] in [' ',self.keySymb] or field[(self+1)//w+1][(self+1)%w+1]==self.endSymb and self.keyPos==-1: self.pos+=1
            if self.pos==self.keyPos: self.keyPos=-1
            elif self.pos==self.endPos: self.finished=True
            field[self.pos//w+1][self.pos%w+1]=self.symb
            

class Level:
    def __init__(self, p1, p2, enemies):
        self.field=[[]]
        self.p1=p1
        self.p2=p2
        self.enemies=enemies
        
    def genField(self,width,heigth):
        self.field=[[]]
        for i in range(width+2): self.field[0].append('#')
        for i in range(heigth):
            row=['#']
            for j in range(width): row.append(' ')
            row.append('#')
            self.field.append(row)
        self.field.append(self.field[0])

    def load(self,string,lvlNumber=0):
        level=ast.literal_eval(string)
        width=level['w']
        heigth=level['h']

        self.genField(width,heigth)
        
        for g in level:
            if g not in ['w', 'h', "p1", "p2", "e1", "e2", "k1", "k2"]:
                for obj in level[g]: self.field[obj//width+1][obj%width+1]=g
            for p in [self.p1, self.p2]:
                n=str([self.p1, self.p2].index(p)+1)
                if g=='p'+n: #p.symb
                    p.pos=level[g][0]
                    self.field[p.pos//width+1][p.pos%width+1]=p.symb
                elif g=='k'+n:
                    p.keyPos=level[g][0]
                    self.field[p.keyPos//width+1][p.keyPos%width+1]=p.keySymb
                elif g=='e'+n:
                    p.endPos=level[g][0]
                    self.field[p.endPos//width+1][p.endPos%width+1]=p.endSymb
            if g==self.enemies[-1].symb:
                for e in level[g]: self.enemies.append(Enemy(self.enemies[-1].symb,e))
                for e in self.enemies:
                    if e.pos==-1: self.enemies.remove(e)

        return self.field

    def makeLvl(self):
        w=int(input("Input lvl width: "))
        h=int(input("Input lvl heigth: "))
        if not(w*h>=4 and w>0 and h>0):
            print("The inputed values are too small. You should try again")
            return

        self.genField(w,h)
        graphics={"wall":'#','x':'#','#':'#',"p1":self.p1.symb,'1':self.p1.symb,"player1":self.p1.symb,"1k":self.p1.keySymb,"k1":self.p1.keySymb,"1key":self.p1.keySymb,"key1":self.p1.keySymb,"1e":self.p1.endSymb,"e1":self.p1.endSymb,"1end":self.p1.endSymb,"end1":self.p1.endSymb,"t1":self.p1.endSymb,"p2":self.p2.symb,'2':self.p2.symb,"player2":self.p2.symb,"2k":self.p2.keySymb,"2key":self.p2.keySymb,"k2":self.p2.keySymb,"key2":self.p2.keySymb,"2e":self.p2.endSymb,"2end":self.p2.endSymb,"e2":self.p2.endSymb,"end2":self.p2.endSymb,"t2":self.p2.endSymb,'e':self.enemies[0].symb,"enemy":self.enemies[0].symb,'miprog':self.enemies[0].symb}
        moveCont={'w':-w,'s':w,'a':-1,'d':1}
        cursor='_'
        pos=0
        obj=''
        while obj!="save" or self.p1.pos==-1 or self.p2.pos==-1 or self.p1.endPos==-1 or self.p2.endPos==-1:
            print("pos vv", pos)
            self.field[pos//w+1][pos%w+1]=cursor
            draw(self.field)
            obj=input("Input object to place on ({}, {}): ".format(pos//w,pos%w)).lower().strip()
            self.field[pos//w+1][pos%w+1]=' '
            if obj in graphics:
                self.field[pos//w+1][pos%w+1]=graphics[obj]
            elif obj in moveCont: pos+=(moveCont[obj]-1)

            for i in [self.p1,self.p2]:
                if i.pos==pos: i.pos=-1
                if i.keyPos==pos: i.keyPos=-1
                if i.endPos==pos: i.endPos=-1
                if self.field[pos//w+1][pos%w+1]==i.symb:
                        if i.pos>-1: self.field[i.pos//w+1][i.pos%w+1]=' '
                        i.pos=pos
                elif self.field[pos//w+1][pos%w+1]==i.keySymb:
                        if i.keyPos>-1: self.field[i.keyPos//w+1][i.keyPos%w+1]=' '
                        i.keyPos=pos
                elif self.field[pos//w+1][pos%w+1]==i.endSymb:
                        if i.endPos>-1: self.field[i.endPos//w+1][i.endPos%w+1]=' '
                        i.endPos=pos
                        
            for e in self.enemies:
                if e.pos==pos: self.enemies.remove(e)
            if len(self.enemies)>0 and self.field[pos//w+1][pos%w+1]==self.enemies[-1].symb: self.enemies.append(Enemy(self.enemies[0].symb,pos))
            
            pos+=1
            pos%=w*h
            a=[]
            for k in self.enemies: a.append(k.pos)
            
        self.save()

        self.enemies=[Enemy('\033[1;31;40m~\033[0;37;40m',-1)]

    def makeLvl2(self):
        self.gui=lM.App(tk.Tk())
        self.gui.wait_variable(self.gui.saveVariable)
        self.field=self.gui.getField()
        self.gui.win.destroy()
        self.save()
        

    def save(self):
        saveFile=open("custom.txt",'a')
        savingDict={}
        savingDict['w'], savingDict['h'] = len(self.field[0])-2, len(self.field)-2
        for row in range(1,len(self.field)-1):
            for cell in range(1,len(self.field[0])-1):
                cellValue=self.field[row][cell]
                for p in [self.p1,self.p2]:
                    if cellValue==p.symb: cellValue='p'+str([self.p1, self.p2].index(p)+1)
                    elif cellValue==p.keySymb: cellValue='k'+str([self.p1, self.p2].index(p)+1)
                    elif cellValue==p.endSymb: cellValue='e'+str([self.p1, self.p2].index(p)+1)
                if cellValue !=' ':
                    if  cellValue not in savingDict: savingDict[cellValue]=[]
                    savingDict[cellValue].append((row-1)*(len(self.field[0])-2)+cell-1)
        saveFile.write(str(savingDict)+"\n")
        saveFile.close()
                    
class Enemy:
    def __init__(self,symb,pos=-1):
        self.symb, self.pos=symb,pos

    def __eq__(self,p): return self.pos==p
    def __add__(self,n): return self.pos+n
    def __sub__(self,n): return self.pos-n
    def __floordiv__(self,n): return self.pos//n
    def __mod__(self,n): return self.pos%n

    def dist(self,field,cell):
        w=len(field[0])-2
        h=len(field)-2
        return ((self.pos//w-cell//w)**2+(self.pos%w-cell%w)**2)**0.5
    def a(self,cell,w): return self.pos//w>cell//w #cell is above
    def b(self,cell,w): return self.pos//w<cell//w #cell is below
    def l(self,cell,w): return self.pos%w>cell%w #cell is left
    def r(self,cell,w): return self.pos%w<cell%w #cell is right

    def move(self,field,p1,p2):
        w=len(field[0])-2
        h=len(field)-2
        closer=p1.pos*(self.dist(field,p1.pos)<self.dist(field,p2.pos))+p2.pos*(self.dist(field,p1.pos)>self.dist(field,p2.pos))

        field[self.pos//w+1][self.pos%w+1]=' '
        if self.a(closer,w) and self-w>=0 and (field[(self-w)//w+1][(self-w)%w+1] in [' ',p1.symb,p2.symb]): self.pos-=w
        elif self.l(closer,w) and self//w==(self-1)//w and field[(self-1)//w+1][(self-1)%w+1] in [' ',p1.symb,p2.symb]: self.pos-=1
        elif self.b(closer,w) and self+w<w*h and field[(self+w)//w+1][(self+w)%w+1] in [' ',p1.symb,p2.symb]: self.pos+=w
        elif self.r(closer,w) and self//w==(self+1)//w and field[(self+1)//w+1][(self+1)%w+1] in [' ',p1.symb,p2.symb]: self.pos+=1
        if self.pos==p1.pos: p1.dead=True
        elif self.pos==p2.pos: p2.dead=True
        field[self.pos//w+1][self.pos%w+1]=self.symb
        

def draw(field,name=''):
    nTabs=(abs(4-len(field[0])//20)+(4-len(field[0])//20))//2
    print("\n"*20,"\t"*nTabs,name,"\n")  
    for row in field:
        print("\t"*nTabs,end='')
        for cell in row: print(cell, end='')
        print()
    print("\n"*2)

def update(p1,p2,crrntLevel):
    for i in range(5):
        if not p1.finished:
            p1.move(crrntLevel.field)
            draw(crrntLevel.field)
            if p1.finished:
                print("{} is teleporting!".format(p1.symb))
                t.sleep(0.75)
    for i in range(5):
        if not p2.finished:
            p2.move(crrntLevel.field)
            draw(crrntLevel.field)
            if p2.finished:
                print("{} is teleporting!".format(p2.symb))
                t.sleep(0.75)
    if not (p1.finished and p2.finished):
        for e in crrntLevel.enemies:
            if e.pos!=-1:
                for j in range(5):
                    e.move(crrntLevel.field,p1,p2)
                    draw(crrntLevel.field)
                    if p1.dead or p2.dead: return
                    t.sleep(0.5)

def start(stringList, camp=0, firstTime=0):
    storyFile=open("story.txt",'r')
    thisLevel=Level(p1,p2,enemies)

    lines=storyFile.readlines()
    nLine=0
   
    while lines[nLine].strip()!='-' and camp and firstTime:
        line=lines[nLine]
        print(line)
        t.sleep(3)
        nLine+=1
    line=''
    if camp:
        for i in range(len(lines)):
            if lines[i].strip()=='-': nLine=i
        line=lines[nLine]
    
    for thisString in stringList: 
        thisLevel.enemies=reset(l1.p1,l1.p2,l1.enemies)
        print(thisString)
##        thisString=thisString.replace("Ă·",p1.endSymb[10])
##        thisString=thisString.replace("â€˘",p1.keySymb[10])
        thisLevel.load(thisString)
        if camp:
            nLine+=1
            line=lines[nLine]
        draw(thisLevel.field,line)
        while not p1.dead and not p2.dead and not (p1.finished and p2.finished):  #game loop
            update(p1, p2, thisLevel)
            draw(thisLevel.field)
        if p1.dead or p2.dead:
            print("MIProGs got you!")
            t.sleep(1)
            break
        elif thisString==stringList[-1]:
            print("Congratulations! You've successfully escaped the ship!")
            t.sleep(1)
            break
        t.sleep(1)
    storyFile.close()

def reset(p1,p2,enemies):
    for i in [p1,p2]:
        i.dead=False
        i.finished=False
    enemies=[Enemy('\033[1;31;40m~\033[0;37;40m',-1)]
    l1=Level(p1,p2,enemies)
    return enemies

def tutorial(fileName):
    tutFile=open(fileName,'r',encoding="unicode_escape")
    lines=tutFile.readlines()
    i=0
    while i<len(lines):
        print(lines[i][1:],end='')
        for k in range(i+1,i+int(lines[i][0])):
            lines[k]=lines[k].replace("Ã·",p1.endSymb[10])
            lines[k]=lines[k].replace("â¢",p1.keySymb[10])
            print(lines[k],end='')
        i+=int(lines[i][0])
        u=input("\nPress ENTER to continue \n\n")
    tutFile.seek(0)
    tutFile.close()

def playMusic():
    while mixerAlive:
        pygame.mixer.init()
        pygame.mixer.music.load("soundtrack.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        t.sleep(1)

p1=Player("\033[1;32;40mo\033[0;37;40m",-1,"\033[1;32;40m•\033[0;37;40m","\033[1;32;40m÷\033[0;37;40m")
p2=Player("\033[1;35;40mo\033[0;37;40m",-1,"\033[1;35;40m•\033[0;37;40m","\033[1;35;40m÷\033[0;37;40m")

enemies=[Enemy('\033[1;31;40m~\033[0;37;40m',-1)]

l1=Level(p1,p2,enemies)

file=open("custom.txt","r+")

mixerAlive=True
t1=th.Thread(target=playMusic)
t1.start()

firstChoice=int(input("Welcome to MIProG!\nPlease input a number infront of your chosen action:\n1. Play\n2. Make level\n3. Exit\n\n"))
firstTime=True
while firstChoice in [1,2]:
    if firstChoice==2:
        secondChoice=int(input("Do you know how to use the level creator? \n1. Of course!\n2. No...\n\n"))
        if secondChoice==1:
            print("\nLevel making it is!")
            l1.makeLvl2()
        elif secondChoice==2: tutorial("tut_maker2.txt")
    elif firstChoice==1:
        secondChoice=input("\nWould you like to play:\n1. Premade levels ('campaign')\n2. Custom levels\n3. How do I play?\n\n")
        if int(secondChoice.split()[0])==1:
            print("\n\nStarting the 'campaign'!\n\n")
            campaign=open("campaign.txt",'r')
            start(campaign.readlines(),1,firstTime*secondChoice.split()[-1]!='n')
            campaign.seek(0)
            firstTime=False
            campaign.close()
        elif int(secondChoice)==2:
            custom=open("custom.txt",'r')
            detected=custom.readlines()
            custom.seek(0)
            if len(detected)!=0:
                thirdChoice=int(input("\nDetected "+str(len(detected))+" custom levels. Which one would you like to play?\n"))
                if thirdChoice>0 and thirdChoice<=len(detected): start([detected[thirdChoice-1]])
            else: print("\nThere are no custom levels yet, but you can make one!")
            custom.close()
        elif int(secondChoice)==3: tutorial("tut_game.txt")
    firstChoice=int(input("\n\nWhat would you like to do next?\n1. Play\n2. Make level\n3. Exit\n\n"))

mixerAlive=False
pygame.mixer.quit()

file.close()


