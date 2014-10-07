
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
    # Wrapper method to return the equations
    # the normals and the side numbers
    #----------------------------------------#
    def getSideInformation(self, initAngle):

        # Get the right to left results
        eqs   = self.getEquations()
        norms = self.getNormal()
        nums  = [0,1,2,3]

        # Rotate angle to be normal to 
        # the rotated cube
        angle = initAngle + self.rotation

        newNums = nums
        #if 0 <= angle and angle <= 90:
        #    newNums = nums
        if 90 < angle and angle <= 90+45:
            newNums  = [0,3,2,1]
        elif 90+45 < angle:
            newNums = [3,2,1,0]
        
        # Set the return values
        newEqs   = []
        newNorms = []
        for i in newNums:
            newEqs.append(eqs[i])
            newNorms.append(norms[i])
        
        # Return
        return newEqs, newNorms, newNums

    #----------------------------------------#    
    # Setup the equations
    #----------------------------------------#
    def getTop(self):   return self.buildEquation(0)
    def getRight(self): return self.buildEquation(1)
    def getBot(self):   return self.buildEquation(2)
    def getLeft(self):  return self.buildEquation(3)

    def getEquations(self):

        equations = []
        equations.append( self.getTop() )
        equations.append( self.getRight() )
        equations.append( self.getBot() )
        equations.append( self.getLeft() )
        #self.printEquations(equations)
        return equations

    def printEquations(self,eqs):
        for eq in eqs:
            s = eq[0]
            y0 = eq[1]
            x0 = eq[2]
            print "Eq: "+ str(s) + "*(x-"+str(x0)+") + "+str(y0) 
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

        # Get Equations
        Eqs = self.getEquations()
        if self.pointFails(0,Eqs[0],x,y): return False
        if self.pointFails(1,Eqs[1],x,y): return False
        if self.pointFails(2,Eqs[2],x,y): return False
        if self.pointFails(3,Eqs[3],x,y): return False

        return True



    #----------------------------------------#
    # Check if point passes
    #----------------------------------------#
    def pointFails(self,sideNum,eq,x,y):
        slope = eq[0]
        x0    = eq[2]
        y0    = eq[1]
        if slope == sys.float_info.max:
            #print "\t\t\tInfinite slope: ", x, x0
            if x0 < 0 and x < x0: return True
            if x0 > 0 and x > x0: return True
            return False
    
        ycomp = slope * (x-x0) + y0
        if sideNum == 0 and y > ycomp: return True
        if sideNum == 2 and y < ycomp: return True
        if sideNum == 1:
            if slope < 0 and y > ycomp: return True
            if slope > 0 and y < ycomp: return True
        if sideNum == 3:
            if slope < 0 and y < ycomp: return True
            if slope > 0 and y > ycomp: return True
        
        return False


    #----------------------------------------#
    # Get the slope, y0, and x0 position
    #----------------------------------------#
    def buildEquation(self,sideNum):

        # Deal with two specific cases: 0 and 90 degree rotation
        if self.rotation == 0: # Perfect cube
            if sideNum == 1 or sideNum == 3:
                x0 = self.length/2.
                if(sideNum == 3): x0 = -x0
                return (sys.float_info.max, 0, x0)
            else:
                y0 = self.height/2.
                if sideNum == 2: y0 = -y0
                return (0, y0, 0)
        elif self.rotation == 90*pi/180: # rotated cube
            if sideNum == 1 or sideNum == 3:
                y0 = -self.length/2.
                if sideNum == 3: y0 = -y0
                return (0,y0,0)
            else:
                x0 = self.height/2.
                if sideNum == 2: x0 = -x0
                return (sys.float_info.max, 0, x0)
        
        # Now handle generic rotation case
        x1 = 0
        x0 = 0
        y1 = 0
        y0 = 0
        
        # Start from a perfect cube
        if sideNum == 0:
            x0 = -self.length/2.
            x1 = self.length/2.
            y0 = self.height/2.
            y1 = self.height/2.
        elif sideNum == 1:
            x0 = self.length/2.
            x1 = self.length/2.
            y0 = -self.height/2.
            y1 = self.height/2.
        elif sideNum == 2:
            x0 = -self.length/2.
            x1 = self.length/2.
            y0 = -self.height/2.
            y1 = -self.height/2.
        elif sideNum == 3:
            x0 = -self.length/2.
            x1 = -self.length/2.
            y0 = -self.height/2.
            y1 = self.height/2.

        # Now add rotation
        x1,y1 = self.rotateCoords(x1,y1)
        x0,y0 = self.rotateCoords(x0,y0)
        
        # Define slope
        slope = (y1-y0)/(x1-x0)
        
        # Now return equation
        return (slope,y0,x0)
