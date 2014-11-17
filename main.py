#!/usr/local/bin/python

# This is for runnning on linux
#!/usr/bin/python

# For running on my mac
#!/usr/local/bin/python

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
# This will be the 'executable' that will draw the ray tracing for the ice #
# block. Will add some options in the future, but at first we consider a   #
# simple case.                                                             #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

#-------------------------------------#
# Import necessaries
#-------------------------------------#

from visual import *
from cube import *
from ray import *
from physics import *
import sys
from optparse import OptionParser

#-------------------------------------#
# Parse some simple user options
#-------------------------------------#

#
## Setup parser
#
parser = OptionParser()

parser.add_option("-s", "--stepsize", action="store",
                  #type=int, default=10, dest="stepsize",
                  type=float, default=10, dest="stepsize",
                  help="Option to set number of steps")
parser.add_option("-l", "--less90", action="store_true",
                  default=False, dest="L90",
                  help="Option to run angles 0-90")
parser.add_option("-g", "--greater90", action="store_true",
                  default=False, dest="G90",
                  help="Optin to run angles 90-180")
parser.add_option("-a","--angle",action="store",
                  type=float,default=-1,dest="angle",
                  help="Specify a specific angle")
parser.add_option("-r", "--rotation", action="store",
                  type=float, default=-30,dest="rotAngle",
                  help="Specify rotation angle for ice")
parser.add_option("-i", "--injection", action="store",
                  type=float, default=0,dest="injPoint",
                  help="Specify injection point in ice")

#
## Load the options
#

print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
print "Starting ray tracing program"
print ""

opts, args = parser.parse_args()

angles = []
stepsize = opts.stepsize
if opts.L90:
    angMax = 90
    angle  = 0
    while angle <= angMax:
        angles.append( angle )
        angle += stepsize
    print "Running for angles 0-90"
elif opts.G90:
    angMax = 180
    angle  = 90
    while angle <= angMax:
        angles.append( angle )
        angle += stepsize
    print "Running for angles 90-180"
elif opts.angle > 0:
    angles.append( opts.angle )
    print "Running for angle: ", angles[0]
else:
    print "Please specify angles to use."
    print ""
    sys.exit()

print angles
print ""
print ""


#
## Convert all angles to radians
#
for i in range(len(angles)):
    angles[i] = angles[i] * pi/180.

#
## Save rotation angle
#

rotAng = opts.rotAngle * pi/180

#-------------------------------------#
# Setup the environment
#-------------------------------------#

m_world = 1
window = display(title='Ray Tracing', x=0, y=0, 
                 width=800, height=800,
                 center=(0,0,0), 
                 #center=(5,0,0), 
                 #scale=(0.1,0.1,1),
                 background=(1,1,1),                 
                 range=m_world)

#-------------------------------------#
# Add antenna Pole off to the right
#-------------------------------------#

#p_height = 8 # [m]
#p_center = (8,-0.15,0)  # [m]
#pole = cylinder(pos = p_center,
#                axis = (0,p_height,0),
#                radius = 0.1,
#                color=(1,0,0))


#-------------------------------------#
# Make the ice block
#-------------------------------------#

# Dimensions
length  = 1  # [m]
#length  = 0.5  # [m]
#length  = 0.3  # [m]
height  = 0.3 # [m]
width   = 0.3 # [m] This is not used. Just 2D

# Locations
icex = 0
icey = 0
icez = 0

# make the cube
iceblock = cube(icex,icey,icez,length,height,rotAng)

# Draw axis
#yaxis = curve(pos=[(0,height),(0,-height)],color=(0,0,0),radius = -0.003)
#xaxis = curve(pos=[(length,0),(-length,0)],color = (0,0,0),radius = -0.003)

#-------------------------------------#
# Determine which angles to draw
#-------------------------------------#

# Specify x0 and y0 for beam
botEq = iceblock.getBot()
x0    = opts.injPoint
y0    = botEq[0]*(x0-botEq[2]) + botEq[1] + 0.06

