# PURE MATHS, NO PYGAME
# two balls touching, have centers exactly one diameter or two radii apart. 

import math

def ghost_ball_position(target, pocket, radius):
    
    """
    Return the (x, y) centre of the ghost ball, in the same units as the inputs.
    target and pocket are (x, y) pairs. radius is the ball radius.
    Raises ValueError if the target is on the pocket centre.
    """
    
    dx = pocket[0] - target[0]
    dy = pocket[1] - target[1]
    
    length = math.hypot(dx,dy)
    
    if length == 0:
        raise ValueError("Why is the target ball in the center of the pocket you stupid cunt")
    
    ux = dx / length 
    uy =  dy / length 
