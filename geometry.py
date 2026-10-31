# PURE MATHS, NO PYGAME
# Two balls touching have centres exactly one diameter (two radii) apart.

import math


def ghost_ball_position(target, pocket, radius):
    """
    Return the (x, y) centre of the ghost ball, in the same units as the inputs.
    target and pocket are (x, y) pairs. radius is the ball radius.
    Raises ValueError if the target is on the pocket centre.
    """
    dx = pocket[0] - target[0]
    dy = pocket[1] - target[1]

    length = math.hypot(dx, dy)

    if length == 0:
        raise ValueError("Target ball is on the pocket centre; direction is undefined")

    ux = dx / length
    uy = dy / length

    return (target[0] - ux * 2 * radius, target[1] - uy * 2 * radius)



def is_straight_shot_possible(cue, ghost, target, pocket):
    """True if the cue ball can reach the ghost ball without passing
    through the target. All arguments are (x, y) pairs."""
    ax = ghost[0] - cue[0]   # cue -> ghost, x
    ay = ghost[1] - cue[1]   # cue -> ghost, y
    bx = pocket[0] - target[0]   # target -> pocket, x
    by = pocket[1] - target[1]   # target -> pocket, y
    return ax * bx + ay * by > 0
