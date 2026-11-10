# ALL DRAWING CODE
import pygame
import math
from table import (
    WINDOW_H, ORIGIN_X, ORIGIN_Y, SCALE,
    TABLE_LENGTH_MM, TABLE_WIDTH_MM,
    BALL_RADIUS_MM, POCKET_RADIUS_MM, POCKETS_MM,
    mm_to_px,
)

# Colours in one place, so restyling later means editing only this block
BACKGROUND = (30, 30, 30)
FRAME = (90, 55, 30)
CLOTH = (18, 118, 64)
POCKET = (0, 0, 0)
HIGHLIGHT = (255, 220, 0)
LINE_OK = (220, 220, 220)
LINE_BAD = (220, 50, 50)
WARNING = (255, 120, 120)
HINT = (200, 200, 200)
BALL_COLOURS = {
    "cue": (255, 255, 255),
    "target": (200, 30, 30),
    "ball2": (230, 200, 0),
}


# finer details 

FRAME_OUTER = (62, 36, 18)    # dark wood edge
FRAME_INNER = (112, 70, 36)   # lighter wood
CUSHION = (0, 78, 40)         # darker green rail
POCKET_RIM = (25, 15, 8)
CUSHION_PX = 16               # cushion thickness on screen
FRAME_PX = 26                 # wooden frame thickness on screen

def draw_table(screen):
    """Background, two-tone wooden frame, cushions, then the cloth."""
    screen.fill(BACKGROUND)
    cloth = pygame.Rect(
        round(ORIGIN_X), round(ORIGIN_Y),
        round(TABLE_LENGTH_MM * SCALE),
        round(TABLE_WIDTH_MM * SCALE),
    )
    c, f = CUSHION_PX, FRAME_PX
    # biggest shape first, each smaller one is painted on top
    pygame.draw.rect(screen, FRAME_OUTER, cloth.inflate(2 * (c + f), 2 * (c + f)),
                     border_radius=14)
    pygame.draw.rect(screen, FRAME_INNER, cloth.inflate(2 * (c + f) - 8, 2 * (c + f) - 8),
                     border_radius=11)
    pygame.draw.rect(screen, CUSHION, cloth.inflate(2 * c, 2 * c), border_radius=4)
    pygame.draw.rect(screen, CLOTH, cloth)


def draw_pockets(screen, selected_pocket):
    """Six pockets with a dark rim, plus a ring around the selected one."""
    radius = round(POCKET_RADIUS_MM * SCALE)
    for x_mm, y_mm in POCKETS_MM:
        centre = mm_to_px(x_mm, y_mm)
        pygame.draw.circle(screen, POCKET_RIM, centre, radius + 3)
        pygame.draw.circle(screen, POCKET, centre, radius)
    selected = POCKETS_MM[selected_pocket]
    pygame.draw.circle(screen, HIGHLIGHT, mm_to_px(*selected), radius + 6, 3)
    
def draw_dashed_line(screen, colour, start, end, width=2, dash=10, gap=7):
    """Draw a dashed line from start to end (pixel coordinates)."""
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    pos = 0
    while pos < length:
        seg_end = min(pos + dash, length)
        a = (start[0] + ux * pos, start[1] + uy * pos)
        b = (start[0] + ux * seg_end, start[1] + uy * seg_end)
        pygame.draw.line(screen, colour, a, b, width)
        pos += dash + gap


def draw_arrowhead(screen, colour, tip, direction, size=14):
    """Filled triangle with its point at tip, aimed along direction (ux, uy)."""
    ux, uy = direction
    px, py = -uy, ux  # perpendicular to the direction
    base = (tip[0] - ux * size, tip[1] - uy * size)
    left = (base[0] + px * size * 0.45, base[1] + py * size * 0.45)
    right = (base[0] - px * size * 0.45, base[1] - py * size * 0.45)
    pygame.draw.polygon(screen, colour, [tip, left, right])


def draw_aim_lines(screen, cue, aim_ball, pocket, ghost, shot_ok):
    """Dashed ball-to-pocket line with arrowhead; solid cue-to-ghost line."""
    start = mm_to_px(*aim_ball)
    end = mm_to_px(*pocket)
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = math.hypot(dx, dy)
    if length > 0:
        u = (dx / length, dy / length)
        # stop the arrow at the pocket's edge, not its centre
        pocket_r = round(POCKET_RADIUS_MM * SCALE)
        tip = (end[0] - u[0] * pocket_r, end[1] - u[1] * pocket_r)
        draw_dashed_line(screen, HIGHLIGHT, start, tip, 2)
        draw_arrowhead(screen, HIGHLIGHT, tip, u)

    if ghost is not None:
        colour = LINE_OK if shot_ok else LINE_BAD
        pygame.draw.line(screen, colour, mm_to_px(*cue), mm_to_px(*ghost), 2)


def shade(colour, factor):
    """Scale an (r, g, b) colour brighter (>1) or darker (<1)."""
    return tuple(max(0, min(255, round(c * factor))) for c in colour)


def draw_ball(screen, centre, radius, colour):
    """One ball: shadow, base, dark rim, soft highlight."""
    x, y = centre
    # shadow, offset down-right and drawn first
    pygame.draw.circle(screen, (10, 60, 30), (x + 2, y + 3), radius)
    # base colour
    pygame.draw.circle(screen, colour, centre, radius)
    # darker rim: outline only
    pygame.draw.circle(screen, shade(colour, 0.6), centre, radius, 2)
    # lighter patch toward the light, then a small white glint on top
    hx, hy = x - radius // 3, y - radius // 3
    pygame.draw.circle(screen, shade(colour, 1.3), (hx, hy), max(2, radius // 2))
    pygame.draw.circle(screen, (255, 255, 255), (hx - 1, hy - 1), max(1, radius // 5))


def draw_balls(screen, balls, aim_name):
    """All balls, plus a ring around the one being aimed at."""
    radius = round(BALL_RADIUS_MM * SCALE)
    for name, pos in balls.items():
        draw_ball(screen, mm_to_px(*pos), radius, BALL_COLOURS[name])
    pygame.draw.circle(screen, HIGHLIGHT, mm_to_px(*balls[aim_name]), radius + 2, 2)
    
def draw_ghost(screen, ghost, shot_ok=True):
    """Translucent ghost ball with an outline."""
    if ghost is None:
        return
    radius = round(BALL_RADIUS_MM * SCALE)
    colour = LINE_OK if shot_ok else LINE_BAD
    size = radius * 2 + 4
    overlay = pygame.Surface((size, size), pygame.SRCALPHA)  # supports transparency
    pygame.draw.circle(overlay, (*colour, 70), (size // 2, size // 2), radius)
    screen.blit(overlay, (mm_to_px(*ghost)[0] - size // 2, mm_to_px(*ghost)[1] - size // 2))
    pygame.draw.circle(screen, colour, mm_to_px(*ghost), radius, 2)


def draw_text(screen, font, messages):
    """Warnings stacked at the top left, plus a key hint at the bottom."""
    for i, msg in enumerate(messages):
        screen.blit(font.render(msg, True, WARNING), (20, 10 + i * 26))
    hint = font.render("T: switch aimed ball", True, HINT)
    screen.blit(hint, (20, WINDOW_H - 30))
