#  112 term project
#  Name: Mi Zhang
#  Andrew id: mizhang
#  Create date: 04/07/2015


import math
import random
from Tkinter import*
import eventBasedAnimation
import datetime
import copy
import sys
import os

class Jewels(object):
    def __init__(self,row,col):# initialize value for each variable
        (self.row,self.col) = (row,col)
        self.grid=60
        (self.leftMargin,self.rightMargin)=(348,888)
        (self.upMargin,self.downMargin)=(40,580)
        self.y=row*self.grid+self.upMargin
        self.x=col*self.grid+self.leftMargin
        (self.merge,self.move) = (False,False)
        (self.moveTox, self.moveToy)= (None,None)
        (self.speed,self.r)= (20,30)
        (self.isOneColorMerge,self.isBoom,self.isRowColMerge)=(False,False,False)
        (self.drawBoom,self.drawColor,self.drawRowCol)=(False,False,False)
        (self.photo,self.photo2,self.photo3)=(None,None,None)
        self.photo4 = PhotoImage(file="picture/photo4.gif")

    # rgb function to get specific color 
    def rgb(self,red,green,blue):
        return "#%02x%02x%02x" % (red,green,blue)
    
    # move each jewel with static speed
    def moveItem(self):
        if(self.move == True):  
            if(self.x!=self.moveTox or self.y!= self.moveToy):
                if(self.moveTox-self.x>0):
                    self.x+=self.speed
                elif(self.moveTox-self.x<0):
                    self.x-=self.speed                   
                if(self.moveToy-self.y>0):
                    self.y+=self.speed
                elif(self.moveToy-self.y<0):
                    self.y-=self.speed
            else:
                self.move = False
                (self.moveTox,self.moveToy)=(None,None)
    
    # draw jewels in differend situation 
    def draw(self,canvas):
        if(self.y>=self.upMargin-10 and self.y<=(9*self.grid+self.upMargin)):
            if(self.isOneColorMerge==False and self.isBoom==False and \
                self.isRowColMerge == False):
                canvas.create_image(self.x,self.y,anchor=NW,image=self.photo)
            elif(self.isOneColorMerge==True):
                canvas.create_image(self.x,self.y,anchor=NW,image=self.photo2)
            elif(self.isBoom==True):
                canvas.create_image(self.x,self.y,anchor=NW,image=self.photo3)
            elif(self.isRowColMerge == True):
                canvas.create_image(self.x,self.y,anchor=NW,image=self.photo4)
    
    # draw hint when necessary
    def drawSpecial(self,canvas):
        if(self.y>=self.upMargin-10):
            color = self.rgb(122,232,181)
            (x,y,r)=(self.x,self.y,self.grid)
            canvas.create_line(x,y,x+r,y,fill = color,width=3)
            canvas.create_line(x+r,y,x+r,y+r,fill = color,width=3)
            canvas.create_line(x+r,y+r,x,y+r,fill = color,width=3)
            canvas.create_line(x,y+r,x,y,fill = color,width=3)

# jewels class with different color 
class Rose(Jewels):
    def __init__(self,row,col):
        super(Rose,self).__init__(row,col)
        self.photo = PhotoImage(file="picture/rose.gif")
        self.photo2 = PhotoImage(file="picture/rose2.gif")
        self.photo3 = PhotoImage(file="picture/rose3.gif")
        self.color = "rose"

class Red(Jewels):
    def __init__(self,row,col):
        super(Red,self).__init__(row,col)
        self.photo = PhotoImage(file="picture/red.gif")
        self.photo2 = PhotoImage(file="picture/red2.gif")
        self.photo3 = PhotoImage(file="picture/red3.gif")
        self.color = "red"
        
class Yellow(Jewels):
    def __init__(self,row,col):
        super(Yellow,self).__init__(row,col)
        self.photo = PhotoImage(file="picture/yellow.gif")
        self.photo2 = PhotoImage(file="picture/yellow2.gif")
        self.photo3 = PhotoImage(file="picture/yellow3.gif")
        self.color = "yellow"
        
class Blue(Jewels):
    def __init__(self,row,col):
        super(Blue,self).__init__(row,col)
        self.photo = PhotoImage(file="picture/blue.gif")
        self.photo2 = PhotoImage(file="picture/blue2.gif")
        self.photo3 = PhotoImage(file="picture/blue3.gif")
        self.color = "blue"

class Orange(Jewels):
    def __init__(self,row,col):
        super(Orange,self).__init__(row,col)
        self.photo = PhotoImage(file="picture/orange.gif")
        self.photo2 = PhotoImage(file="picture/orange2.gif")
        self.photo3 = PhotoImage(file="picture/orange3.gif")
        self.color = "orange"

class White(Jewels):
    def __init__(self,row,col):
        super(White,self).__init__(row,col)
        self.photo = PhotoImage(file="picture/white.gif")
        self.photo2 = PhotoImage(file="picture/white2.gif")
        self.photo3 = PhotoImage(file="picture/white3.gif")
        self.color = "white"
     
class Gold(Jewels):
    def __init__(self,row,col):
        super(Gold,self).__init__(row,col)
        self.photo = PhotoImage(file="picture/gold.gif")
        self.color = "gold"

    def draw(self,canvas):
        canvas.create_image(self.x,self.y,anchor=NW,image=self.photo)

class Soil(Jewels):
    def __init__(self,row,col):
        super(Soil,self).__init__(row,col)
        self.photo = PhotoImage(file="picture/soil.gif")
        self.color = "soil"

    def draw(self,canvas):
        canvas.create_image(self.x,self.y,anchor=NW,image=self.photo)

# compute the score 
def computeScore(available):
    num = len(available)
    return 10*(3+num-1)*(num-3)/2+30

