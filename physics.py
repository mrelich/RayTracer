
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
    if boundarySlope == sys.float_info.max:
        x = boundaryX0
        y = tan(rayAngle)*(x-rayX0) + rayY0
        #print "\t\tFixed x: ", x, y
        return (x,y)
    
    # All other cases can follow this:
    #x = (boundaryY0 - rayY0) / (tan(rayAngle) - boundarySlope) + rayX0
    x = 1/(tan(rayAngle) - boundarySlope) * (boundaryY0 - rayY0  + tan(rayAngle)*rayX0 - boundarySlope*boundaryX0)
    y = boundarySlope * (x-boundaryX0) + boundaryY0
    #print "\t\tNot Fixed x: ", x, y
    #print "Ray info: ", rayAngle, rayY0, rayX0
    #print "boundary: ", boundarySlope, boundaryY0, boundaryX0
    return (x,y)

#---------------------------------------------#
# Find incident angle
#---------------------------------------------#
def incidentAngle(v_ray, v_boundary,activeSide):
    
    # Angle we are after is the incident angle
    # of the ray on the boundary so we can
    # later check snell's law. 
    # Incident Angle = 90 - angle between vectors
    mag = v_ray[0]*v_boundary[0] + v_ray[1]*v_boundary[1]
    magRay = sqrt(v_ray[0]*v_ray[0]+v_ray[1]*v_ray[1])
    magB   = sqrt(v_boundary[0]*v_boundary[0]+v_boundary[1]*v_boundary[1])
    #print "\t\t\tMag = ", magRay, magB
    #print v_ray
    angle = acos( mag/(magRay*magB) )

    #print "\tAngle between vectors: ", angle, angle*180/pi
    #print "\tIncident angle: ",  angle, (pi/2.-angle)*180/pi
    
    # Subtract pi/2
    #if activeSide == 1 or activeSide == 3:
    #    return pi/2 - angle

    return angle


#---------------------------------------------#
# Check for refraction
#---------------------------------------------#
def refractedAngle(incidentAngle, slope, activeSide, iceTilt):
    
    # Check for TIR case first
    arg = nIce/nAir * sin(fabs(incidentAngle))
    
    # If arg > 1, we have TIR
    if arg > 1: return -1

    # Otherwise, the ray leaves
    angle = asin(arg) 
    #print "In refracted: ", arg, angle, angle*180/pi
    return angle


#---------------------------------------------#
# Get reflected angle
#---------------------------------------------#
def reflectedAngle(sign, incidentAngle, activeSide, rotAng):
    
    if activeSide == 0:
        return sign*(pi/2. - incidentAngle)
    elif activeSide == 1:
        return sign*(pi/2. - incidentAngle)
    elif activeSide == 2:
        return pi/2 - incidentAngle
    elif activeSide == 3:
        return sign*(pi/2. - incidentAngle)

#---------------------------------------------#
# Translate angle to det coords
#---------------------------------------------#
def translateAngle(x0, y0, intX0, intY0, 
                   rotAng, refAng, activeSide):
    # x0,y0 = original position
    # rayX0,rayY0 = incident point on wall
    # refAngle = refracted angle
    # activeSide = side of the cube (0=top, 1=right, etc)
    
    # The rotation angle is actually for the cube
    # in the frames orientation.  We want to rotate
    # our coordinate system such that it is normal to the cube
    rotAng = -rotAng

    # The idea is to put the coordinate system at
    # the interaction point with normal to the side
    # in the positive y direction and then check where
    # our initial ray point lies to determine the angle
    # in the coordinate system of the block
    xt = x0 - intX0  # translate x
    yt = y0 - intY0  # translate y
    xr = xt*cos(rotAng) - yt*sin(rotAng)
    yr = xt*sin(rotAng) + yt*cos(rotAng)

    #print xt, yt, xr, yr, rotAng*180./pi

    # Remember, refracted angle is w/respect to
    # the normal.  Make it with respect to x-axis

    # Top of cube
    pi2 = pi/2.
    if activeSide == 0: 
        if xr > 0: return pi2 + refAng
        return pi2 - refAng
    # Right
    elif activeSide == 1:
        if yr > 0: return -refAng
        return refAng
    # Bottom
    elif activeSide == 2:
        refAng = pi2 + refAng
        if xr < 0: return -refAng
        return refAng
    # Left
    elif activeSide == 3:
        if yr < 0: return pi/2-refAng 
        return refAng

    # Do nothing
    return refAng

#---------------------------------------------#
# Get perpendicular vector
#---------------------------------------------#
def getPerp(point):
    x = point[0]
    y = point[1]
    
    return (y,x)
