#!/usr/bin/python

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

#-------------------------------------#
# Setup the environment
#-------------------------------------#

m_world = 1
window = display(title='Ray Tracing', x=0, y=0, 
                 width=600, height=600,
                 center=(0,0,0), background=(1,1,1),
                 range=m_world)

#-------------------------------------#
# Make the ice block
#-------------------------------------#

# Dimensions
length  = 1  # [m]
height  = 0.3 # [m]
width   = 0.3 # [m] This is not used. Just 2D

# Locations
icex = 0
icey = 0
icez = 0

# Angle to rotate
rotAng = -30*pi/180. # [rad]
#rotAng = 30*pi/180. # [rad]
#rotAng = 0. # [rad]

# make the cube
iceblock = cube(icex,icey,icez,length,height,rotAng)

# Draw axis
#yaxis = curve(pos=[(0,height),(0,-height)],color=(0,0,0),radius = -0.003)
#xaxis = curve(pos=[(length,0),(-length,0)],color = (0,0,0),radius = -0.003)

#-------------------------------------#
# Determine which angles to draw
#-------------------------------------#

# Define angles to consider
#angles = [pi/2,pi/6.] #,pi/3,pi/4,pi/5,pi/6] #,pi/8]

angles = []
conv = pi/180.
if False: #True: #True:
    #angles.append(90*conv)
    #angles.append(80*conv)
    #angles.append(70*conv)
    #angles.append(30*conv)
    #angles.append(40*conv)
    #angles.append(90*conv)
    #angles.append(50*conv)
    #angles.append(60*conv)
    #angles.append(50*conv)
    #angles.append(60*conv)
    #angles.append(30*conv)
    #angles.append((90-57)*conv)
    #angles.append(20*conv)
    #angles.append(10*conv)
    angles.append(100*conv)

if True: 
    nStep = 18
    step = 5 # [deg]
    start = 0
    for i in range(nStep+1):
        angles.append(conv*(start +i*step))

botEq = iceblock.getBot()
x0    = 0
y0    = botEq[0]*(x0-botEq[2]) + botEq[1] + 0.1


# Add Rays for each angle and calculate
# the points
rays = []
for ang in angles:

    # Get equations defining cube
    iceEq    = iceblock.getEquations()
    normals  = iceblock.getNormal()
    sideNums = [0,1,2,3]

    # Print some info
    print "------------------------------------------------------------"
    print "Trying angle: ", ang, ang*180/pi
    #print iceEq
    #print normals
    #print sideNums

    # Create new ray for this angle
    newray = ray(ang,x0,y0)

    # Loop until refracted angle is positive
    # or hits all four sides
    angRef   = -1
    nSides   = 0
    activeSide = -1
    point = -1
    while angRef < 0 and nSides <= 6:

        # Get interaction point
        intPoint = (0,0)
        v_normal   = (0,0)
        insideIce = False
        #print "Looping over equations: ", nSides
        #print "with coords: ", newray.angle*180/pi, newray.x, newray.y
        for i in range(len(iceEq)):
            eq = iceEq[i]
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
                #print "\tActive side: ", activeSide
                break

        # Change order of iceEq
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
        print "\t\tIncident Point: ",intPoint
        newray.addPoint(intPoint[0],intPoint[1])

        # Get Incident angle
        #print "Prior to Incident; ", newray.getVector(), v_normal
        incAngle = incidentAngle(newray.getVector(),v_normal,activeSide)
        print "\t\tIncident Angle: ", incAngle*180/pi

        # Check if there is refraction
        angRef = refractedAngle(incAngle, newray.angle, activeSide, rotAng)
        #print "\t\tRefracted angle", angRef, angRef * 180/pi

        if angRef < 0: 
            print "\t\t\tTIR!"
            sign = -1
            if newray.angle < 0: sign = 1
            if newray.angle > 0 and saveEq[0] > 0: sign = 1
            newAngle = sign*(pi/2. - incAngle)
            print "\t\t\tReflected Angle", newAngle*180/pi, sign, incAngle
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
            #if newray.angle < 0: sign = -1

            x = m_world*cos(fixedAngle)
            y = m_world*sin(fixedAngle)
            
            #if activeSide == 0:             # Top
            #    x = sign*m_world*sin(fixedAngle)
            #    y = m_world*cos(fixedAngle)
            #elif activeSide == 1:             # Right
            #    x = m_world*cos(fixedAngle)
            #    y = sign*m_world*sin(fixedAngle)
            #elif activeSide == 2:
            #    x = sign*m_world*sin(fixedAngle)
            #    y = -m_world*cos(fixedAngle)
            #else:
            #    x = -m_world*cos(fixedAngle)
            #    y = sign*m_world*sin(fixedAngle)
            
            print x, y
            # Add final point off in the distance
            newray.addPoint(intPoint[0]+x,intPoint[1]+y)
        
        # Incraease nSides hit by one
        nSides += 1

        # Add a check for corner events
        # Remove if point is within 10% of edges
        ratioX = 1- fabs(intPoint[0])/(iceblock.xpos + iceblock.length/2.)
        ratioY = 1- fabs(intPoint[1])/(iceblock.ypos + iceblock.height/2.)
        threshold = 0.05
        if ratioX < threshold and ratioY < threshold:
            break

    # end while loop

    newray.drawRay()
    #rays.append(newray)

#end loop over angles
                                
sys.exit()
