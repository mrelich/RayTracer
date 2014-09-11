
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# This will be the virtual ice block and I wanted to have it as a class #
# so I can have methods to tell if the ray is still in the ice block.   #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

from visual import *
import sys

class cube:
    

    #----------------------------------------#
    # Constructor
    #----------------------------------------#
    def __init__(self,x,y,z,L,H,Rotation):

        print "Making cube: ", x,y,z,L,H,Rotation

        # Save generic characteristics
        self.xpos     = x
        self.ypos     = y 
        self.zpos     = z
        self.length   = L
        self.height   = H
        self.rotation = Rotation

        # Create the box
        self.box = box(pos=(self.xpos,self.ypos,self.zpos),
                       length=L,
                       height=H,
                       width=0,
                       color=(0,1.5,1),
                       axis=(L*cos(Rotation),L*sin(Rotation),0))   

    #----------------------------------------#
    # Get equation for sides (slope,y0)
    #----------------------------------------#                       
    def getTop(self):
        return (tan(self.rotation),self.ypos+self.height/2.,sys.float_info.max)
    def getBot(self):
        return (tan(self.rotation),self.ypos-self.height/2.,sys.float_info.max)
    def getRight(self):
        return (0, sys.float_info.max, self.xpos+self.length/2.)
    def getLeft(self):
        return (0, sys.float_info.max, self.xpos-self.length/2.)


    def getEquations(self):

        equations = []
        equations.append( self.getTop() )
        equations.append( self.getRight() )
        equations.append( self.getBot() )
        equations.append( self.getLeft() )
        return equations

    #----------------------------------------#
    # Get normal vector for each side
    #----------------------------------------#
    def getTopV(self):
        return (sin(self.rotation),cos(self.rotation))
    def getBotV(self):
        return (sin(self.rotation),-cos(self.rotation))
    def getRightV(self):
        return (cos(self.rotation),sin(self.rotation))
    def getLeftV(self):
        return (-cos(self.rotation), sin(self.rotation))

    def getNormal(self):
        
        norms = []
        norms.append( self.getTopV() )
        norms.append( self.getRightV() )
        norms.append( self.getBotV() )
        norms.append( self.getLeftV() )
        return norms

    #----------------------------------------#
    # Determine if point is inside square
    #----------------------------------------#
    def inCube(self, point):
        x = point[0]
        y = point[1]

        if x > self.xpos + self.length/2.: return False
        if x < self.xpos - self.length/2.: return False        
        if y > self.ypos + self.height/2.: return False        
        if y < self.ypos - self.height/2.: return False

        return True
    
    
        
