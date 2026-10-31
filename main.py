# WINDOW + EVENT LOOP

import pygame
import math
from table import *
from geometry import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Snooker Ghost-Ball Visualizer")
clock = pygame.time.Clock()

running = True

# dictionary for all the balls (positions in mm)
balls = {
    "cue": (TABLE_LENGTH_MM * 0.25, TABLE_WIDTH_MM * 0.5),
    "target": (TABLE_LENGTH_MM * 0.60, TABLE_WIDTH_MM * 0.40),
    "blocker": (TABLE_LENGTH_MM * 0.50, TABLE_WIDTH_MM * 0.80),
}

dragging = None          # name of ball being dragged, or None
selected_pocket = 0      # index into POCKETS_MM
target_name = "target"   # which ball we're aiming at: "target" or "blocker"
GRAB_RADIUS_MM = BALL_RADIUS_MM * 2
POCKET_CLICK_RADIUS_MM = POCKET_RADIUS_MM * 2
font = pygame.font.SysFont(None, 28)

while running:
    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = px_to_mm(*event.pos)

            # 1. Grab the closest ball within range, if any
            best = GRAB_RADIUS_MM
            for name, (bx, by) in balls.items():
                d = math.hypot(mx - bx, my - by)
                if d <= best:
                    best = d
                    dragging = name

            # 2. If no ball was grabbed, try to select a pocket
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
            target_name = "blocker" if target_name == "target" else "target"

    # DRAWING
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

    # highlight ring on the selected pocket
    pocket = POCKETS_MM[selected_pocket]
    pygame.draw.circle(screen, (255, 220, 0), mm_to_px(*pocket), pocket_radius_px + 4, 3)

    # which ball are we aiming at, and which one is the obstacle?
    aim_ball = balls[target_name]
    obstacle_name = "blocker" if target_name == "target" else "target"
    obstacle = balls[obstacle_name]

    # recompute the ghost ball every frame from the current state
    try:
        ghost = ghost_ball_position(aim_ball, pocket, BALL_RADIUS_MM)
    except ValueError:
        ghost = None  # aimed ball is exactly on the pocket centre

    # aiming lines (drawn BEFORE the balls so the balls sit on top)
    pygame.draw.line(screen, (255, 220, 0),
                     mm_to_px(*aim_ball), mm_to_px(*pocket), 2)
    shot_ok = False
    if ghost is not None:
        shot_ok = is_straight_shot_possible(balls["cue"], ghost, aim_ball, pocket)
        line_colour = (220, 220, 220) if shot_ok else (220, 50, 50)
        pygame.draw.line(screen, line_colour,
                         mm_to_px(*balls["cue"]), mm_to_px(*ghost), 2)

    # real balls
    ball_radius_px = round(BALL_RADIUS_MM * SCALE)
    pygame.draw.circle(screen, (255, 255, 255), mm_to_px(*balls["cue"]), ball_radius_px)
    pygame.draw.circle(screen, (200, 30, 30), mm_to_px(*balls["target"]), ball_radius_px)
    pygame.draw.circle(screen, (230, 200, 0), mm_to_px(*balls["blocker"]), ball_radius_px)

    # ring around the ball we're aiming at
    pygame.draw.circle(screen, (255, 220, 0), mm_to_px(*aim_ball), ball_radius_px + 1 , 2)

    # ghost ball: outline only, so it reads as imaginary
    if ghost is not None:
        pygame.draw.circle(screen, (255, 255, 255), mm_to_px(*ghost), ball_radius_px, 2)

    # warnings, stacked down the screen
    messages = []
    if ghost is not None:
        if not shot_ok:
            messages.append("Straight shot not possible")
        if path_blocked(balls["cue"], ghost, [obstacle], BALL_RADIUS_MM):
            messages.append("Cue ball path is blocked")
        if path_blocked(aim_ball, pocket, [obstacle], BALL_RADIUS_MM):
            messages.append("Target ball's path to the pocket is blocked")

    for i, msg in enumerate(messages):
        text = font.render(msg, True, (255, 120, 120))
        screen.blit(text, (20, 10 + i * 26))

    hint = font.render("T: switch aimed ball", True, (200, 200, 200))
    screen.blit(hint, (20, WINDOW_H - 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
