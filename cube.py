
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# This will be the virtual ice block and I wanted to have it as a class #
# so I can have methods to tell if the ray is still in the ice block.   #
# TODO: Need to fix the getTop, etc and also inCube methods. They are 
# broken when you perform rotations.
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
    # Define method for rotation
    #----------------------------------------#
    def rotateCoords(self,x,y):
        newx = x*cos(self.rotation) - y*sin(self.rotation)
        newy = x*sin(self.rotation) + y*cos(self.rotation)
        return newx, newy

    #----------------------------------------#    
    # Setup the equations
    #----------------------------------------#
    def getTop(self):   return (self.getSlope(0), self.getY0(0), self.getX0(0))
    def getRight(self): return (self.getSlope(1), self.getY0(1), self.getX0(1))
    def getBot(self):   return (self.getSlope(2), self.getY0(2), self.getX0(2))
    def getLeft(self):  return (self.getSlope(3), self.getY0(3), self.getX0(3))

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
        return (-sin(self.rotation),cos(self.rotation))
    def getBotV(self):
        return (sin(self.rotation),-cos(self.rotation))
    def getRightV(self):
        return (cos(self.rotation),sin(self.rotation))
    def getLeftV(self):
        return (-cos(self.rotation), -sin(self.rotation))

    def getNormal(self):
        
        norms = []
        norms.append( self.getTopV() )
        norms.append( self.getRightV() )
        norms.append( self.getBotV() )
        norms.append( self.getLeftV() )
        return norms

    #----------------------------------------#
    # Determine if point is inside square
    # NOTE! This fails for angle > 90 deg
    #----------------------------------------#
    def inCube(self, point):
        x = point[0]
        y = point[1]

        # Simple case, if there is no lean
        #if x > self.xpos + self.length/2.: return False
        #if x < self.xpos - self.length/2.: return False        
        #if y > self.ypos + self.height/2.: return False        
        #if y < self.ypos - self.height/2.: return False

        # Complicated case, if there is rotation in the ice
        # We need to take care of the fact that the side is
        # basically a function in x-y plane determined from
        # the rotation of the figure.
        
        # Top:
        if self.pointFails(0,x,y): return False
        if self.pointFails(1,x,y): return False
        if self.pointFails(2,x,y): return False
        if self.pointFails(3,x,y): return False

        return True



    #----------------------------------------#
    # Check if point passes
    #----------------------------------------#
    def pointFails(self,sideNum,x,y):
        slope = self.getSlope(sideNum)
        x0    = self.getX0(sideNum)
        y0    = self.getY0(sideNum)
        if slope == sys.float_info.max:
            if x0 < 0 and x < x0: return True
            if x0 > 0 and x > x0: return True
    
        ycomp = slope * x + y0
        if sideNum == 0 and y > y0: return True
        if sideNum == 2 and y < y0: return True
        if sideNum == 1:
            if slope < 0 and y > y0: return True
            if slope > 0 and y < y0: return True
        if sideNum == 3:
            if slope < 0 and y < y0: return True
            if slope > 0 and y > y0: return True
        
        return False


    #----------------------------------------#
    # Get slope of the side
    #----------------------------------------#
    def getSlope(self, sideNum):

        # Two extreme cases where we have a verticle line
        if self.rotation == 0 and (sideNum == 1 or sideNum ==3):
            return sys.float_info.max
        if self.rotation*pi/180 == 90 and (sideNum == 0 or sideNum == 2):
            return sys.float_info.max

        # Now handle based on which side we are looking at
        if sideNum == 0 or sideNum == 2: return tan(self.rotation)
        else: return 1/tan(self.rotation)
    
    #----------------------------------------#
    # Get y0
    #----------------------------------------#
    def getY0(self, sideNum):
        
        x0    = 0
        y0    = 0
        slope = 0
        if sideNum == 0:
            x0 = -self.length/2.
            y0 =  self.height/2.
        elif sideNum == 1:
            x0 =  self.length/2.
            y0 =  self.height/2.
        elif sideNum == 2:
            x0 = -self.length/2.
            y0 = -self.height/2.
        elif sideNum == 3:
            x0 = -self.length/2.
            y0 = self.height/2.
        
        slope = self.getSlope(sideNum)
        x0,y0 = self.rotateCoords(x0,y0)
        
        return y0 - slope*x0

    #----------------------------------------#
    # Get x0 -- only needed when slope is 
    # infinite (eg. for a vertical line)
    #----------------------------------------#
    def getX0(self, sideNum):
        
        slope = self.getSlope(sideNum)
        if slope != sys.float_info.max:
            return 0
        
        x0    = 0
        y0    = 0
        slope = 0
        if sideNum == 0:
            x0 = -self.length/2.
            y0 =  self.height/2.
        elif sideNum == 1:
            x0 =  self.length/2.
            y0 =  self.height/2.
        elif sideNum == 2:
            x0 = -self.length/2.
            y0 = -self.height/2.
        elif sideNum == 3:
            x0 = -self.length/2.
            y0 = self.height/2.

        slope = self.getSlope(sideNum)
        x0,y0 = self.rotateCoords(x0,y0)
        
        return x0 - y0/slope
