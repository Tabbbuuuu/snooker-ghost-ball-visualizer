# WINDOW + EVENT LOOP 

import pygame
import math
from table import * 

pygame.init()
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Snooker Ghost-Ball Visualizer")
clock = pygame.time.Clock()

running = True

# dictionary for all the balls
balls = {
    "cue": (TABLE_LENGTH_MM * 0.25, TABLE_WIDTH_MM * 0.5),
    "target": (TABLE_LENGTH_MM * 0.60, TABLE_WIDTH_MM * 0.40),
}

dragging = None # name of ball being dragged, ATM None.
GRAB_RADIUS_MM = BALL_RADIUS_MM * 2 # for a more user friendly forgiving clicking area 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # handeling mouse events 
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my, = px_to_mm(*event.pos)
            for name, (bx, by) in balls.items():
                if math.hypot(mx - bx, my - by) <= GRAB_RADIUS_MM:
                    dragging = name
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = None
            
        elif event.type == pygame.MOUSEMOTION and dragging is not None: 
            balls[dragging] = px_to_mm(*event.pos)

    screen.fill((30, 30, 30))
    
    cloth = pygame.Rect(
                        round(ORIGIN_X), round(ORIGIN_Y),
                        round(TABLE_LENGTH_MM * SCALE), 
                        round(TABLE_WIDTH_MM * SCALE) 
                        )
    
    pygame.draw.rect(screen,  (90,55,30), cloth.inflate(60,60))
    pygame.draw.rect(screen,  (0,100,50), cloth)
    
    # the pockets 
    
    for x_mm, y_mm in POCKETS_MM:
        #convert mm to px 
        center = mm_to_px(x_mm, y_mm)
        radius = round(POCKET_RADIUS_MM * SCALE)
        #draw black filled circles 
        pygame.draw.circle(screen, (0,0,0), center, radius)
    
    
    # balls 
    ball_radius_px = round(BALL_RADIUS_MM * SCALE)
    pygame.draw.circle(screen, (255, 255, 255), mm_to_px(*balls["cue"]), ball_radius_px)
    pygame.draw.circle(screen, (200, 30, 30), mm_to_px(*balls["target"]), ball_radius_px)

    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()