# Add Rays for each angle and calculate
# the points
rays = []
for ang in angles:

    # Get equations defining cube
    #iceEq    = iceblock.getEquations()
    #normals  = iceblock.getNormal()
    #sideNums = [0,1,2,3]
    iceEq, normals, sideNums = iceblock.getSideInformation(ang*180/pi)

    # Hack for angles > 90
    #cornerAngle = pi - atan((iceblock.height/2.-y0)/(iceblock.length/2.-x0)) + iceblock.rotation
    #if ang > cornerAngle:
    #    temp = iceEq 
        #iceEq = [temp[3], temp[2], temp[1], temp[0]]
    #    iceEq = [temp[0], temp[3], temp[2], temp[1]]
    #    temp = normals
        #normals = [temp[3], temp[2], temp[1], temp[0]]
    #    normals = [temp[0], temp[3], temp[2], temp[1]]
        #sideNums = [3,2,1,0]
    #    sideNums = [0,3,2,1]
        

    # Print some info
    print "------------------------------------------------------------"
    print "Trying angle: ", ang, ang*180/pi

    # Create new ray for this angle
    newray = ray(ang,x0,y0)

    # Loop until refracted angle is positive
    # or hits all four sides
    angRef   = -1
    nSides   = 0
    activeSide = -1
    point = -1
    while angRef < 0 and nSides <= 10:

        # Get interaction point
        intPoint = (0,0)
        v_normal   = (0,0)
        insideIce = False
        for i in range(len(iceEq)):
            eq = iceEq[i]
            #print "Checking interaction point: ", sideNums[i]
            intPoint = interactionPoint(newray.angle,
                                        newray.y,
                                        newray.x,
                                        eq[0],
                                        eq[1],
                                        eq[2])

            if iceblock.inCube(intPoint): 
                insideIce  = True
                activeSide = sideNums[i]
                point      = i
                break

        # Change order of iceEq for next iteration
        # in case of reflection
        saveEq = iceEq[point]
        del iceEq[point]
        iceEq.append(saveEq)
        v_normal = normals[point]
        del normals[point]
        normals.append(v_normal)
        del sideNums[point]
        sideNums.append(activeSide)

        # Protect against exhausting all options
        if not insideIce: break
        print "\t\tIncident Point: ",intPoint, " on side", activeSide
        newray.addPoint(intPoint[0],intPoint[1])

        # Get Incident angle
        incAngle = incidentAngle(newray.getVector(),v_normal,activeSide)
        print "\t\tIncident Angle: ", incAngle*180/pi

        # Check if there is refraction
        angRef = refractedAngle(incAngle, newray.angle, activeSide, rotAng)

        if angRef < 0: 
            print "\t\t\tTIR!"
            newAngle = reflectedAngle(newray.x,newray.y,intPoint[0],intPoint[1],
                                      incAngle,activeSide,rotAng)
            newAngle += iceblock.rotation
            print "\t\t\tReflected Angle", (pi/2 - incAngle)*180/pi
            print "\t\t\tReflected Angle in frame coords", newAngle*180/pi 
            newray.update(newAngle,intPoint[1],intPoint[0])
            #newray.addPoint(intPoint[0], intPoint[1])
        else:
            print "\t\t\tRefracted Angle", angRef*180/pi
            fixedAngle = translateAngle(newray.x,newray.y,
                                        intPoint[0],intPoint[1],
                                        rotAng,angRef,activeSide)
            print "\t\t\t\tTranslated Angle", fixedAngle*180/pi
            fixedAngle += iceblock.rotation
            print "\t\t\t\tIncluding Rotation", fixedAngle*180/pi
            x = 0
            y = 0
            sign = 1

            x = m_world*cos(fixedAngle)
            y = m_world*sin(fixedAngle)
            
            # Add final point off in the distance
            newray.addPoint(intPoint[0]+x,intPoint[1]+y)

        # Incraease nSides hit by one
        nSides += 1

    # end while loop

    newray.drawRay()

#end loop over angles
sys.exit()
