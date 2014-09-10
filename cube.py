
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# This will be the virtual ice block and I wanted to have it as a class #
# so I can have methods to tell if the ray is still in the ice block.   #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

from visual import *

class cube:
    

    #----------------------------------------#
    # Constructor
    #----------------------------------------#
    def __init__(self,x,y,z,L,H):

        # Save generic characteristics
        self.xpos   = x
        self.ypos   = y
        self.zpos   = z
        self.length = L
        self.height = H

        # Create the box
        self.box = box(pos=(x,y,z),
                       length=L,
                       height=H,
                       width=0,
                       color=(0,1.5,1))
        