class JewelsGame(eventBasedAnimation.Animation):
    def onInit(self):
        self.initFlag()
        self.initPicture()    
        (self.drawTime,self.drawAdventure)=(False,False)
        (self.drawPlay,self.drawOption,self.drawRecord) = (False,False,False)
        (self.drawQuit,self.drawHelp,self.drawIntroduction) = (False,False,False)
        (self.changeBackColorTime,self.changeBackColorAdventure)=(False,False)
        (self.rows,self.cols,self.score) = (10,10,0)
        (self.frmrow,self.frmcol,self.torow,self.tocol)=(None,None,None,None)
        self.mergecount = None  
        self.firstpress =  ["waiting",None,None]
        self.secondpress = ["waiting",None,None]
        self.emptyColor = "empty"
        self.board = [([self.emptyColor] * self.cols) for row in xrange(self.rows)]
        self.boardtwo = [([self.emptyColor] * (self.cols-2)) for row in xrange(self.rows)]
        (self.recordTimeMode,self.recordAdventureMode)=([],[])
        self.initJewels()
        self.initAdventure()
        self.getRecord()

    def initPicture(self):
        self.beginScreen = PhotoImage(file="picture/begin.gif")
        self.TimeModeBackground=PhotoImage(file="picture/TimeModebackground.gif")
        self.modeSelecBackground = PhotoImage(file="picture/modeselection.gif")
        self.AdventureModeBackground=PhotoImage(file="picture/Adventurebackground.gif")
        self.column=PhotoImage(file="picture/column.gif")
        self.ScoreBoardBackground = PhotoImage(file="picture/ScoreBoardbackground.gif")
        self.Yesbutton = PhotoImage(file="picture/Yesbutton.gif")
        self.Nobutton = PhotoImage(file="picture/Nobutton.gif")
        self.beginScreenPlay = PhotoImage(file="picture/play.gif")
        self.beginScreenOption = PhotoImage(file="picture/option.gif")
        self.beginScreenRecord = PhotoImage(file="picture/record.gif")
        self.beginScreenHelp = PhotoImage(file="picture/help.gif")
        self.beginScreenQuit = PhotoImage(file = "picture/quit.gif")
        self.modeSelectTime = PhotoImage(file= "picture/timebutton.gif")
        self.modeSelectAdventure = PhotoImage(file = "picture/adventurebutton.gif")
        self.introduction = PhotoImage(file="picture/introduction.gif")
        self.TimeModepath="recordTimeMode.txt"
        self.AdventureModepath = "recordAdventureMode.txt"
    
    def initFlag(self):
        (self.isGameStart, isGameOver) = (False,False)
        (self.isTimeMode ,self.isAdventureMode)= (False,False)
        (self.isScoreBoard,self.hasExchange)=(False,None)
        (self.mouseX ,self.mouseY)= (None,None)
        (self.mouseReleaseX,self.mouseReleaseY)=(None,None)
        (self.mouseMoveX,self.mouseMoveY)=(None,None)
        (self.hinttime,self.hintadventure)=(None,None)
        (self.isBeginScreen, self.modeselect)=(True,False)
        (self.isOptionMode, self.isHelpMode)= (False,False)
        (self.time ,self.defaulttime) = (900,900)
        (self.isRecordTimeMode,self.isRecordAdventureMode) = (False,False)
        (self.drawBoom,self.drawColor,self.drawRowCol)=(None,None,None)
        (self.layercount,self.goldscore) = (0,0)
        (self.RowColCount,self.RowColGrid) = (5,40)
        (self.drawColorCount,self.r)=(10,30)
        (self.easy,self.hard)=(True,False)
        (self.hintTimecount,self.timeAutoCount,self.defaultTime) = (30,30,30)
        (self.drawHintTimeMode,self.drawHintAdventureMode)=(False,False)
        (self.isTimeAuto,self.isAdventureAuto)=(False,False)   

    def initJewels(self):
        for i in xrange(self.rows):
            for j in xrange(self.cols):
                if(self.easy==True):
                    choice = random.choice(["yellow","blue","red","rose"])
                elif(self.hard==True):
                    choice = random.choice(["yellow","red","orange","blue",\
                        "rose","white"])
                if(choice =="yellow"):
                    self.board[i][j]=Yellow(i,j)
                elif(choice =="red"):
                    self.board[i][j]=Red(i,j)
                elif(choice =="orange"):
                    self.board[i][j]=Orange(i,j)
                elif(choice =="blue"):
                    self.board[i][j]=Blue(i,j)
                elif(choice =="rose"):
                    self.board[i][j]=Rose(i,j)
                elif(choice =="white"):
                    self.board[i][j]=White(i,j)
    
    def initAdventure(self):
        for i in xrange(self.rows-3):
            for j in xrange(self.cols-2):
                if(self.easy==True):
                    choice = random.choice(["yellow","blue","red","rose"])
                elif(self.hard==True):
                    choice = random.choice(["yellow","red","orange","blue",\
                        "rose","white"])
                if(choice =="yellow"):
                    self.boardtwo[i][j]=Yellow(i,j)
                elif(choice =="red"):
                    self.boardtwo[i][j]=Red(i,j)
                elif(choice =="orange"):
                    self.boardtwo[i][j]=Orange(i,j)
                elif(choice =="blue"):
                    self.boardtwo[i][j]=Blue(i,j)
                elif(choice =="rose"):
                    self.boardtwo[i][j]=Rose(i,j)
                elif(choice =="white"):
                    self.boardtwo[i][j]=White(i,j)
        for i in xrange(self.rows-3,self.rows):
            for j in xrange(self.cols-2):
                choice = random.choice(["soil","gold"])
                if(choice =="soil"):
                    self.boardtwo[i][j]=Soil(i,j)
                elif(choice =="gold"):
                    self.boardtwo[i][j]=Gold(i,j)

    #  read the record from a txt file 
    def getRecord(self):
        timemode = open(self.TimeModepath)
        timeModerecord=timemode.read()
        timemode.close()
        timeModerecord=timeModerecord.splitlines()
        for record in timeModerecord:
            self.recordTimeMode.append(int(record))
        adventuremode = open(self.AdventureModepath)
        recordAdventureMode=adventuremode.read()
        adventuremode.close()
        recordAdventureMode=recordAdventureMode.split()
        for record in recordAdventureMode:
            self.recordAdventureMode.append(int(record))
    
    # when user finish a roll of time mode game ,update and save it into record
    def updateScoreTimeMode(self,mode):
        if(mode=="timemode"):
            self.recordTimeMode.append(self.score)
            self.recordTimeMode.sort()
            self.recordTimeMode.reverse()
            self.recordTimeMode=self.recordTimeMode[0:3]
            newRecord = ""
            for item in self.recordTimeMode:
                newRecord=newRecord+str(item)+"\n"
            timemode = open(self.TimeModepath,"w")
            timemode.write(newRecord)
            timemode.close()
        elif(mode =="adventuremode"):
            self.recordAdventureMode.append(self.score)
            self.recordAdventureMode.sort()
            self.recordAdventureMode.reverse()
            self.recordAdventureMode=self.recordAdventureMode[0:3]
            newRecord = ""
            for item in self.recordAdventureMode:
                newRecord=newRecord+str(item)+"\n"
            timemode = open(self.AdventureModepath,"w")
            timemode.write(newRecord)
            timemode.close()

    # easy or hard mode level to choose 
    # magic number are specific coordinate on screen 
    def runOptionMode(self):
        if(self.isOptionMode==True):
            if(self.mouseX>450 and self.mouseX<550 and \
                self.mouseY>390 and self.mouseY<410):
                self.isBeginScreen = True
                self.isOptionMode = False
                self.isGameStart = False
                (self.mouseX,self.mouseY)=(None,None)
            if(self.mouseX>310 and self.mouseX<450 and\
                self.mouseY>330 and self.mouseY<360):
                self.easy=True
                self.hard=False
            if(self.mouseX>560 and self.mouseX<700 and\
                self.mouseY>330 and self.mouseY<360):
                self.hard=True
                self.easy=False
    
    # find the available diamond with same color toward left for time mode
    def getAvailableLeft(self,row,col):
        if(type(self.board[row][col])!=str):
            Color = self.board[row][col].color
            available=[]
            for i in xrange(col-1,-1,-1):
                if(self.isLegal(row,i)):
                    if(self.board[row][i].color == Color):
                        available.append((row,i))
                    else:
                        break
            return available

    # find the available diamond with same color toward right for time mode
    def getAvailableRight(self,row,col):
        if(self.isLegal(row,col)):
            Color = self.board[row][col].color
            available=[]
            for i in xrange(col+1,self.cols):
                if(self.isLegal(row,i)):
                    if(self.board[row][i].color == Color):
                        available.append((row,i))
                    else:
                        break
            return available
    
    # find the available diamond with same color toward up direction 
    # for time mode
    def getAvailableUp(self,row,col):
        if(type(self.board[row][col])!=str):
            Color = self.board[row][col].color
            available=[]
            for i in xrange(row-1,-1,-1):
                if(self.isLegal(i,col)):
                    if(self.board[i][col].color == Color):
                        available.append((i,col))
                    else:
                        break
            return available

    # find the available diamond with same color toward down direction 
    # for time mode
    def getAvailableDown(self,row,col):
        if(type(self.board[row][col])!=str):
            Color = self.board[row][col].color
            available=[]
            for i in xrange(row+1,self.rows):
                if(self.isLegal(i,col)):
                    if(self.board[i][col].color == Color):
                        available.append((i,col))
                    else:
                        break
            return available
    
    # find the available diamond with same color toward left 
    # for adventure mode
    def getAvailableLefttwo(self,row,col):
        if(type(self.boardtwo[row][col])!=str):
            Color = self.boardtwo[row][col].color
            available=[]
            for i in xrange(col-1,-1,-1):
                if(self.isLegaltwo(row,i)):
                    if(self.boardtwo[row][i].color == Color):
                        available.append((row,i))
                    else:
                        break
            return available

    # find the available diamond with same color toward right
    # for adventure mode
    def getAvailableRighttwo(self,row,col):
        if(self.isLegaltwo(row,col)):
            Color = self.boardtwo[row][col].color
            available=[]
            for i in xrange(col+1,8):
                if(self.isLegaltwo(row,i)):
                    if(self.boardtwo[row][i].color == Color):
                        available.append((row,i))
                    else:
                        break
            return available
    
    # find the available diamond with same color toward up direction  
    # for adventure mode
    def getAvailableUptwo(self,row,col):
        if(type(self.boardtwo[row][col])!=str):
            Color = self.boardtwo[row][col].color
            available=[]
            for i in xrange(row-1,-1,-1):
                if(self.isLegaltwo(i,col)):
                    if(self.boardtwo[i][col].color == Color):
                        available.append((i,col))
                    else:
                        break
            return available
    
    # find the available diamond with same color toward down direction  
    # for adventure mode
    def getAvailableDowntwo(self,row,col):
        if(type(self.boardtwo[row][col])!=str):
            Color = self.boardtwo[row][col].color
            available=[]
            for i in xrange(row+1,self.rows):
                if(self.isLegaltwo(i,col)):
                    if(self.boardtwo[i][col].color == Color):
                        available.append((i,col))
                    else:
                        break
            return available
    
    # find diamond with same color on one with position row, col fromt four 
    # directin, this helper function is called in time mode 
    def getAvailable(self,row,col):
        if(type(self.board[row][col])!=str):
            Color = self.board[row][col].color
            Updown=[]
            LeftRight=[]
            available=[(row,col)]
            LeftRight=LeftRight+self.getAvailableLeft(row,col)
            LeftRight=LeftRight+self.getAvailableRight(row,col)
            if(len(LeftRight)>=2):
                available+=LeftRight
            Updown+=self.getAvailableUp(row,col)
            Updown+=self.getAvailableDown(row,col)
            if(len(Updown)>=2):
                available+=Updown
            if(len(available)>=3):
                return available
            else:
                return []
        else:
            return []
     
    # find diamond with same color on one with position row, col fromt four 
    # directin, this helper function is called in adventure mode 
    def getAvailableTwo(self,row,col):
        if(self.isLegaltwo(row,col)):
            color = self.boardtwo[row][col].color
            (Updown,LeftRight)=([],[])
            available=[(row,col)]
            LeftRight+=self.getAvailableLefttwo(row,col)
            LeftRight+=self.getAvailableRighttwo(row,col)
            if(len(LeftRight)>=2):
                available+=LeftRight
            Updown+=self.getAvailableUptwo(row,col)
            Updown+=self.getAvailableDowntwo(row,col)
            if(len(Updown)>=2):
                available+=Updown
            if(len(available)>=3):
                return available
            else:
                return []
        else:
            return []
    
    # eliminate and possible diamond on the whole board automaticlly for time mode 
    # this is a helper function for time mode 
    def mergeItemHelpOne(self,available):
        for item in available:
            (mergerow,mergecol)=(item[0],item[1])
            if(self.isLegal(mergerow,mergecol)):
                if(self.board[mergerow][mergecol].isOneColorMerge==False and\
                   self.board[mergerow][mergecol].isBoom == False and \
                   self.board[mergerow][mergecol].isRowColMerge==False):
                   self.board[mergerow][mergecol]="empty"
                elif(self.board[mergerow][mergecol].isOneColorMerge==True):
                    color =  self.board[mergerow][mergecol].color
                    self.clearOneColor(color)
                elif(self.board[mergerow][mergecol].isBoom == True):
                    self.clearBoom(mergerow,mergerow)
                elif(self.board[mergerow][mergecol].isRowColMerge== True):
                    self.clearRowCol(mergerow,mergerow)
        self.score+=len(available*10)
    
    # helper function two for time mode eliminate diamond automaticlly 
    def mergeItemHelpTwo(self,available,row,col):
        for item in available:
            if(item[0]!=row or item[1]!=col):
                (mergerow,mergecol)=(item[0],item[1])
                if(self.board[mergerow][mergecol].isOneColorMerge==False):
                    self.board[mergerow][mergecol]="empty"
    
    # this function is called by runTimeMode, 
    # eliminate all possible diamond with same color after the user swap
    def mergeItem(self,row,col):
        if (self.isLegal(row,col)):
            available=self.getAvailable(row,col)
            if(len(available)!=0):
                self.mergecount=True
                if(len(available)<=3):
                    self.mergeItemHelpOne(available)
                else:
                    self.mergeItemHelpTwo(available,row,col)
                    if(len(available)>5):
                        self.board[row][col].isOneColorMerge=True
                    if(len(available)==4):
                        self.board[row][col].isBoom=True
                    if(len(available)==5):
                        self.board[row][col].isRowColMerge=True
                    self.score+=computeScore(available)
    
    # helper function when eliminate and move diamond 
    # update a flag variable for draw special effect
    def updateBoom(self):
        if(self.drawBoom!=None):
            (x,y)=(self.drawBoom[2]*60+348,self.drawBoom[1]*60+40)
            if(x-self.r>x-90 or y+self.r<y+90):
                self.r+=10
            else:
                self.r=30
                self.drawBoom=None
    
    # helper function when eliminate and move diamond 
    # update a flag variable for draw "rowcol" special effect
    def updateRowCol(self):
        if(self.drawRowCol!=None):
            (x,y)=(self.drawRowCol[2]*60+348,self.drawRowCol[1]*60+40)
            if(self.RowColCount>0):
                self.RowColCount-=1
                self.RowColGrid+=4
            else:
                self.RowColCount=5
                self.RowColGrid=40
                self.drawRowCol=None
    
    # update a flag variable for draw special effect of one color 
    def updateOnecolor(self):
        if(self.drawColor!=None):
            if(self.drawColorCount>0):
                self.drawColorCount-=1
            else:
                self.drawColor=None
                self.drawColorCount=10
    
    # helper function for eliminate diamond with same color on adventure
    # mode. this function is called by mergeItemTwo
    def mergeItemTwoHelpOne(self,available,row,col):
        for item in available:
            if(item[0]!=row or item[1]!=col):
                (mergerow,mergecol)=(item[0],item[1])
                if(self.boardtwo[mergerow][mergecol].isOneColorMerge==False):
                    self.boardtwo[mergerow][mergecol]="empty"
                if(mergerow<9):
                    if(self.boardtwo[mergerow+1][mergecol]!='empty'):
                        if(self.boardtwo[mergerow+1][mergecol].color=='soil' or 
                            self.boardtwo[mergerow+1][mergecol].color=='gold'):
                            if(self.boardtwo[mergerow+1][mergecol].color=='gold'):
                                self.goldscore+=10
                            self.boardtwo[mergerow+1][mergecol]='empty' 
        if(len(available)>5):
            self.boardtwo[row][col].isOneColorMerge=True
            self.time=self.time+6*len(available)
        if(len(available)==4):
            self.boardtwo[row][col].isRowColMerge=True
            self.time=self.time+4*len(available)
        if(len(available)==5):
            self.boardtwo[row][col].isRowColMerge=True
            self.time=self.time+5*len(available)
    
    # helper function for eliminate diamond with same color on adventure
    # mode. this function is called by mergeItemTwo
    # if diamond is adjavent to a soil or gold. then eliminate the gold
    def mergeItemTwoHelpTwo(self,available):
        for item in available:
            (mergerow,mergecol)=(item[0],item[1])
            self.boardtwo[mergerow][mergecol]="empty"
            if(mergerow<9):
                if(self.boardtwo[mergerow+1][mergecol]!='empty'):
                    if(self.boardtwo[mergerow+1][mergecol].color=='soil' or 
                        self.boardtwo[mergerow+1][mergecol].color=='gold'):
                        if(self.boardtwo[mergerow+1][mergecol].color=='gold'):
                            self.goldscore+=10
                        self.boardtwo[mergerow+1][mergecol]='empty' 
        self.score+=len(available*10)
        self.time+=len(available)
    
    # eliminate all possible diamond with same color after user's swap
    def mergeItemTwo(self,row,col):
        if (self.isLegaltwo(row,col)):
            available=self.getAvailableTwo(row,col)
            if(len(available)>=3):
                self.mergecount=True
            if(len(available)==3):
                self.mergeItemTwoHelpTwo(available)
            else:
                self.mergeItemTwoHelpOne(available,row,col)
                self.score+=computeScore(available)
            if(self.time>self.defaulttime):
                self.time=self.defaulttime
    
    # if one specific column have some diamond been eliminated, generate a new
    # one with random color based on "easy" or "hard" selection 
    def generateDiamond(self,col):
        colEmpty=self.getColEmpty(col)
        for i in xrange(colEmpty):
            if(self.easy==True):
                choice = random.choice(["yellow","red","orange","blue"])
            elif(self.hard==True):
                choice = random.choice(["yellow","red","orange","blue",\
                    "rose","white"])
            dist=i-colEmpty
            if(choice =="yellow"):
                self.board[i][col]=Yellow(dist,col)
            elif(choice =="red"):
                self.board[i][col]=Red(dist,col)
            elif(choice =="orange"):
                self.board[i][col]=Orange(dist,col)
            elif(choice =="blue"):
                self.board[i][col]=Blue(dist,col)
            elif(choice =="rose"):
                self.board[i][col]=Rose(dist,col)
            elif(choice =="white"):
                self.board[i][col]=White(dist,col)
            self.board[i][col].moveToy = 40+i*60
            self.board[i][col].moveTox = self.board[i][col].x
            self.board[i][col].move = True
 
    # count how many diamond had been eliminated on specific column
    def getColEmpty(self,col):
        count =0
        for i in xrange(len(self.board)):
            if(not self.isLegal(i,col)):
                count+=1
        return count
    
    #  find the bottom of specific column
    def findBottom(self,col):
        for i in xrange(len(self.board)-1,-1,-1):
            if(not self.isLegal(i,col)):
                return i
        return -1
    
    #  helper function for eliminate diamond. 
    def findEmptyUp(self,bottom,col):
        for i in xrange(bottom,-1,-1):
            if(self.isLegal(i,col)):
                return i
        return -1
    
    # after user's swap, update all diamonds to new position
    def updataItemPositionTwo(self,col):
        colEmpty=self.getColEmptyTwo(col)
        bottom = self.findBottomTwo(col)
        if bottom!=-1 and colEmpty!=0:
            while(colEmpty!=(bottom+1)):
                up = self.findEmptyUpTwo(bottom,col)
                if(up!=-1):
                    for i in xrange(up,-1,-1):
                        if(self.isLegaltwo(i,col)):
                            Color = self.boardtwo[i][col].color
                            (x,y)=(self.boardtwo[i][col].x,self.boardtwo[i][col].y)
                            (row,col)=((y-40)/60,(x-348)/60)
                            self.copyOneSquareTwo(Color,row,col,i+bottom-up,col)
                            self.boardtwo[i+bottom-up][col].move=True
                        else:
                            self.boardtwo[i+bottom-up][col]="empty"
                    for i in xrange(bottom-up):
                        self.boardtwo[i][col]="empty"
                colEmpty=self.getColEmptyTwo(col)
                bottom = self.findBottomTwo(col)
    
    #  generate a diamond when user have eliminated after a swap
    #  this function is called by runAdventureMode 
    def generateDiamondTwo(self,col):
        colEmpty=self.getColEmptyTwo(col)
        for i in xrange(colEmpty):
            if(self.easy==True):
                choice = random.choice(["yellow","red","orange","blue"])
            elif(self.hard==True):
                choice = random.choice(["yellow","red","orange","blue",\
                    "rose","white"])
            dist=i-colEmpty
            if(choice =="yellow"):
                self.boardtwo[i][col]=Yellow(dist,col)
            elif(choice =="red"):
                self.boardtwo[i][col]=Red(dist,col)
            elif(choice =="orange"):
                self.boardtwo[i][col]=Orange(dist,col)
            elif(choice =="blue"):
                self.boardtwo[i][col]=Blue(dist,col)
            elif(choice =="rose"):
                self.boardtwo[i][col]=Rose(dist,col)
            elif(choice =="white"):
                self.boardtwo[i][col]=White(dist,col)
            self.boardtwo[i][col].moveToy = 40+i*60
            self.boardtwo[i][col].moveTox = self.boardtwo[i][col].x
            self.boardtwo[i][col].move = True
   
    #  get how many empty position at adventure mode 
    def getColEmptyTwo(self,col):
        count =0
        for i in xrange(len(self.boardtwo)):
            if(self.boardtwo[i][col]=='empty'):
                count+=1
        return count
    
    #  find the bottom of a diamond which is empty
    # helper function for Adventure mode 
    def findBottomTwo(self,col):
        for i in xrange(len(self.boardtwo)-1,-1,-1):
            if(self.boardtwo[i][col]==self.emptyColor):
                return i
        return -1
    
    # find position of the first non-empty diamond begin on input "bottom "
    def findEmptyUpTwo(self,bottom,col):
        for i in xrange(bottom,-1,-1):
            if(self.isLegaltwo(i,col)):
                return i
        return -1
    
    # copy one square to another and copy all of its property
    # helper function for time mode 
    def copyOneSquare(self,choice,frmrow,frmcol,torow,tocol):
        if(choice =="yellow"):
            self.board[torow][tocol]=Yellow(frmrow,frmcol)        
        elif(choice =="red"):
            self.board[torow][tocol]=Red(frmrow,frmcol)
        elif(choice =="orange"):
            self.board[torow][tocol]=Orange(frmrow,frmcol)
        elif(choice =="blue"):
            self.board[torow][tocol]=Blue(frmrow,frmcol)
        elif(choice =="rose"):
            self.board[torow][tocol]=Rose(frmrow,frmcol)
        elif(choice =="white"):
            self.board[torow][tocol]=White(frmrow,frmcol)
        self.board[torow][tocol].row = torow
        self.board[torow][tocol].col = tocol         
        self.board[torow][tocol].moveTox=self.board[torow][tocol].x
        self.board[torow][tocol].moveToy=torow*self.board[torow][tocol].grid+\
            self.board[torow][tocol].upMargin
        if(self.isLegal(frmrow,frmcol)):
            self.board[torow][tocol].isOneColorMerge = \
                self.board[frmrow][frmcol].isOneColorMerge
            self.board[torow][tocol].isBoom = \
                self.board[frmrow][frmcol].isBoom
            self.board[torow][tocol].isRowColMerge = \
                self.board[frmrow][frmcol].isRowColMerge
    
    # copy one square to another and copy all of its property
    # helper function for adventure mode 
    def copyOneSquareTwo(self,choice,frmrow,frmcol,torow,tocol):
        if(choice =="yellow"):
            self.boardtwo[torow][tocol]=Yellow(frmrow,frmcol)        
        elif(choice =="red"):
            self.boardtwo[torow][tocol]=Red(frmrow,frmcol)
        elif(choice =="orange"):
            self.boardtwo[torow][tocol]=Orange(frmrow,frmcol)
        elif(choice =="blue"):
            self.boardtwo[torow][tocol]=Blue(frmrow,frmcol)
        elif(choice =="rose"):
            self.boardtwo[torow][tocol]=Rose(frmrow,frmcol)
        elif(choice =="white"):
            self.boardtwo[torow][tocol]=White(frmrow,frmcol)
        elif(choice == "soil"):
            self.boardtwo[torow][tocol]=Soil(frmrow,frmcol)
        elif(choice == "gold"):
            self.boardtwo[torow][tocol]=Gold(frmrow,frmcol)
        self.boardtwo[torow][tocol].row = torow
        self.boardtwo[torow][tocol].col = tocol         
        self.boardtwo[torow][tocol].moveTox=self.boardtwo[torow][tocol].x
        self.boardtwo[torow][tocol].moveToy=torow*self.boardtwo[torow][tocol].grid+\
            self.boardtwo[torow][tocol].upMargin
        if(self.isLegaltwo(frmrow,frmcol)):
            self.boardtwo[torow][tocol].isOneColorMerge = \
                self.boardtwo[frmrow][frmcol].isOneColorMerge
            self.boardtwo[torow][tocol].isBoom = \
                self.boardtwo[frmrow][frmcol].isBoom
            self.boardtwo[torow][tocol].isRowColMerge = \
                self.boardtwo[frmrow][frmcol].isRowColMerge
    
    # after eliminate all item, update position of each diamond to new position
    def updataItemPosition(self,col):
        colEmpty=self.getColEmpty(col)
        bottom = self.findBottom(col)
        if bottom!=-1 and colEmpty!=0:
            while(colEmpty!=(bottom+1)):
                up = self.findEmptyUp(bottom,col)
                if(up!=-1):
                    for i in xrange(up,-1,-1):
                        if(self.isLegal(i,col)):
                            Color = self.board[i][col].color
                            (x,y)=(self.board[i][col].x,self.board[i][col].y)
                            (row,col)=((y-40)/60,(x-348)/60)
                            self.copyOneSquare(Color,row,col,i+bottom-up,col)
                            self.board[i+bottom-up][col].move=True
                        else:
                            self.board[i+bottom-up][col]="empty"
                    for i in xrange(bottom-up):
                        self.board[i][col]="empty"
                colEmpty=self.getColEmpty(col)
                bottom = self.findBottom(col)

    #  test whether this positon is empty or a diamond 
    def isLegal(self,x,y):
        if(self.board[x][y]!="empty"):
            return True
        else:
            return False

    #  test whether this positon is "empty ", "soil","gold" or a diamond  
    def isLegaltwo(self,x,y):
        if(self.boardtwo[x][y]=="empty" or self.boardtwo[x][y].color=="soil" or\
            self.boardtwo[x][y].color=="gold"):
            return False
        else:
            return True
    
    # draw function for begin screen 
    def drawBeginScreen(self,canvas):
        if(self.isGameStart==False):
            if(self.isBeginScreen == True):
                canvas.create_image(0,0,anchor=NW,image=self.beginScreen)
            if(self.drawPlay == True):
                canvas.create_image(400,250,anchor=NW,image=self.beginScreenPlay)
            if(self.drawOption == True):
                canvas.create_image(50,280,anchor=NW,\
                    image=self.beginScreenOption)
            if(self.drawRecord == True):
                canvas.create_image(750,280, anchor=NW, \
                    image=self.beginScreenRecord)
            if(self.drawQuit == True):
                canvas.create_image(870,640,anchor=NW,image=self.beginScreenQuit)
            if(self.drawHelp == True):
                canvas.create_image(7,640,anchor=NW,image=self.beginScreenHelp)
    
    # draw function for adventuer mode background 
    def drawAdventureModeBackground(self,canvas):
        if(self.isGameStart==True):
            if(self.isAdventureMode==True):            
                canvas.create_image(0,0,anchor=NW,image=\
                    self.AdventureModeBackground)
                if(self.isAdventureAuto==True):
                    textcolor = "red"
                else:
                    textcolor = "yellow"
                canvas.create_text(112,458,text="Auto",anchor="nw",
                        font = "Arial 50 bold",fill = textcolor)
                if(self.changeBackColorAdventure==True):
                    backcolor = "yellow"
                else:
                    backcolor="red"
                canvas.create_text(112,540,text="Back",anchor="nw",
                    font ="Arial 50 bold",fill = backcolor)
    
    # draw function for adventure mode column and the layer count on column 
    def drawAdventureColumn(self,canvas):
        if(self.isGameStart==True):
            if(self.isAdventureMode==True):
                canvas.create_image(0,0,anchor=NW,image=self.column)
                layer = str(self.layercount/1000)+str((self.layercount/100)%10)+\
                        str(self.layercount%10)
                canvas.create_text(350,558,text=layer,\
                    anchor="se",font="Arial 35 bold",fill='black')
                canvas.create_text(887,558,text=layer,\
                    anchor="se",font="Arial 35 bold",fill='black')
    
    # draw function for time mode background 
    def drawTimeModeBackground(self,canvas):
        if(self.isGameStart==True):
            if(self.isTimeMode== True):
                canvas.create_image(0,0,anchor=NW,image=self.TimeModeBackground)
                self.drawScore(canvas)
                time = self.time
                red = 255-255.0/self.defaulttime*time
                green = 255.0/self.defaulttime*time
                width = 563.0/self.defaulttime*time
                color = self.boardtwo[0][0].rgb(int(red),int(green),0)
                canvas.create_rectangle(365,640,int(width+365),666,fill=color)
                if(self.isTimeAuto==False):
                    textcolor = "yellow"
                else:
                    textcolor = "red"
                canvas.create_text(70,490,text="Auto",anchor="nw",
                                    font = "Arial 50 bold", fill =textcolor)
                if(self.changeBackColorTime==False):
                    backcolor = "yellow"
                else:
                    backcolor = "red"
                canvas.create_text(75,570,text="Back",anchor="nw",
                                    font = "Arial 40 bold",fill=backcolor)
    
    # draw function for mode selection, change button size when mouse move on it
    def drawModeSelectionBackground(self,canvas):
        if(self.isGameStart==True):
            if(self.modeselect == True):
                canvas.create_image(0,0,anchor=NW,
                    image=self.modeSelecBackground)
            if(self.drawTime==True):
                canvas.create_image(210,150,anchor=NW,
                    image=self.modeSelectTime)
            if(self.drawAdventure==True):
                canvas.create_image(625,150,anchor=NW,
                    image=self.modeSelectAdventure)
    
    # drawscore function 
    def drawScore(self,canvas):
        canvas.create_text(190,350,text="Score: "+str(self.score),anchor="ne",
                           font="Arial 20 bold",fill='yellow')
        canvas.create_text(190,140,text="Time:  "+str(self.time/10),anchor="ne",
                           font="Arial 25 bold",fill='yellow')
    
    #  draw function for option mode, "easy" or "hard"
    def drawOptionMode(self,canvas):
        if(self.isOptionMode == True):
            canvas.create_image(0,0,anchor=NW,image=self.beginScreen)
            coloryellow = "#%02x%02x%02x" % (245,205,56)
            colorpurple = "#%02x%02x%02x" % (115,63,141)
            canvas.create_rectangle(250,250,750,450,fill=coloryellow)
            canvas.create_rectangle(255,255,745,445,fill=colorpurple)
            if(self.easy ==True):
                canvas.create_image(300,320,anchor=NW,image=self.Yesbutton)
            else:
                canvas.create_image(300,320,anchor=NW,image=self.Nobutton)
            if(self.hard==True):
                canvas.create_image(550,320,anchor=NW,image=self.Yesbutton)
            else:
                canvas.create_image(550,320,anchor=NW,image=self.Nobutton)
            easycolor = coloryellow if self.easy==True else "black"
            canvas.create_text(430,320,text="Easy",font = "Arial 40 bold",\
                            anchor = "ne",fill=easycolor)
            hardcolor = coloryellow if self.hard==True else "black"
            canvas.create_text(680,320,text="Hard",font = "Arial 40 bold",\
                            anchor = "ne",fill=hardcolor)
            canvas.create_text(560,380,text="PLAY!",font="Arial 40 bold",\
                            anchor="ne", fill = "cyan")
    
    # draw the help and introduction window when user click it 
    def drawHelpMode(self,canvas):
        if(self.isHelpMode==True):
            canvas.create_image(0,0,anchor=NW,image=self.beginScreen)
            canvas.create_image(330,100,anchor=NW,image=self.introduction)
    
    # draw each jewels for time mode
    def drawTimeModeJewels(self,canvas):
        if(self.isTimeMode==True):
            for i in xrange(len(self.board)):
                for j in xrange(len(self.board[0])):
                    if (self.isLegal(i,j)):
                        self.board[i][j].draw(canvas)
        if(self.drawBoom!=None):
            (x,y)=(self.drawBoom[2]*60+348+30,self.drawBoom[1]*60+40+30)
            r=self.r
            canvas.create_oval(x-r,y-r,x+r,y+r,fill='yellow')
        if(self.drawRowCol!=None):
            r= (60-self.RowColGrid)/2
            (x1,y1)=(348,self.drawRowCol[1]*60+40)
            (x2,y2)=(348+self.drawRowCol[2]*60,40)
            canvas.create_rectangle(x1,y1+r,x1+600,y1+60-r,fill='white')
            canvas.create_rectangle(x2+r,y2,x2+60-r,y1+600,fill='white')
        if(self.drawHintTimeMode==True):
            if(self.isTimeAuto==False):
                for item in self.hinttime:
                    (row,col)=(item[0],item[1])
                    if(self.isLegal(row,col)):
                        if(self.time%3==0):
                            self.board[row][col].drawSpecial(canvas)
    
    # draw each diamond on adventure mode 
    # helper function for drawAdventureModeJewels
    def drawAdventureModeJewelsHelp(self,canvas):
        if(self.drawBoom!=None):
            (x,y)=(self.drawBoom[2]*60+348+30,self.drawBoom[1]*60+40+30)
            r=self.r
            canvas.create_oval(x-r,y-r,x+r,y+r,fill='yellow')
        if(self.drawRowCol!=None):
            r= (60-self.RowColGrid)/2
            (x1,y1)=(348,self.drawRowCol[1]*60+40)
            (x2,y2)=(348+self.drawRowCol[2]*60,40)
            canvas.create_rectangle(x1,y1+r,x1+600,y1+60-r,fill='white')
            canvas.create_rectangle(x2+r,y2,x2+60-r,y1+600,fill='white')
        if(self.drawHintAdventureMode==True):
            if(self.isAdventureAuto==False):
                if(self.hintadventure!=None):
                    for item in self.hintadventure:
                        (row,col)=(item[0],item[1])
                        if(self.isLegaltwo(row,col)):
                            if(self.time%3==0):
                                self.boardtwo[row][col].drawSpecial(canvas)
    
    # draw diamond when user is playing adventure mode 
    def drawAdventureModeJewels(self,canvas):
        if(self.isAdventureMode == True):
            for i in xrange(len(self.boardtwo)):
                for j in xrange(len(self.boardtwo[0])):
                    if(self.boardtwo[i][j]!='empty'):
                        self.boardtwo[i][j].draw(canvas)
            time = self.time
            red = 255-255.0/self.defaulttime*time
            green = 255.0/self.defaulttime*time
            width = 514.0/self.defaulttime*time
            color = "#%02x%02x%02x" % (red,green,0)
            canvas.create_rectangle(330,642,int(width+332),678,fill=color)
            canvas.create_text(165,185,text="Score ",anchor="se",
                           font="Arial 20 bold",fill='yellow')
            canvas.create_text(235,190,text=str(self.score),anchor="se",
                           font="Arial 30 bold",fill='yellow')
            canvas.create_text(160,330,text=str(self.goldscore),anchor="nw",
                           font="Arial 30 bold",fill='yellow')
            self.drawAdventureModeJewelsHelp(canvas)
    
    # draw score board when user click "record" button on begin interface
    def drawScoreBoard(self,canvas):
        if(self.isScoreBoard==True):
            canvas.create_image(0,0,anchor=NW,image=self.ScoreBoardBackground)
            y=300
            for item in self.recordTimeMode:
                y+=80
                text = str(item)
                canvas.create_text(150,y,text=text,anchor="nw",\
                    font ="Arial 60 bold",fill="black")
            y=300
            for item in self.recordAdventureMode:
                y+=80
                text=str(item)
                canvas.create_text(620,y,text=text,anchor="nw",\
                    font ="Arial 60 bold",fill="black")
 
    #  helper function for Time Mode mouse
    def TimeModeMouseHelp(self):
        if(self.mouseX>50 and self.mouseX<200 and
            self.mouseY>500 and self.mouseY<535):
            self.isTimeAuto=True if (self.isTimeAuto==False) else False
        if(self.mouseX>80 and self.mouseX<170 and 
            self.mouseY>580 and self.mouseY<615):
            (self.modeselect, self.isTimeMode)= (True,False)
            self.mergecount = None
            (self.score, self.hintTimecount)= (0,self.defaultTime)
            self.clearDrawRecord()
            self.initJewels()
            (self.time,self.isTimeAuto) = (self.defaulttime,False)
        if self.mouseX >=348 and self.mouseX<=948:
            if(self.mouseY>=40 and self.mouseY<=640):
                (col,row) = ((self.mouseX -348)/60,(self.mouseY -40)/60)
                self.firstpress = ["frm",row,col]
        if self.mouseReleaseX >=348 and self.mouseReleaseX<=948:
            if(self.mouseReleaseY>=40 and self.mouseReleaseY<=640):
                (col,row) = ((self.mouseReleaseX - 348)/60,(self.mouseReleaseY -40)/60)
                self.secondpress = ["to",row,col]
        self.clearMouseRecord()
    

    #  time mode mouse function, tansfer coordinate into 
    #  corresponding singal
    def TimeModeMouse(self):
        if self.isGameStart==True:
            if(self.isTimeMode==True):
                if(self.mouseMoveX>80 and self.mouseMoveX<170 and 
                        self.mouseMoveY>580 and self.mouseMoveY<615):
                    self.changeBackColorTime=True
                else:
                    self.changeBackColorTime=False
                if(self.mouseX!=None and self.mouseY!=None and \
                    self.mouseReleaseX!=None and self.mouseReleaseY!=None):
                    self.TimeModeMouseHelp()
    
    #  helper function for adventure mode mouse click
    def AdventureModeMouseHelp(self):
        if(self.mouseX>110 and self.mouseX<220 and 
            self.mouseY>550 and self.mouseY<600):
            (self.modeselect,self.isAdventureMode)= (True,False)
            self.time=self.defaulttime
            self.initAdventure()
            self.clearPressRecord()
            (self.score,self.layercount,self.hintTimecount)= (0,0,self.defaultTime)
            self.isAdventureAuto=False
        if(self.mouseX>120 and self.mouseX<210 and 
            self.mouseY > 470 and self.mouseY<500):
            self.isAdventureAuto = True if(self.isAdventureAuto==False) else False
        if (self.mouseX >=348 and self.mouseX<=828):
            if(self.mouseY>=40 and self.mouseY<=640):
                (col,row) = ((self.mouseX -348)/60,(self.mouseY -40)/60)
                self.firstpress = ["frm",row,col]
        if (self.mouseReleaseX >=348 and self.mouseReleaseX<=828):
            if(self.mouseReleaseY>=40 and self.mouseReleaseY<=640):
                (col,row) = ((self.mouseReleaseX- 348)/60,(self.mouseReleaseY-40)/60)
                self.secondpress = ["to",row,col]
        self.clearMouseRecord()
    
    #  adventure mode mouse function, tansfer coordinate into 
    #  corresponding signal
    def AdventureModeMouse(self):
        if(self.isGameStart==True):
            if(self.isAdventureMode==True):
                if(self.mouseMoveX>120 and self.mouseMoveX<225 and 
                        self.mouseMoveY>550 and self.mouseMoveY<590):
                    self.changeBackColorAdventure=True
                else:
                    self.changeBackColorAdventure=False
                if(self.mouseX!=None and self.mouseY!=None and \
                    self.mouseReleaseX!=None and self.mouseReleaseY!=None):
                    self.AdventureModeMouseHelp()
    
    #  clear the mouse press and mouse release record
    def clearMouseRecord(self):
        (self.mouseX ,self.mouseY) = (None,None)
        (self.mouseReleaseX ,self.mouseReleaseY) = (None,None)
    
    #  test whether animation of diamond is over for time mode 
    def isMoveOver(self):
        move = False
        for i in xrange(len(self.board)):
            for j in xrange(len(self.board[0])):
                if(self.isLegal(i,j)):
                    if(self.board[i][j].move==True):
                        move = True
        return move
    
    # test whether animation of diamond is over for adventure mode 
    def isMoveOverTwo(self):
        move = False
        for i in xrange(len(self.boardtwo)):
            for j in xrange(len(self.boardtwo[0])):
                if(self.isLegaltwo(i,j)):
                    if(self.boardtwo[i][j].move==True):
                        move = True
        return move
    
    #  save coordiante to variable and reset the hint time to 100
    def onMouse(self, event):
        (self.mouseX,self.mouseY)=(event.x,event.y)
        self.hintTimecount=self.defaultTime
        self.drawHintTimeMode=False
        self.hinttime=None
        self.hintadventure=None
        self.drawHintAdventureMode=False
    
    # mouse release function. reset variable 
    def onMouseRelease(self,event):
        (self.mouseReleaseX,self.mouseReleaseY)=(event.x,event.y)
        self.hintTimecount=self.defaultTime
        self.drawHintTimeMode=False
        self.hinttime=None
        self.hintadventure=None
        self.drawHintAdventureMode=False
    
    #  begin interface interface. when user move mouse to different, 
    #  button will enlarge
    def BeginScreenMouse(self):
        if(self.isBeginScreen==True):
            if(self.mouseMoveX>420 and self.mouseMoveX<580 and 
                self.mouseMoveY>280 and self.mouseMoveY<420):
                self.drawPlay = True
            else:
                self.drawPlay = False
            if(self.mouseMoveX>90 and self.mouseMoveX<190 and 
                self.mouseMoveY>340 and self.mouseMoveY<430):
                self.drawOption = True
            else:
                self.drawOption= False
            if(self.mouseMoveX>800 and self.mouseMoveX<900 and 
                self.mouseMoveY>340 and self.mouseMoveY<430):
                self.drawRecord = True
            else:
                self.drawRecord= False
            if(self.mouseMoveX>17 and self.mouseMoveX<95 and 
                self.mouseMoveY>655 and self.mouseMoveY<678):
                self.drawHelp=True
            else:
                self.drawHelp=False
            if(self.mouseMoveX>890 and self.mouseMoveX<935 and 
                self.mouseMoveY>645 and self.mouseMoveY<675):
                self.drawQuit=True
            else:
                self.drawQuit=False
    
    #  transfer mouse coordiante to class variable
    def onMouseMove(self,event):
        (self.mouseMoveX,self.mouseMoveY)=(event.x, event.y)
        self.BeginScreenMouse()
    
    # brgin interface run function 
    def runBeginScreen(self):
        if(self.isBeginScreen == True):
            if(self.mouseX>890 and self.mouseX<1000 and \
                self.mouseY>650 and self.mouseY<690):
                os._exit(0)
            if(self.mouseX>410 and self.mouseX<580 and 
                    self.mouseY>270 and self.mouseY<430):
                self.isGameStart = True
                self.isBeginScreen = False
                self.modeselect=True
                (self.mouseX,self.mouseY)=(None,None)
            if(self.mouseX>800 and self.mouseX<900 and
                self.mouseY>336 and self.mouseY<436):
                (self.isBeginScreen,self.isScoreBoard)= (False,True)
                self.isGameStart = True
                (self.mouseX,self.mouseY)=(None,None)
            if(self.mouseX>90 and self.mouseX<190 and \
                self.mouseY>340 and self.mouseY<440):
                (self.isBeginScreen,self.isOptionMode) = (False,True)
                self.isGameStart = True
                (self.mouseX,self.mouseY)=(None,None)
            if(self.mouseX>17 and self.mouseX<95 and \
                self.mouseY>655 and self.mouseY<678):
                (self.isBeginScreen,self.isHelpMode)=(False,True)
                self.isGameStart = True
    
    # mode selection funtion 
    # magic number is specific coordiante on mode select screen 
    def runModeSelect(self):
        if(self.modeselect==True):
            if(self.mouseX>240 and self.mouseX<380 and 
                self.mouseY>170 and self.mouseY<320):
                self.isTimeMode = True
                self.modeselect = False
            if(self.mouseX>68 and self.mouseX<155 and 
                self.mouseY>70 and self.mouseY<100):
                self.isGameStart = False
                self.modeselect = False
                self.isBeginScreen = True
            if(self.mouseX>650 and self.mouseX<810 and 
                self.mouseY>170 and self.mouseY<320):
                self.modeselect = False
                self.isAdventureMode = True
            if(self.mouseMoveX>247 and self.mouseMoveX<382 and 
                self.mouseMoveY>175 and self.mouseMoveY<312):
                self.drawTime=True
            else:
                self.drawTime=False
            if(self.mouseMoveX> 655 and self.mouseMoveX<789 and 
                self.mouseMoveY>175 and self.mouseMoveY<312):
                self.drawAdventure=True
            else:
                self.drawAdventure=False
    
    #  help interface, show introduction for this game s
    def runHelp(self):
        if(self.isHelpMode==True):
            if(self.mouseX>450 and self.mouseX<574 and \
                self.mouseY>523 and self.mouseY<545):
                self.isBeginScreen = True
                self.isHelpMode = False
                self.isGameStart = False
                (self.mouseX,self.mouseY)=(None,None)
    
    # clear mouse press record 
    def clearPressRecord(self):
        self.firstpress=["waiting",None,None]
        self.secondpress=["waiting",None,None]
    
    #  copy one item to another position for time mode board 
    def generateItem(self,frmrow,frmcol,torow,tocol,choice,mergeproperty):
        if(choice =="yellow"):
            self.board[torow][tocol]=Yellow(frmrow,frmcol)
        elif(choice =="red"):
            self.board[torow][tocol]=Red(frmrow,frmcol)
        elif(choice =="orange"):
            self.board[torow][tocol]=Orange(frmrow,frmcol)
        elif(choice =="blue"):
            self.board[torow][tocol]=Blue(frmrow,frmcol)
        elif(choice =="rose"):
            self.board[torow][tocol]=Rose(frmrow,frmcol)
        elif(choice =="white"):
            self.board[torow][tocol]=White(frmrow,frmcol)
        self.board[torow][tocol].row = torow
        self.board[torow][tocol].col = tocol
        self.board[torow][tocol].moveTox = tocol*60+348
        self.board[torow][tocol].moveToy = torow*60+40
        self.board[torow][tocol].move = True
        if(self.isLegal(frmrow,frmcol)):
            self.board[torow][tocol].isOneColorMerge = mergeproperty[0]
            self.board[torow][tocol].isBoom = mergeproperty[1]
            self.board[torow][tocol].isRowColMerge = mergeproperty[2]
    
    #  copy one item to another position for adventure mode board 
    def generateItemTwo(self,frmrow,frmcol,torow,tocol,choice):
        if(choice =="yellow"):
            self.boardtwo[torow][tocol]=Yellow(frmrow,frmcol)
        elif(choice =="red"):
            self.boardtwo[torow][tocol]=Red(frmrow,frmcol)
        elif(choice =="orange"):
            self.boardtwo[torow][tocol]=Orange(frmrow,frmcol)
        elif(choice =="blue"):
            self.boardtwo[torow][tocol]=Blue(frmrow,frmcol)
        elif(choice =="rose"):
            self.boardtwo[torow][tocol]=Rose(frmrow,frmcol)
        elif(choice =="white"):
            self.boardtwo[torow][tocol]=White(frmrow,frmcol)
        self.boardtwo[torow][tocol].row = torow
        self.boardtwo[torow][tocol].col = tocol
        self.boardtwo[torow][tocol].moveTox = tocol*60+348
        self.boardtwo[torow][tocol].moveToy = torow*60+40
        self.boardtwo[torow][tocol].move = True
    
    #  exchange two items for time mode 
    def exchangeTwoItem(self):
        (frmrow,frmcol)=(self.firstpress[1],self.firstpress[2])
        (torow,tocol) = (self.secondpress[1],self.secondpress[2])
        if(not (frmrow == torow and frmcol == tocol)):
            if(frmrow == torow or frmcol == tocol):
                if(abs(frmrow-torow)>1):
                    if(torow>frmrow):
                        torow = frmrow+1
                    else:
                        torow = frmrow-1
                if(abs(frmcol-tocol)>1):
                    if(tocol>frmcol):
                        tocol = frmcol+1
                    else:
                        tocol = frmcol-1
            frmcolor = self.board[frmrow][frmcol].color
            tocolor = self.board[torow][tocol].color
            frm=[self.board[frmrow][frmcol].isOneColorMerge,\
                 self.board[frmrow][frmcol].isBoom,\
                self.board[frmrow][frmcol].isRowColMerge]
            to=[self.board[torow][tocol].isOneColorMerge,\
                 self.board[torow][tocol].isBoom,\
                self.board[torow][tocol].isRowColMerge]
            self.generateItem(frmrow,frmcol,torow,tocol,frmcolor,frm)
            self.generateItem(torow,tocol,frmrow,frmcol,tocolor,to)
    
    #  exchange two items for adventure  mode 
    def exchangeTwoItemTwo(self):
        (frmrow,frmcol)=(self.firstpress[1],self.firstpress[2])
        (torow,tocol) = (self.secondpress[1],self.secondpress[2])
        if(not (frmrow == torow and frmcol == tocol)):
            if(self.isLegaltwo(frmrow,frmcol) and self.isLegaltwo(torow,tocol)):
                frmcolor = self.boardtwo[frmrow][frmcol].color
                tocolor = self.boardtwo[torow][tocol].color
                self.generateItemTwo(frmrow,frmcol,torow,tocol,frmcolor)
                self.generateItemTwo(torow,tocol,frmrow,frmcol,tocolor)

    # process the mouse press data and transfer it to specific row and col 
    def filterPressRecode(self):
        (frmrow,frmcol)=(self.firstpress[1],self.firstpress[2])
        (torow,tocol) = (self.secondpress[1],self.secondpress[2])
        if(not (frmrow == torow and frmcol == tocol)):
            if(frmrow == torow or frmcol == tocol):
                if(abs(frmrow-torow)>1):
                    if(torow>frmrow):
                        torow = frmrow+1
                    else:
                        torow = frmrow-1
                if(abs(frmcol-tocol)>1):
                    if(tocol>frmcol):
                        tocol = frmcol+1
                    else:
                        tocol = frmcol-1
                (self.firstpress[0],self.firstpress[1],self.firstpress[2])=\
                      ("frm",frmrow,frmcol)
                (self.secondpress[0],self.secondpress[1],self.secondpress[2])=\
                      ("to",torow,tocol)
            else:
                self.clearPressRecord()
    
    # if swap eliminate no diamond , recover the swap 
    def recoverExchange(self):
        tmp=["waitint",None,None]
        tmp[0]=self.firstpress[0]
        tmp[1]=self.firstpress[1]
        tmp[2]=self.firstpress[2]
        self.firstpress[0]=self.secondpress[0]
        self.firstpress[1]=self.secondpress[1]
        self.firstpress[2]=self.secondpress[2]
        self.secondpress[0]=tmp[0]
        self.secondpress[1]=tmp[1]
        self.secondpress[2]=tmp[2]
    
    #  clear all diamonds with same color for time mode 
    def clearOneColor(self,color):
        for i in xrange(len(self.board)):
            for j in xrange(len(self.board[0])):
                if(self.isLegal(i,j) and self.board[i][j].color==color):
                    self.board[i][j]="empty"
                    self.score+=20
    
    #  clear all diamonds with same color for adventure mode 
    def clearOneColorTwo(self,color):
        for i in xrange(len(self.boardtwo)):
            for j in xrange(len(self.boardtwo[0])):
                if(self.isLegaltwo(i,j) and self.boardtwo[i][j].color==color):
                    self.boardtwo[i][j]="empty"
                    if(i<9):
                        if(self.boardtwo[i+1][j]!="empty"):
                            if(self.boardtwo[i+1][j].color=="soil"):
                                self.boardtwo[i+1][j]="empty"
                                self.score+=10
                            elif(self.boardtwo[i+1][j].color=="gold"):
                                self.goldscore+=10
                                self.boardtwo[i+1][j]="empty"
                                self.score+=20
                    self.score+=20
    
    # clear the diamond with boom bonus, clear 8 diamond around it in 
    # time mode 
    def clearBoom(self,row,col):
        if row == 0:
            availablerow =[row,row+1]
        elif row==self.rows-1:
            availablerow =[row-1,row]
        else:
            availablerow =[row-1,row,row+1]
        if col == 0:
            availablecol =[col,col+1]
        elif col== self.cols-1:
            availablecol =[col-1,col]
        else:
            availablecol =[col-1,col,col+1]
        self.board[row][col]='empty'
        for i in availablerow:
            for j in availablecol:
                 if(self.isLegal(i,j)):
                    if(i!=row or j!=col):
                        if(self.board[i][j].isOneColorMerge==False and \
                            self.board[i][j].isBoom==False and \
                            self.board[i][j].isRowColMerge==False):
                            self.board[i][j]="empty"
                        elif(self.board[i][j].isOneColorMerge==True):
                            self.clearOneColor(self.board[i][j].color)
                        elif(self.board[i][j].isBoom==True):
                            self.clearBoom(i,j)
                        elif(self.board[i][j].isRowColMerge==True):
                            self.clearRowCol(i,j)
        self.score+=(len(availablerow)*len(availablecol)*10)
    
    # clear the diamond with boom bonus, clear 8 diamond around it in 
    # adventure mode  
    def clearBoomTwo(self,row,col):
        if row == 0:
            availablerow =[row,row+1]
        elif row==self.rows-1:
            availablerow =[row-1,row]
        else:
            availablerow =[row-1,row,row+1]
        if col == 0:
            availablecol =[col,col+1]
        elif col== self.cols-3:
            availablecol =[col-1,col]
        else:
            availablecol =[col-1,col,col+1]
        self.boardtwo[row][col]='empty'
        for i in availablerow:
            for j in availablecol:
                 if(self.boardtwo[i][j]!="empty"):
                    if(i!=row or j!=col):
                        if(self.boardtwo[i][j].isOneColorMerge==False and \
                            self.boardtwo[i][j].isBoom==False and \
                            self.boardtwo[i][j].isRowColMerge==False):
                            self.boardtwo[i][j]="empty"
                        elif(self.boardtwo[i][j].isOneColorMerge==True):
                            self.clearOneColorTwo(self.board[i][j].color)
                        elif(self.boardtwo[i][j].isBoom==True):
                             self.clearBoomTwo(i,j)
                        elif(self.boardtwo[i][j].isRowColMerge==True):
                            self.clearRowColTwo(i,j)
                        if(self.boardtwo[i+1][j]!="empty"):
                            if(self.boardtwo[i+1][j].color == "soil"):
                                self.boardtwo[i+1][j]="empty"
                            elif(self.boardtwo[i+1][j].color=="gold"):
                                self.goldscore+=1
                                self.boardtwo[i+1][j]="empty"
    
    # clear all diamonds in a whole row and whole col for time mode 
    def clearRowCol(self,row,col):
        self.board[row][col]='empty'
        for i in xrange(self.cols):
            if(self.isLegal(row,i)):
                self.board[row][i]="empty"
        for j in xrange(self.rows):
            if(self.isLegal(j,col)):
                 self.board[j][col]="empty"
        self.score=self.score+self.rows*30
        self.score=self.score+self.cols*30
    
    # clear all diamonds in a whole row and whole col for adventure mode 
    def clearRowColTwo(self,row,col):
        self.boardtwo[row][col]='empty'
        for i in xrange(self.cols-2):
            if(self.boardtwo[row][i]!="empty"):
                self.boardtwo[row][i]="empty"
        for j in xrange(self.rows):
            if(self.boardtwo[j][col]!="empty"):
                 self.boardtwo[j][col]="empty"
        self.score=self.score+self.rows*30
        self.score=self.score+(self.cols-2)*30

    def getLongestLeft(self,row,col,color,mode):
        count =0
        if(mode=="TimeMode"):
            while(col>=0 and self.isLegal(row,col) and \
                self.board[row][col].color==color):
                count+=1
                col-=1
        else:
            while(col>=0 and self.isLegaltwo(row,col) and \
                self.boardtwo[row][col].color==color):
                count+=1
                col-=1
        return count

    def getLongestRight(self,row,col,color,mode):
        count=0
        if(mode=="TimeMode"):     
            while(col<10 and self.isLegal(row,col) and \
                 self.board[row][col].color == color):
                count+=1
                col+=1
        else:
            while(col<8 and self.isLegaltwo(row,col) and \
                 self.boardtwo[row][col].color == color):
                count+=1
                col+=1
        return count

    def getLongestUp(self,row,col,color,mode):
        count=0
        if(mode=="TimeMode"):
            while(row>=0 and self.isLegal(row,col) and \
                self.board[row][col].color == color):
                count+=1
                row-=1
        else:
            while(row>=0 and self.isLegal(row,col) and \
                self.boardtwo[row][col].color == color):
                count+=1
                row-=1
        return count
    

    def getLongestDown(self,row,col,color,mode):
        count=0
        if(mode=="TimeMode"):
            while(row<10 and self.isLegal(row,col) and \
                self.board[row][col].color == color):
                count+=1
                row+=1
        else:
            while(row<10 and self.isLegal(row,col) and \
                self.boardtwo[row][col].color == color):
                count+=1
                row+=1
        return count

    # helper function for hint in time mode 
    def hintTimeModeHelp(self,available,row,col,color,shuffle=True):
        for item in available:
            (subrow,subcol,count)=(item[0],item[1],0)
            if(subrow==row-1):
                leftright = self.getLongestLeft(subrow,subcol-1,color,"TimeMode")+\
                    self.getLongestRight(subrow,subcol+1,color,"TimeMode")
                updown = self.getLongestUp(subrow-1,subcol,color,"TimeMode")
            elif(subrow==row+1):
                leftright = self.getLongestLeft(subrow,subcol-1,color,"TimeMode")+\
                    self.getLongestRight(subrow,subcol+1,color,"TimeMode")
                updown = self.getLongestDown(subrow+1,subcol,color,"TimeMode")
            if(subcol==col-1):
                leftright = self.getLongestLeft(subrow,subcol-1,color,"TimeMode")
                updown = self.getLongestUp(subrow-1,subcol,color,"TimeMode")+\
                        self.getLongestDown(subrow+1,subcol,color,"TimeMode")
            elif(subcol==col+1):
                leftright = self.getLongestRight(subrow,subcol+1,color,"TimeMode")
                updown = self.getLongestUp(subrow-1,subcol,color,"TimeMode")+\
                        self.getLongestDown(subrow+1,subcol,color,"TimeMode")
            if(leftright>=2): (count,shuffle)=(count+leftright,False)             
            if(updown>=2):  (count,shuffle)=(count+updown,False)               
            if(self.hinttime==None and count!=0):
                self.hinttime=[[subrow,subcol,count],[row,col,count]]
            elif(self.hinttime!=None and count>self.hinttime[0][2]):
                self.hinttime=[[subrow,subcol,count],[row,col,count]]
            if(self.board[row][col].isRowColMerge==True):
                self.hinttime=[[row,col,10],[row,col,10]]
        return shuffle

    def hintTimeMode(self):
        shuffle = True
        for row in xrange(1,len(self.board)-1):
            for col in xrange(1,len(self.board[0])-1):
                available=[(row-1,col),(row,col-1),(row,col+1),(row+1,col)]
                if(self.isLegal(row,col)):
                    color =self.board[row][col].color
                    newshuffle = self.hintTimeModeHelp(available,row,col,color)
                    if(shuffle==True and newshuffle == False):
                        shuffle=False
        return shuffle

    # helper function for adventure mode 
    def hintAdventureModeHelp(self,available,row,col,color,shuffle=True):
        for item in available:
            (subrow,subcol,count)=(item[0],item[1],0)
            if(subrow==row-1):
                leftright = self.getLongestLeft(subrow,subcol-1,color,"AdventureMode")+\
                    self.getLongestRight(subrow,subcol+1,color,"AdventureMode")
                updown = self.getLongestUp(subrow-1,subcol,color,"AdventureMode")
            elif(subrow==row+1):
                leftright = self.getLongestLeft(subrow,subcol-1,color,"AdventureMode")+\
                    self.getLongestRight(subrow,subcol+1,color,"AdventureMode")
                updown = self.getLongestDown(subrow+1,subcol,color,"AdventureMode")
            if(subcol==col-1):
                leftright = self.getLongestLeft(subrow,subcol-1,color,"AdventureMode")
                updown = self.getLongestUp(subrow-1,subcol,color,"AdventureMode")+\
                        self.getLongestDown(subrow+1,subcol,color,"AdventureMode")
            elif(subcol==col+1):
                leftright = self.getLongestRight(subrow,subcol+1,color,"AdventureMode")
                updown = self.getLongestUp(subrow-1,subcol,color,"AdventureMode")+\
                        self.getLongestDown(subrow+1,subcol,color,"AdventureMode")
            if(leftright>=2): (count,shuffle)=(count+leftright,False)               
            if(updown>=2):  (count,shuffle)=(count+updown,False)              
            if(self.hintadventure==None and count!=0):
                self.hintadventure=[[subrow,subcol,count],[row,col,count]]
            elif(self.hintadventure!=None and count>self.hintadventure[0][2]):
                self.hintadventure=[[subrow,subcol,count],[row,col,count]]
            if(self.boardtwo[row][col].isRowColMerge== True):
                self.hintadventure=[[row,col,count],[row,col,count]]
        return shuffle


    def hintAdventureMode(self):
        shuffle= True
        for row in xrange(1,len(self.boardtwo)-1):
            for col in xrange(1,len(self.boardtwo[0])-1):
                available = [(row-1,col),(row+1,col),(row,col-1),(row,col+1)]
                if(self.isLegaltwo(row,col)):
                    color = self.boardtwo[row][col].color
                    newshuffle=self.hintAdventureModeHelp(available,row,col,color)
                    if(shuffle==True and newshuffle == False):
                        shuffle=False
        return shuffle
    
    # if all soil and gold in row 6 and row 7 have been clear, move the board
    # up 
    def checkMoveUp(self):
        moveup = True
        for col in xrange(len(self.boardtwo[0])):
            for i in [6,7]:
                if(not self.isLegaltwo(i,col)):
                    moveup=False
        return moveup
    
    # mode up all items and generate new soil and gold 
    def moveUpItem(self):
        for row in xrange(2,len(self.boardtwo)):
            for col in xrange(len(self.boardtwo[0])):
                color = self.boardtwo[row][col].color
                (frmrow,frmcol,torow,tocol)=(row,col,row-2,col)
                self.copyOneSquareTwo(color,frmrow,frmcol,torow,tocol)
                self.boardtwo[torow][tocol].move=True
        for row in [8,9]:
            for col in xrange(len(self.boardtwo[0])):
                choice = random.choice(["soil","gold"])
                if(choice=="soil"):
                    self.boardtwo[row][col]=Soil(row+2,col)
                else:
                    self.boardtwo[row][col]=Gold(row+2,col)
                self.boardtwo[row][col].row = row
                self.boardtwo[row][col].col = col
                self.boardtwo[row][col].moveTox = self.boardtwo[row][col].x
                self.boardtwo[row][col].moveToy = 40+row*60
                self.boardtwo[row][col].move = True
    
    #  check whether time is up 
    def isAliveTimeMode(self):
        if(self.time>0):
            return True
        else:
            return False
    
    # clear draw function flage 
    def clearDrawRecord(self):
        self.drawColor=None
        self.drawBoom=None
        self.drawRowCol=None
    
    # helper function for time mode 
    def runTimeModeHelpOne(self):
        if(self.firstpress[0]!="waiting" and self.secondpress[0]!="waiting"and \
            self.hasExchange==None):
            self.filterPressRecode()
            self.hasExchange=True
            (frmrow,frmcol)=(self.firstpress[1],self.firstpress[2])
            (torow,tocol)=(self.secondpress[1],self.secondpress[2])
            if(frmrow!=None and frmcol!=None and torow!=None and tocol!=None and 
                self.isLegal(frmrow,frmcol) and self.isLegal(torow,tocol) and 
                (not(frmrow==torow and frmcol==tocol))):
                self.exchangeTwoItem()
            elif(frmrow==torow and frmcol==tocol and frmrow!=None and frmcol!=None):
                if(self.isLegal(frmrow,frmcol)):
                    if(self.board[frmrow][frmcol].isOneColorMerge==True):
                        color = self.board[frmrow][frmcol].color
                        self.clearOneColor(color)
                        self.drawColor= [True,color]
                    elif(self.board[frmrow][frmcol].isBoom==True):
                        self.clearBoom(frmrow,frmcol)
                        self.drawBoom= [True,frmrow,frmcol]
                    elif(self.board[frmrow][frmcol].isRowColMerge==True):
                        self.clearRowCol(frmrow,frmcol)
                        self.drawRowCol= [True,frmrow,frmcol]
        for i in xrange(len(self.board)):
            for j in xrange(len(self.board[0])):
                if (self.isLegal(i,j)):
                    self.board[i][j].moveItem()

    #  helper function for time mode 
    def runTimeModeHelpTwo(self):
        self.mergecount=False
        if(self.secondpress[1]!=None and self.secondpress[2]!=None and \
            self.firstpress[1]!=None and self.firstpress[2]!=None):
            self.mergeItem(self.secondpress[1],self.secondpress[2])
            self.mergeItem(self.firstpress[1],self.firstpress[2])
        for i in xrange(len(self.board)):
            for j in xrange(len(self.board[0])):
                if (self.isLegal(i,j)):
                    self.mergeItem(i,j)
        for j in xrange(len(self.board[0])):
            self.updataItemPosition(j)
        for j in xrange(len(self.board[0])):
            self.generateDiamond(j)
        self.hinttime=None
        shuffle = self.hintTimeMode()
        if(shuffle==True):
            self.initJewels()
        if(self.hintTimecount<0):
            self.drawHintTimeMode = True

    def runTimeMode(self):
        if(self.isTimeMode == True and self.isAliveTimeMode()):
            self.time -= 1
            self.hintTimecount -= 1
            self.TimeModeMouse()
            if(self.isTimeAuto==True):  self.timeAutoCount -=1               
            if(self.isTimeAuto==True and self.hinttime!=None and self.timeAutoCount == 0):
                (subrow1,subcol1)=(self.hinttime[0][0],self.hinttime[0][1])
                (subrow2,subcol2)=(self.hinttime[1][0],self.hinttime[1][1])
                self.firstpress=["frm",subrow1,subcol1]
                self.secondpress=["to",subrow2,subcol2]
            self.runTimeModeHelpOne()
            self.updateBoom()
            self.updateRowCol()
            self.updateOnecolor()
            move = self.isMoveOver()
            if(move == False):  self.runTimeModeHelpTwo()
            if(self.timeAutoCount==0):  self.timeAutoCount=30
            if(self.mergecount==False):
                if(self.hasExchange==True and move ==False):
                    self.recoverExchange()
                    self.exchangeTwoItem()
                    (self.mergecount,self.hasExchange)=(None,None)
                    self.clearPressRecord()
            elif(self.mergecount==True):# mergecount is true means merge some item 
                (self.mergecount,self.hasExchange)=(None,None)
                self.clearPressRecord()
        elif(self.isAliveTimeMode()==False):
            (self.isTimeMode, self.drawHintTimeMode)= (False,False)
            self.clearDrawRecord()
            self.clearPressRecord()
            self.updateScoreTimeMode("timemode")
            self.time=self.defaulttime
            (self.mergecount,self.score) = (None,0)
            (self.isTimeAuto,self.modeselect)=(False,True)

    # interface for score board 
    def runScoreBoard(self):
        if(self.isScoreBoard==True):
            if(self.mouseX!=None and self.mouseY!=None and \
                self.mouseReleaseX!=None and self.mouseReleaseY!=None):
                (x,y)=(self.mouseX,self.mouseY)
                if(x>38 and x<130 and y> 70 and y<105):
                    self.isScoreBoard = False
                    self.isBeginScreen = True
                    self.isGameStart = False

    def runAdventureModeHelpOne(self):
        if(self.firstpress[0]!="waiting" and self.secondpress[0]!="waiting" and\
         self.hasExchange==None):
            self.filterPressRecode()
            self.hasExchange=True
            (frmrow,frmcol)=(self.firstpress[1],self.firstpress[2])
            (torow,tocol)=(self.secondpress[1],self.secondpress[2])
            if(frmrow!=None and frmcol!=None and torow!=None and tocol!=None and 
                self.isLegaltwo(frmrow,frmcol) and self.isLegaltwo(torow,tocol) and 
                (not(frmrow==torow and frmcol==tocol))):
                self.exchangeTwoItemTwo()
            elif(frmrow==torow and frmcol==tocol and \
                frmrow!=None and frmcol!=None):
                if(self.isLegaltwo(frmrow,frmcol)):
                    if(self.boardtwo[frmrow][frmcol].isOneColorMerge==True):
                        color = self.boardtwo[frmrow][frmcol].color
                        self.clearOneColorTwo(color)
                        self.drawColor= [True,color]
                    elif(self.boardtwo[frmrow][frmcol].isBoom==True):
                        self.clearBoomTwo(frmrow,frmcol)
                        self.drawBoom= [True,frmrow,frmcol]
                    elif(self.boardtwo[frmrow][frmcol].isRowColMerge==True):
                        self.clearRowColTwo(frmrow,frmcol)
                        self.drawRowCol= [True,frmrow,frmcol]
        for i in xrange(len(self.boardtwo)):
            for j in xrange(len(self.boardtwo[0])):
                if (self.boardtwo[i][j]!="empty"):
                    self.boardtwo[i][j].moveItem()
    
    #  adventure mode helper function 
    def runAdventureModeHelpTwo(self):
        self.mergecount=False
        if(self.secondpress[1]!=None and self.secondpress[2]!=None and \
            self.firstpress[1]!=None and self.firstpress[2]!=None):
            self.mergeItemTwo(self.secondpress[1],self.secondpress[2])
            self.mergeItemTwo(self.firstpress[1],self.firstpress[2])
        for i in xrange(len(self.boardtwo)):
            for j in xrange(len(self.boardtwo[0])):
                if (self.isLegaltwo(i,j)):
                    self.mergeItemTwo(i,j)
        for j in xrange(len(self.boardtwo[0])):
            self.updataItemPositionTwo(j)
        for j in xrange(len(self.boardtwo[0])):
            self.generateDiamondTwo(j)
        moveUp = self.checkMoveUp()
        if moveUp==True:
            self.moveUpItem()
            self.layercount+=1
        self.hintadventure = None
        shuffle = self.hintAdventureMode()
        if(shuffle==True):  self.initAdventure()
        if(self.hintTimecount<0):  self.drawHintAdventureMode = True

    # advenure mode function 
    def runAdventureMode(self):
        if(self.isAdventureMode==True and self.isAliveTimeMode()):
            self.time-=1
            self.hintTimecount-=1
            self.AdventureModeMouse()
            if(self.isAdventureAuto==True):  self.timeAutoCount-=1
            if(self.isAdventureAuto == True and self.hintadventure!=None and \
                self.timeAutoCount==0):
                (subrow1,subcol1)=(self.hintadventure[0][0],self.hintadventure[0][1])
                (subrow2,subcol2)=(self.hintadventure[1][0],self.hintadventure[1][1])
                self.firstpress=["frm",subrow1,subcol1]
                self.secondpress=["to",subrow2,subcol2]
            self.runAdventureModeHelpOne()
            self.updateBoom()
            self.updateRowCol()
            self.updateOnecolor()
            move = self.isMoveOverTwo()
            if(move == False): self.runAdventureModeHelpTwo()
            if(self.timeAutoCount==0): self.timeAutoCount=30
            if(self.mergecount==False):
                if(self.hasExchange==True and move ==False):
                    self.recoverExchange()
                    self.exchangeTwoItemTwo()
                    (self.mergecount, self.hasExchange)=(None,None)
                    self.clearPressRecord()
            elif(self.mergecount==True):
                (self.mergecount,self.hasExchange)=(None,None)
                self.clearPressRecord()
        elif(self.isAliveTimeMode()==False):
            (self.isAdventureMode,self.time)= (False,self.defaulttime)
            self.clearDrawRecord()
            self.clearPressRecord()
            (self.drawHintAdventureMode,self.isAdventureAuto)=(False,False)
            self.updateScoreTimeMode("adventuremode")
            (self.mergecount,self.score) = (None,0)
            (self.modeselect,self.mergecount) = (True,None)
   
    def onStep(self):
        if(self.isGameStart == False):
            self.runBeginScreen()
        elif(self.modeselect==True):
            self.runModeSelect()
        elif(self.isOptionMode==True):
            self.runOptionMode()
        elif(self.isHelpMode==True):
            self.runHelp()
        elif(self.isTimeMode == True):
            self.runTimeMode()
        elif(self.isAdventureMode==True):
            self.runAdventureMode()
        elif(self.isScoreBoard == True):
            self.runScoreBoard()

    def onDraw(self,canvas):
        self.drawBeginScreen(canvas)
        self.drawModeSelectionBackground(canvas)
        self.drawTimeModeBackground(canvas)
        self.drawTimeModeJewels(canvas)
        self.drawAdventureModeBackground(canvas)
        self.drawAdventureModeJewels(canvas)
        self.drawAdventureColumn(canvas)
        self.drawScoreBoard(canvas)
        self.drawOptionMode(canvas)
        self.drawHelpMode(canvas)

JewelsGame(width=1000,height=700,timerDelay=50).run()




