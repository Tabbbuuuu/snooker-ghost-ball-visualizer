# WINDOW + EVENT LOOP

import pygame
import math
from table import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Snooker Ghost-Ball Visualizer")
clock = pygame.time.Clock()

running = True

# dictionary for all the balls (positions in mm)
balls = {
    "cue": (TABLE_LENGTH_MM * 0.25, TABLE_WIDTH_MM * 0.5),
    "target": (TABLE_LENGTH_MM * 0.60, TABLE_WIDTH_MM * 0.40),
}

dragging = None          # name of ball being dragged, or None
selected_pocket = 0      # index into POCKETS_MM; start with the first pocket
GRAB_RADIUS_MM = BALL_RADIUS_MM * 2             # forgiving click area for balls
POCKET_CLICK_RADIUS_MM = POCKET_RADIUS_MM * 2   # forgiving click area for pockets

while running:
    # ---------- EVENTS: change the state ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = px_to_mm(*event.pos)

            # 1. Try to grab a ball first
            for name, (bx, by) in balls.items():
                if math.hypot(mx - bx, my - by) <= GRAB_RADIUS_MM:
                    dragging = name

            # 2. If no ball was grabbed, try to select a pocket
            if dragging is None:
                for i, (pkx, pky) in enumerate(POCKETS_MM):
                    if math.hypot(mx - pkx, my - pky) <= POCKET_CLICK_RADIUS_MM:
                        selected_pocket = i

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = None

        elif event.type == pygame.MOUSEMOTION and dragging is not None:
            balls[dragging] = px_to_mm(*event.pos)

    #DRAWING
    screen.fill((30, 30, 30))

    cloth = pygame.Rect(
        round(ORIGIN_X), round(ORIGIN_Y),
        round(TABLE_LENGTH_MM * SCALE),
        round(TABLE_WIDTH_MM * SCALE),
    )
    pygame.draw.rect(screen, (90, 55, 30), cloth.inflate(60, 60))
    pygame.draw.rect(screen, (0, 100, 50), cloth)

    # pockets
    pocket_radius_px = round(POCKET_RADIUS_MM * SCALE)
    for x_mm, y_mm in POCKETS_MM:
        pygame.draw.circle(screen, (0, 0, 0), mm_to_px(x_mm, y_mm), pocket_radius_px)

    # highlight ring on the selected pocket (drawn after pockets, so it's on top)
    sel_center = mm_to_px(*POCKETS_MM[selected_pocket])
    pygame.draw.circle(screen, (255, 220, 0), sel_center, pocket_radius_px + 4, 3)

    # balls
    ball_radius_px = round(BALL_RADIUS_MM * SCALE)
    pygame.draw.circle(screen, (255, 255, 255), mm_to_px(*balls["cue"]), ball_radius_px)
    pygame.draw.circle(screen, (200, 30, 30), mm_to_px(*balls["target"]), ball_radius_px)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
