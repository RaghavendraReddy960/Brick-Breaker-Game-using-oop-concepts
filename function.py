import sys
import termios
import tty
import signal
from datetime import datetime
from config import *
from colorama import *

def blitobject(scene, item, x, y):
    """ Blit given item over the scene where specified
    after deleting previous instance"""
    scenematrix = scene.returnmatrix()
    itemmatrix = item.returnmatrix()
    k = 0
    l = 0
    # deleting previous position
    for i in range(item.x, item.x + item.length):
        for j in range(item.y, item.y + item.width):
            scenematrix[i][j] = ' '
    # putting at new position
    for i in range(x, x + item.length):
        for j in range(y, y + item.width):
            scenematrix[i][j] = itemmatrix[i-x][j-y]
    scene.updatescene(scenematrix)

class Paddle:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.x = 0
        self.y = 0
        self.matrix = []
        p = Back.RED+' '+RESET
        q = Back.YELLOW+' '+RESET
        self.matrix = [[p, q, q, q, q,q,q, p],]

    def setPos(self, scene, x, y):
        ''' Take the item and blit it over the scene at position specified'''
        blitobject(scene, self, x, y)
        self.x = x
        self.y = y
        
    def moveleft(self, scene):
        if(self.y<=0):
            self.setPos(scene,self.x,0)
        else:
            self.setPos(scene,self.x,self.y-1)
    
    def moveright(self, scene):
        if(self.y>=scene.width-self.width):
            self.setPos(scene,self.x,scene.width-self.width)
        else:
            self.setPos(scene,self.x,self.y+1)
        
    def returnmatrix(self):
        ''' Return the obstacle as a matrix '''
        return self.matrix
        
class Ball():
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.x = 0
        self.y = 0
        self.xDir = 1
        self.yDir = 1
        self.matrix = []
        p = Back.WHITE+' '+RESET
        self.matrix = [[p],]

    def setPos(self, scene, x, y):
        ''' Take the item and blit it over the scene at position specified'''
        blitobject(scene, self, x, y)
        self.x = x
        self.y = y
        
    def moveleft(self, scene):
        if(self.y<=0):
            self.setPos(scene,self.x,0)
        else:
            self.setPos(scene,self.x,self.y-1)
    
    def moveright(self, scene):
        if(self.y>=scene.width-self.width):
            self.setPos(scene,self.x,scene.width-self.width)
        else:
            self.setPos(scene,self.x,self.y+1)
            
    def moveBox(self, scene,x,y ):
        self.setPos(scene,self.x+(self.xDir*self.x),self.y+(self.yDir*self.y))
        
    def returnmatrix(self):
        ''' Return the obstacle as a matrix '''
        return self.matrix

class Get:
    """Class to get input from user in real time"""

    def __call__(self):
        """ Defining the call for class objects """

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class AlarmException(Exception):
    """Handling alarm exception."""
    pass


def alarmHandler(signum, frame):
    """Handling timeouts."""
    raise AlarmException


def input_to(getch, timeout=0.15):
    """Taking input from user."""
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.setitimer(signal.ITIMER_REAL, timeout)
    try:
        text = getch()
        signal.alarm(0)
        return text
    except AlarmException:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        return None

class Scene:
    """ Making a matrix to represent the game scene """

    def __init__(self, length, width, fullwidth):
        """ Initial matrix """
        self.start = 0
        self.length = length
        self.width = width
        self.fullwidth = fullwidth
        self.max_y = 0
        self.score = 0
        self.now=datetime.now()
        self.scenematrix = []
        # scenematrix is a matrix to display all elements
        for x in range(0, fullwidth):
            self.scenematrix.append([])
            for y in range(0, fullwidth):
                self.scenematrix[x].append(' ')

    def displayScene(self,time):
        """ Print the screen to the terminal """
        sceneprint = ""
        sceneprint += colors['Yellow'] + " "*30 + "Brick Breaker\n" + RESET
        sceneprint += colors['Cyan']+"SCORE : " +\
            str("16") + " "*10+"LIVES:"+str("2") + " "*10 + \
            "TIME LEFT:" + str(int((time-self.now).total_seconds()))+ " "*10 + \
            "b\n"+RESET
        sceneprint += colors['Cyan'] + "ac\n" + RESET  
        for x in range(0, self.width):
                sceneprint += colors['White']+'X'
        sceneprint += "\n"+RESET    
        if self.start >= self.fullwidth - self.width:
            self.start = self.fullwidth - self.width
        for i in range(0, self.length):
            for j in range(self.start, self.start + self.width):
                sceneprint += str(self.scenematrix[i][j])
            sceneprint += '\n'
        for x in range(0, self.width):
                sceneprint += colors['Yellow']+'X'
        sceneprint += "\n"+RESET 
        for x in range(0, self.width):
                sceneprint += colors['Yellow']+'X'
        sceneprint += "\n"+RESET       
        return sceneprint

    # auxilary functions to return and update matrix
    def returnmatrix(self):
        return self.scenematrix

    def updatescene(self, updmatrix):
        self.scenematrix = updmatrix
        

        
def generatescene(scene):
    paddle = Paddle(1, 8)
    paddle.setPos(scene, groundx, 30)