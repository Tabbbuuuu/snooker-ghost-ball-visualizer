# ALL DRAWING CODE# ALL DRAWING CODE
import pygame
from table import (
    WINDOW_H, ORIGIN_X, ORIGIN_Y, SCALE,
    TABLE_LENGTH_MM, TABLE_WIDTH_MM,
    BALL_RADIUS_MM, POCKET_RADIUS_MM, POCKETS_MM,
    mm_to_px,
)

# Colours in one place, so restyling later means editing only this block
BACKGROUND = (30, 30, 30)
FRAME = (90, 55, 30)
CLOTH = (0, 100, 50)
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


def draw_table(screen):
    """Background, wooden frame and green cloth."""
    screen.fill(BACKGROUND)
    cloth = pygame.Rect(
        round(ORIGIN_X), round(ORIGIN_Y),
        round(TABLE_LENGTH_MM * SCALE),
        round(TABLE_WIDTH_MM * SCALE),
    )
    pygame.draw.rect(screen, FRAME, cloth.inflate(60, 60))
    pygame.draw.rect(screen, CLOTH, cloth)


def draw_pockets(screen, selected_pocket):
    """Six pockets, plus a ring around the selected one."""
    radius = round(POCKET_RADIUS_MM * SCALE)
    for x_mm, y_mm in POCKETS_MM:
        pygame.draw.circle(screen, POCKET, mm_to_px(x_mm, y_mm), radius)
    selected = POCKETS_MM[selected_pocket]
    pygame.draw.circle(screen, HIGHLIGHT, mm_to_px(*selected), radius + 4, 3)


def draw_aim_lines(screen, cue, aim_ball, pocket, ghost, shot_ok):
    """Ball-to-pocket line, and cue-to-ghost line if a ghost exists."""
    pygame.draw.line(screen, HIGHLIGHT, mm_to_px(*aim_ball), mm_to_px(*pocket), 2)
    if ghost is not None:
        colour = LINE_OK if shot_ok else LINE_BAD
        pygame.draw.line(screen, colour, mm_to_px(*cue), mm_to_px(*ghost), 2)


def draw_balls(screen, balls, aim_name):
    """All balls, plus a ring around the one being aimed at."""
    radius = round(BALL_RADIUS_MM * SCALE)
    for name, pos in balls.items():
        pygame.draw.circle(screen, BALL_COLOURS[name], mm_to_px(*pos), radius)
    pygame.draw.circle(screen, HIGHLIGHT, mm_to_px(*balls[aim_name]), radius + 4, 2)


def draw_ghost(screen, ghost):
    """Outline-only ghost ball, so it reads as imaginary."""
    if ghost is not None:
        radius = round(BALL_RADIUS_MM * SCALE)
        pygame.draw.circle(screen, LINE_OK, mm_to_px(*ghost), radius, 2)


def draw_text(screen, font, messages):
    """Warnings stacked at the top left, plus a key hint at the bottom."""
    for i, msg in enumerate(messages):
        screen.blit(font.render(msg, True, WARNING), (20, 10 + i * 26))
    hint = font.render("T: switch aimed ball", True, HINT)
    screen.blit(hint, (20, WINDOW_H - 30))
