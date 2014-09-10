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

#-------------------------------------#
# Setup the environment
#-------------------------------------#

window = display(title='Ray Tracing', x=0, y=0, 
                 width=600, height=600,
                 center=(0,0,0), background=(1,1,1),
                 range=1)

#-------------------------------------#
# Make the ice block
#-------------------------------------#

# Dimensions
length = 1   # [m]
height = 0.3 # [m]
width  = 0.3 # [m] This is not used. Just 2D

# Locations
icex = 0
icey = 0
icez = 0

# make the cube
iceblock = cube(icex,icey,icez,length,height)
