# snooker-ghost-ball-visualizer
Interactive 2D snooker ghost-ball visualizer built with Python and Pygame. Place the cue ball, target ball and pocket, and see the idealized aiming geometry. Long-term goal: webcam ball detection and AR/projector aim overlay on a real table.



A desktop tool that calculates and draws the **ghost ball** position for
a snooker shot: the spot where the cue ball must be at contact to send a
target ball toward a chosen pocket.

## Status
Work in progress. Currently implemented:
- 2D top-down table with six pockets, drawn from real dimensions (mm)
- Draggable cue and target ball(s)

Planned (not yet built):
- Pocket selection, ghost-ball calculation, aiming lines
- Invalid-shot and obstruction checks
- Saving/loading layouts
- Webcam ball detection (OpenCV)
- Mixed-reality overlay on a real table (needs compatible hardware)

## Limitations
The ghost ball is an ** idealised geometric solution**. It does not
account for spin, speed, throw, cushion effects or pocket jaw shape,
so it doesn't guarantee a successful real-world shot.


TODO: add real table and ball dimentions to the program 
