#Tommy Williams
#Marble Game Solver Algorithm
#April 17th, 2020

from math import *
from tkinter import *
import copy

def _create_circle(self,x,y,r,**kwargs):
   return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

#priorities for captures:
c=30 #outter lones pieces
d=23 #lone pieces
e=0 #non-capture pieces
f=12 #distance from center
g=27.3 #average distance from other pieces
h=10 #adjacence of just piece involved in capture
j=5 #Amount of captures
#h is only used once

speed=int(input("Input Run Speed: "))

if speed<1000:
   indicator = False
else:
   indicator = True

class Marble:
   def __init__(self,x,y,r,i,a):
      self.x=x
      self.y=y
      self.r=r
      self.indexY=i 
      self.indexX=a
      self.altIndexY={}
      self.altIndexX={}
      self.obj=canvas.create_circle(x,y,r,fill="grey")
      self.selected=False
      canvas.tag_bind(self.obj,"<Button-1>",lambda event: self.select(event))
      canvas.tag_bind(self.obj,"<Button-2>",lambda event: self.unselect(event))
      
   
   def remove(self):
      global emptyNum
      if self.selected:
         self.unselect("0")
      canvas.delete(self.obj)
      emptyNum += 1      
   
   def remake(self):
      global emptyNum
      self.remove()
      self.obj=canvas.create_circle(self.x,self.y,self.r,fill="grey")
      canvas.tag_bind(self.obj,"<Button-1>",lambda event: self.select(event))
      canvas.tag_bind(self.obj,"<Button-2>",lambda event: self.unselect(event))
      emptyNum -= 1
      
   def select(self,event):
      global selectedNum,selectedList
      print(event.x,event.y)
      canvas.itemconfig(self.obj,fill="red")
      if not self.selected:
         self.selected=True
         selectedNum+=1
      if not self in selectedList:
         selectedList.append(self)
      
   def unselect(self,event):
      global selectedNum,selectedList
      canvas.itemconfig(self.obj,fill="grey")
      if self.selected:
         selectedNum-=1
         self.selected=False
      if self in selectedList:
         selectedList.remove(self)
   
   def capture(self,arg,increment,direction):
      if indicator:
         canvas.delete("q")
         canvas.create_circle(self.x,self.y,self.r+(0.125*self.r),outline="dark green",width=0.125*self.r,tag="q")
      oldX=self.x
      oldY=self.y
      arg.remove()
      marbles.remove(arg)
      mainArray[arg.indexY][arg.indexX]=0
      mainArray[self.indexY][self.indexX]=0
      if direction=="east":
         self.x+=increment*2
         self.indexX+=2
         oldX+=self.r+0.125*self.r
      elif direction=="west":
         self.x-=increment*2
         self.indexX-=2
         oldX-=self.r+0.125*self.r
      elif direction=="north":
         self.y+=increment*2
         self.indexY+=2
         oldY+=self.r+0.125*self.r
      elif direction=="south":
         self.y-=increment*2
         self.indexY-=2
         oldY-=self.r+0.125*self.r
      else:
         print("Error: incorrect direction input")
      mainArray[self.indexY][self.indexX]=self
      self.remake()
      if indicator:
         canvas.create_line(oldX,oldY,self.x,self.y,fill="dark green",arrow=LAST,arrowshape=(32,40,12),width=self.r*0.125,tag="q")
        
   def isNextTo(self,arg,increment):
      xDiff=round(abs(self.x-arg.x),3)
      yDiff=round(abs(self.y-arg.y),3)
      incr=round(increment,3)
      if xDiff==incr:
         if yDiff==0.0:      
            return(True)
      elif yDiff==incr:
         if xDiff==0.0:
            return(True)
      return(False)
       
   def findSide(self,arg): 
      x=round(self.x,3)
      y=round(self.y,3)
      argX=round(arg.x,3)
      argY=round(arg.y,3)
      if x>argX:
         return("west")
      elif x<argX:
         return("east")
      elif y>argY:
         return("south")
      elif y<argY:
         return("north")
      else:
         return("They are the same marble?")
                  
       
