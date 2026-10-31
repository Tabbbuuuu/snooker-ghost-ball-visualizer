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


def balls_overlap(a, b, radius):
    """True if two balls of the same radius overlap (touching is allowed)."""
    return math.hypot(a[0] - b[0], a[1] - b[1]) < 2 * radius


def clamp_to_table(pos, length, width, radius):
    """Return pos moved to the nearest spot where a ball's centre can
    sit without crossing a cushion."""
    x = max(radius, min(pos[0], length - radius))
    y = max(radius, min(pos[1], width - radius))
    return (x, y)


def point_segment_distance(p, a, b):
    """Shortest distance from point p to the line segment from a to b."""
    abx, aby = b[0] - a[0], b[1] - a[1]
    apx, apy = p[0] - a[0], p[1] - a[1]
    len_sq = abx * abx + aby * aby
    if len_sq == 0:
        return math.hypot(apx, apy)  # segment is a single point
    # t = how far along the segment the closest point is (0 = a, 1 = b)
    t = max(0, min(1, (apx * abx + apy * aby) / len_sq))
    closest_x = a[0] + t * abx
    closest_y = a[1] + t * aby
    return math.hypot(p[0] - closest_x, p[1] - closest_y)


def path_blocked(start, end, blockers, radius):
    """True if any blocker ball would hit a ball of this radius travelling
    from start to end. Touching is allowed."""
    return any(point_segment_distance(b, start, end) < 2 * radius
               for b in blockers)
