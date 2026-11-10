# WINDOW, EVENT LOOP AND STATE

import pygame
import math
from table import (
    WINDOW_W, TABLE_LENGTH_MM, TABLE_WIDTH_MM,
    BALL_RADIUS_MM, POCKET_RADIUS_MM, POCKETS_MM, px_to_mm,
)
from geometry import (
    ghost_ball_position,
    is_straight_shot_possible,
    clamp_to_table,
    balls_overlap,
    path_blocked,
)
from table import WINDOW_H
import draw

pygame.init()
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Snooker Ghost-Ball Visualizer")
clock = pygame.time.Clock()

running = True

# positions in mm
balls = {
    "cue": (TABLE_LENGTH_MM * 0.25, TABLE_WIDTH_MM * 0.5),
    "target": (TABLE_LENGTH_MM * 0.60, TABLE_WIDTH_MM * 0.40),
    "ball2": (TABLE_LENGTH_MM * 0.50, TABLE_WIDTH_MM * 0.80),
}

dragging = None          # name of ball being dragged, or None
selected_pocket = 0      # index into POCKETS_MM
target_name = "target"   # which ball we're aiming at: "target" or "ball2"
GRAB_RADIUS_MM = BALL_RADIUS_MM * 2
POCKET_CLICK_RADIUS_MM = POCKET_RADIUS_MM * 2
font = pygame.font.SysFont(None, 28)

while running:
    #EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = px_to_mm(*event.pos)

            best = GRAB_RADIUS_MM
            for name, (bx, by) in balls.items():
                d = math.hypot(mx - bx, my - by)
                if d <= best:
                    best = d
                    dragging = name

            if dragging is None:
                for i, (pkx, pky) in enumerate(POCKETS_MM):
                    if math.hypot(mx - pkx, my - pky) <= POCKET_CLICK_RADIUS_MM:
                        selected_pocket = i

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = None

        elif event.type == pygame.MOUSEMOTION and dragging is not None:
            new_pos = clamp_to_table(px_to_mm(*event.pos),
                                     TABLE_LENGTH_MM, TABLE_WIDTH_MM, BALL_RADIUS_MM)
            others = [pos for name, pos in balls.items() if name != dragging]
            if not any(balls_overlap(new_pos, o, BALL_RADIUS_MM) for o in others):
                balls[dragging] = new_pos

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:
            target_name = "ball2" if target_name == "target" else "target"

    # LOGIC
    pocket = POCKETS_MM[selected_pocket]
    aim_ball = balls[target_name]
    obstacle = balls["ball2" if target_name == "target" else "target"]

    try:
        ghost = ghost_ball_position(aim_ball, pocket, BALL_RADIUS_MM)
    except ValueError:
        ghost = None

    shot_ok = False
    messages = []
    if ghost is not None:
        shot_ok = is_straight_shot_possible(balls["cue"], ghost, aim_ball, pocket)
        if not shot_ok:
            messages.append("Straight shot not possible")
        if path_blocked(balls["cue"], ghost, [obstacle], BALL_RADIUS_MM):
            messages.append("Cue ball path is blocked")
        if path_blocked(aim_ball, pocket, [obstacle], BALL_RADIUS_MM):
            messages.append("Target ball's path to the pocket is blocked")

    # DRAWING:
    draw.draw_table(screen)
    draw.draw_pockets(screen, selected_pocket)
    draw.draw_aim_lines(screen, balls["cue"], aim_ball, pocket, ghost, shot_ok)
    draw.draw_balls(screen, balls, target_name)
    draw.draw_ghost(screen, ghost)
    draw.draw_text(screen, font, messages)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
