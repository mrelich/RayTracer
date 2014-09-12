
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
# A class for the definition of a ray, which will be a vpython object  #
# called a curve. It is convenient for specifying a list of points and #
# having a line connecting them.  Ideal for ray-tracing purposes.      #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

from visual import curve

class ray:

    #----------------------------------#
    # Constructor
    #----------------------------------#
    def __init__(self,angle,x0,y0):
        
        # Set initial angle, x0, and y0
        self.angle = angle
        self.y     = y0
        self.x     = x0
        self.points = []
        
        self.addPoint(x0,y0)

    #----------------------------------#
    # Add method to update angle
    #----------------------------------#
    def update(self,angle,y,x):
        self.angle = angle
        self.y     = y
        self.x     = x

    #----------------------------------#
    # Add points
    #----------------------------------#
    def addPoint(self,x,y):
        self.points.append((x,y))
        

    #----------------------------------#
    # Get vector of last two points
    #----------------------------------#
    def getVector(self):

        np = len(self.points)
        if np < 2: return (0,0)

        p0 = self.points[np-2]
        p1 = self.points[np-1]
        newX = p1[0] - p0[0]
        newY = p1[1] - p0[1]
        vect = (newX, newY)
        return vect

    #----------------------------------#
    # Make curve object
    #----------------------------------#
    def drawRay(self):
        print "Drawing Ray"
        print self.points
        self.ray = curve(pos=self.points,
                         color=(0,0,0),
                         radius=0.005
                         )
        