class Array:
   def __init__(self,a,m,n):
      self.array=copy.deepcopy(a)
      self.marbles=copy.copy(m)
      self.n=n 
      for i in range(len(self.array)):
         for a in range(len(self.array[i])):
            if isinstance(self.array[i][a],Marble): 
               if not self.array[i][a] in self.marbles:
                  self.marbles.append(self.array[i][a])
      for i in range(len(self.marbles)):
         self.marbles[i].altIndexX[self.n]=self.marbles[i].indexX
         self.marbles[i].altIndexY[self.n]=self.marbles[i].indexY
      self.lonePieces=0
      self.captureMarble="_"
   
   def capture(self,marble1,marble2,direction):
      self.array[marble1.altIndexY[self.n]][marble1.altIndexX[self.n]]=0
      self.array[marble2.altIndexY[self.n]][marble1.altIndexX[self.n]]=0
      y=marble1.altIndexY[self.n]
      x=marble1.altIndexX[self.n]
      if direction=="east":
         x+=2
      elif direction=="west":
         x-=2
      elif direction=="north":
         y+=2
      elif direction=="south":
         y-=2
      else:
         print("incorrect direction entered")
      if self.array[y][x]==0:
         marble1.altIndexX[self.n]=x
         marble1.altIndexY[self.n]=y
         self.array[marble1.altIndexY[self.n]][marble1.altIndexX[self.n]]=marble1
         self.captureMarble=marble1
      else:
         print("Incorrect capture")
         return(False)
      self.marbles.remove(marble2)
      
   def clearCapture(self,marble1,marble2,direction):
      y=marble1.altIndexY[self.n]
      x=marble1.altIndexX[self.n]
      if direction=="east":
         x+=2
      elif direction=="west":
         x-=2
      elif direction=="north":
         y+=2
      elif direction=="south":
         y-=2
      else:
         print("incorrect direction entered")
         print("You entered " + str(direction))
      if y<0 or x<0 or y>6 or x>6:
         return(False)
      if self.array[y][x]==0:
         return(True)
      else:
         return(False)
         
   def isNextTo(self,x1,y1,x2,y2):
      
      if x1==x2:
         if abs(y1-y2)<=1:
            return(True)
      elif y1==y2:
         if abs(x1-x2)<=1:
            return(True)
      return(False)
   
   def findSide(self,marble1,marble2):
      x1=marble1.altIndexX[self.n]
      y1=marble1.altIndexY[self.n]
      x2=marble2.altIndexX[self.n]
      y2=marble2.altIndexY[self.n]
      
      if x1==x2:
         if y1>y2:
            return("south")
         elif y2>y1:
            return("north")
      elif y1==y2:
         if x1>x2:
            
            return("west")
         elif x2>x1:
            return("east")
            
   def piecesTouching(self,marble,dist):
      x=marble.altIndexX[self.n]
      y=marble.altIndexY[self.n]
        
      
      placesX = [x,x,x+1,x-1]
      placesY = [y+1,y-1,y,y]
      if dist==2:
         placesX = [x,x,x,x,x+1,x+1,x+1,x-1,x-1,x-1,x+2,x-2]
         placesY = [y+1,y+2,y-1,y-2,y+1,y-1,y,y+1,y-1,y,y,y]
         
      
      dir = ["north","south","east","west"]
      altDir = ["south","north","west","east"]
      
      pieces = 0
      args=[]
      
      
      for i in range(0,len(placesX)):
         try:
            if placesX[i]<0 or placesY[i]<0:
               raise IndexError
            arg = self.array[placesY[i]][placesX[i]]
            if isinstance(arg,Marble):
               args.append([arg,dir[i],altDir[i]])
               pieces+=1
         except IndexError:
            pass    
      return(pieces,args)
   def possibleCaptures(self):
      captures=[]
      for i in range(0,len(self.marbles)):
         x=self.marbles[i].altIndexX[self.n]
         y=self.marbles[i].altIndexY[self.n]
         
         exes=[x,x,x+1,x-1]
         eyes=[y+1,y-1,y,y]
         
         for e in range(len(exes)):
            try:
               if exes[e]<0 or eyes[e]<0:
                  raise IndexError
               
               other = self.array[eyes[e]][exes[e]]
               
               if isinstance(other,Marble):
                  x1=self.marbles[i].altIndexX[self.n]
                  y1=self.marbles[i].altIndexX[self.n]
                  x2=other.altIndexX[self.n]
                  y2=other.altIndexX[self.n]
                  if self.isNextTo(x1,y1,x2,y2): 
                     direction=self.findSide(self.marbles[i],other)
                     if self.clearCapture(self.marbles[i],other,direction)==True:
                        locX=captureLocation(x,y,direction,1)[0]
                        locY=captureLocation(x,y,direction,1)[1]
                        captures.append((self.marbles[i],other,direction,locX,locY))
                    
            except IndexError:
               pass
      return(captures)  
   def checkLonePieces(self):
      lonePieces=0
      captures=self.possibleCaptures()
      
      for i in range(len(self.marbles)):
         
         farNessCentX=abs(self.marbles[i].altIndexX[self.n]-3)
         farNessCentY=abs(self.marbles[i].altIndexY[self.n]-3)
         farNessCentDist = float(farNessCentX**2+farNessCentY**2)**0.5
         
         if len(self.marbles)>=0:            
            farNessCentDist-=2
            farNessCentDist*=5
            if farNessCentDist<0:
               farNessCentDist=0
         
         if not self.marbles[i].obj==self.captureMarble.obj:
            if len(self.marbles)>=7:
               lonePieces+=farNessCentDist*f
            
         pieces=self.piecesTouching(self.marbles[i],1)
         
         if pieces[0]==0:
            
            touchingCapture=False
            
            for p in range(len(captures)):
               
               
               if self.isNextTo(self.marbles[i].altIndexX[self.n],self.marbles[i].altIndexY[self.n],captures[p][3],captures[p][4]):
                  if captures[p][2]=="east" or captures[p][2]=="west":
                     if self.marbles[i].altIndexX[self.n]==captures[p][3]:
                        if abs(self.marbles[i].altIndexY[self.n]-captures[p][4])==1:
                           if len(marbles)<=5:
                              lonePieces-=d*6
                        
                  elif captures[p][2]=="north" or captures[p][2]=="south":
                     if self.marbles[i].altIndexY[self.n]==captures[p][4]:
                        if abs(self.marbles[i].altIndexX[self.n]-captures[p][3])==1:
                           if len(marbles)<=5:
                              lonePieces-=d*6
                        
                  touchingCapture=True
                  
            if touchingCapture==False: 
               if len(marbles)<=15: 
                       
                  lonePieces+=c*6
               else:
                  lonePieces+=c
            else:  
               if len(marbles)<=15:
                  lonePieces+=d*3
               else:
                  lonePieces+=d
         else:
            capture=False
            for p in range(len(pieces[1])):
               capture1 = self.clearCapture(self.marbles[i],pieces[1][p][0],pieces[1][p][1])
               capture2 = self.clearCapture(pieces[1][p][0],self.marbles[i],pieces[1][p][2])
               if capture1 or capture2:
                  capture=True
            if capture==False:
               lonePieces+=e
               
         farNessDicts=[]
         for a in range(0,len(self.marbles)):
            if not a==i:
               farNessX=abs(self.marbles[i].altIndexX[self.n]-self.marbles[a].altIndexX[self.n])
               farNessY=abs(self.marbles[i].altIndexY[self.n]-self.marbles[a].altIndexX[self.n])
               farNessDict=(farNessX**2+farNessY**2)**0.5
               farNessDicts.append(farNessDict)
         farNess=0
         for a in range(len(farNessDicts)):
            farNess+=farNessDicts[a]
         farNess=farNess/len(farNessDicts)
         if len(self.marbles)<=15:
           lonePieces+=farNess*g*3
            
         else:
            lonePieces+=farNess*g
      lonePieces=lonePieces/len(self.marbles)  
      if adjacence==True:
         lonePieces+=h
      else:
         lonePieces+=-1*h
      self.lonePieces=lonePieces
      
