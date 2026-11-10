# Snooker Ghost-Ball Visualizer

I own a snooker table and wanted to see where the cue ball needs to be to pot a ball. That spot is the "ghost ball". This is a small Python/Pygame tool that works it out and draws it.

![Ghost ball and aiming lines]
<img width="758" height="710" alt="image" src="https://github.com/user-attachments/assets/31e54bc4-2294-4e11-8e9b-8046e67b2248" />


## What it does

- Draws a top-down table with six pockets, using real dimensions in mm
- Lets you drag the cue ball and two object balls around
- Click a pocket to pick where you're aiming
- Draws the ghost ball and the aiming lines, updated live
- Press `T` to switch which object ball you're aiming at
- Warns you when the cue ball is on the wrong side of the target, or when another ball is in the way

![Impossible shot]
<img width="751" height="712" alt="image" src="https://github.com/user-attachments/assets/a4b00d6a-8fd7-4699-b89b-8a8361108fe8" />
<img width="748" height="707" alt="image" src="https://github.com/user-attachments/assets/4f1043fd-ee10-43a2-861e-174bf37b4858" />


## How the maths works

The cue ball has to hit the target along the line from the pocket through the target's centre. Two touching balls have centres one diameter apart, so the ghost ball sits two radii behind the target, directly away from the pocket. Everything is stored in millimetres and only converted to pixels when drawing.

## Running it

Needs Python 3.12 or newer.


Tests for the maths: `python tests/test_geometry.py`

Table size and ball diameter are at the top of `src/table.py`. They default to approximate full-size values.

## Limitations

This is the idealised geometric answer. It ignores spin, speed, throw, cushions and the real shape of pocket jaws, so a drawn ghost ball doesn't guarantee a pot. I haven't compared it against real shots on my table yet.

## Ideas for later

Bank shots, saving layouts, webcam ball detection with OpenCV, and eventually an AR overlay. None of that is built.
