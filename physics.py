
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# In here I will either put a list of methods or make it a class. The #
# idea will be to input some angle and get back either a refracted    #
# angle or the reflected angle.                                       #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

from math import *
import sys

#---------------------------------------------#
# Define constants needed for calculations
#---------------------------------------------#

# Index of refraction
nIce = 1.78
nAir = 1.

#---------------------------------------------#
# Define method to solve for crossing point
#---------------------------------------------#
def interactionPoint(rayAngle, rayY0, rayX0,
                     boundarySlope, boundaryY0, 
                     boundaryX0):

    # Check for non-zero slope
    # Which implies lines never cross
    if boundarySlope == 0 and tan(rayAngle) == 0:
        print "\tInt point info: ", boundarySlope, rayAngle, tan(rayAngle)
        return (-9999,-9999)
    
    # Handle the case of x=constant
    if boundaryX0 != sys.float_info.max:
        x = boundaryX0
        y = tan(rayAngle)*(x-rayX0) + rayY0
        print "Fixed x: ", x, y
        return (x,y)
    
    # All other cases can follow this:
    x = (boundaryY0 - rayY0) / (tan(rayAngle) - boundarySlope) - rayX0
    y = boundarySlope * (x) + boundaryY0
    print "Not Fixed x: ", x, y
    return (x,y)

#---------------------------------------------#
# Find incident angle
#---------------------------------------------#
def incidentAngle(v_ray, v_boundary,activeSide):
    
    # Angle we are after is the incident angle
    # of the ray on the boundary so we can
    # later check snell's law. 
    # Incident Angle = 90 - angle between vectors
    print "\tVectors: ", v_ray, v_boundary
    mag = v_ray[0]*v_boundary[0] + v_ray[1]*v_boundary[1]
    magRay = sqrt(v_ray[0]*v_ray[0]+v_ray[1]*v_ray[1])
    magB   = sqrt(v_boundary[0]*v_boundary[0]+v_boundary[1]*v_boundary[1])
    angle = acos( mag/(magRay*magB) )

    print "\tAngle between vectors: ", angle, angle*180/pi
    #print "\tIncident angle: ",  angle, (pi/2.-angle)*180/pi
    
    # Subtract pi/2
    #if activeSide == 1 or activeSide == 3:
    #    return pi/2 - angle

    return angle


#---------------------------------------------#
# Check for refraction
#---------------------------------------------#
def refractedAngle(incidentAngle):
    
    # Check for TIR case first
    arg = nIce/nAir * sin(fabs(incidentAngle))
    
    # If arg > 1, we have TIR
    if arg > 1: return -1
    
    # Otherwise, the ray leaves
    #print asin(arg)
    return asin(arg)

    
#---------------------------------------------#
# Get perpendicular vector
#---------------------------------------------#
def getPerp(point):
    x = point[0]
    y = point[1]
    
    return (y,x)