selectedNum = 0
selectedList = []
emptyList = []
emptyNum = 0
adjacence=False
  
width,height = 800,800
 
root=Tk()       
canvas = Canvas(root,width=width,height=height,bg="white")
   
middle=width/2
boardR=width*float(11)/24
boardD=boardR*2
increment=boardD/float(8)
   
   
canvas.create_circle(middle,middle,boardR)

mainArray = [
   ["_","_", 0 , 0 , 0 ,"_","_"],
   ["_","_", 0 , 0 , 0 ,"_","_"],
   [ 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
   [ 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
   [ 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
   ["_","_", 0 , 0 , 0 ,"_","_"],
   ["_","_", 0 , 0 , 0 ,"_","_"]
]
marbles=[]
marR = boardD/float(17)
for i in range(0,7):
   marY = middle-boardR+increment+float(i)/8*boardD
   if i<=1 or i>=5: 
      for a in range(0,3):
         marX = middle-increment+float(a)/8*boardD
         m=Marble(marX,marY,marR,i,a+2)
         marbles.append(m)
         mainArray[i][a+2]=marbles[len(marbles)-1]
            
   else:
      for a in range(0,7):
         marX = middle-increment*3+float(a)/8*boardD
         m=Marble(marX,marY,marR,i,a)
         marbles.append(m)
         mainArray[i][a]=marbles[len(marbles)-1]
            
   
   
setUp=False
inGame=False
boundList=[] 
canvas.create_line(middle-boardR,middle,middle+boardR,middle,fill="blue")
canvas.create_line(middle,middle-boardR,middle,middle+boardR,fill="blue")
canvas.pack()             

def marblesAdjacentTo(indexX,indexY,capturedPiece):
   smiy=[indexY+1,indexY-1,indexY,indexY]
   smix=[indexX,indexX,indexX+1,indexX-1]
   if isinstance(capturedPiece,Marble):
      try:
         for i in range(0,len(smix)+1):
            if smix[i]==capturedPiece.indexX and smiy[i]==capturedPiece.indexY:
               del smix[i]
               del smiy[i]
               break     
      except:
         print("capturedPiece is not touching spot that is being checked")
   for e in range(len(smix)):
      try:
         arg = mainArray[smiy[e]][smix[e]] 
         if smiy[e]<0 or smix[e]<0 or smiy[e]>6 or smix[e]>6:
            raise IndexError
         if (not isinstance(arg,str)) and (not isinstance(arg,int)):
            return(True)
      except IndexError:
         pass
   return(False)

def captureLocation(x,y,direction,increment):
   if direction=="east":
      x+=2*increment
   elif direction=="west":
      x-=2*increment
   elif direction=="north":
      y+=2*increment
   elif direction=="south":
      y-=2*increment
   else:
      print("incorrect direction entered")
   return((x,y))
   
def inBoundaries(x,y):
      global middle,boardR,incrementf
      x=round(x,3)
      y=round(y,3)
      incr=round(increment,3)
      if x>middle-boardR and x<middle+boardR:
         if x>=middle-incr and x<=middle+incr:
            if y>middle-boardR and y<middle+boardR:
               return(True)
         else:
            if y>=middle-incr and y<=middle+incr:
               return(True)
      return(False)

def captureIndexLocation(marble1,marble2):
   if not marble1.isNextTo(marble2,increment):
      print("marbles can not capture each other")
      return([-1,-1])
   direction=marble1.findSide(marble2)
   if direction=="east":
      return([marble1.indexX+2,marble1.indexY])
   elif direction=="west":
      return([marble1.indexX-2,marble1.indexY])
   elif direction=="north":
      return([marble1.indexX,marble1.indexY+2])
   elif direction=="south":
      return([marble1.indexX,marble1.indexY-2])

      
def clearCapture(x,y,direction,increment):
   if direction=="east":
      posX=x+increment*2
      posY=y
   elif direction=="west":
      posX=x-increment*2
      posY=y
   elif direction=="north":
      posX=x
      posY=y+increment*2
   elif direction=="south":
      posX=x
      posY=y-increment*2
   for i in range(len(marbles)):
      if round(marbles[i].x,3)==round(posX,3) and round(marbles[i].y,3)==round(posY,3):
            return(False)      
   return(inBoundaries(posX,posY))
   

def yButton(event):
   global pause
   if pause==True:
      pause=False
   else:
      pause=True
      
root.bind("<y>",yButton)
pause=False
   
def possibleCaptures():
   global adjacence
   captures=[]
   for i in range(0,len(marbles)):
      indexX=marbles[i].indexX
      indexY=marbles[i].indexY
      smiy=[indexY+1,indexY-1,indexY,indexY]
      smix=[indexX,indexX,indexX+1,indexX-1]
      for e in range(len(smix)):
         try:
            arg = mainArray[smiy[e]][smix[e]] 
            
            if (not isinstance(arg,str)) and (not isinstance(arg,int)):
               
               if marbles[i].isNextTo(arg,increment):
                  direction = marbles[i].findSide(arg)
                  if clearCapture(marbles[i].x,marbles[i].y,direction,increment):
                     loc=captureIndexLocation(marbles[i],arg)
                     locX=loc[0]
                     locY=loc[1]
                     adjacence=marblesAdjacentTo(locX,locY,arg)
                     captures.append([marbles[i],arg,direction])
         except IndexError:
            pass
   return(captures)         
     
   
def tick():
   global setUp,selectedNum,increment,selectedList,inGame,speed,pause
   while pause==True:
      pass
      
   
   if setUp==False:
      if selectedNum==1:
         i=0 
         while i<len(marbles):
            if marbles[i].selected:
               mainArray[marbles[i].indexY][marbles[i].indexX]=0
               marbles[i].unselect("0")
               marbles[i].remove() 
               marbles.remove(marbles[i])
               
               break
            else:
               i+=1  
         setUp=True
         inGame=True
      canvas.after(speed,tick)
   
   elif inGame==True:
   
      captures=possibleCaptures()
      
      if len(captures)==0:
         inGame=False
         
      else:
         
         lowestNum = 100000
         lowestIndex = 100000
         
         
         for i in range(0,len(captures)):
            tempArray=Array(mainArray,marbles,"p")
            if (tempArray.capture(captures[i][0],captures[i][1],captures[i][2]))==False:
               printArray(mainArray)
               print(captures[i])
               print(captures[i][0].indexY,captures[i][0].indexX)
               print(captures[i][1].indexY,captures[i][1].indexX)
               del tempArray
            else:
               
               tempArray.checkLonePieces()
               if tempArray.lonePieces<lowestNum:
                  if len(marbles)>31:
                     print(tempArray.lonePieces)
                  secondNum=lowestNum
                  secondIndex=lowestIndex
                  lowestNum=tempArray.lonePieces  
                  lowestIndex=i
               del tempArray
         capNum=lowestIndex
         marble1=captures[capNum][0]
         marble2=captures[capNum][1]
      
         direction = marble1.findSide(marble2)
         marble1.capture(marble2,increment,direction)
      
     
      captures=[]
      canvas.after(speed,tick)
            
   else:
      marblesLeft=len(marbles)
      print("Ended with " + str(marblesLeft) + " marble(s) left.")
root.after(speed,tick)
root.mainloop()


 


