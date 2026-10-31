#TABLE DIMENSINOS AND POCKETS
WINDOW_W = 1280
WINDOW_H = 720
MARGIN = 50
# Table dimensions in millimetres (approximate full-size snooker table)
TABLE_LENGTH_MM = 3569
TABLE_WIDTH_MM = 1778
BALL_DIAMETER_MM = 52.5
BALL_RADIUS_MM = BALL_DIAMETER_MM / 2
POCKET_RADIUS_MM = 45  # rough visual size, not an official measurement

# Drawing settings: how many pixels per millimetre, and where the
# top-left corner of the cloth sits in the window.
SCALE = 0.26
ORIGIN_X = 36
ORIGIN_Y = 49

# Pocket positions in mm, (0, 0) is the top-left corner of the cloth.
POCKETS_MM = [
    (0, 0),
    (TABLE_LENGTH_MM / 2, 0),
    (TABLE_LENGTH_MM, 0),
    (0, TABLE_WIDTH_MM),
    (TABLE_LENGTH_MM / 2, TABLE_WIDTH_MM),
    (TABLE_LENGTH_MM, TABLE_WIDTH_MM),
]


def mm_to_px(x_mm, y_mm):
    """Convert table coordinates (mm) to window coordinates (pixels)."""
    return (round(ORIGIN_X + x_mm * SCALE), round(ORIGIN_Y + y_mm * SCALE))

def px_to_mm(x_px, y_px):
    """ convert window coordinates (pixels) to table coordinates (mm)."""
    return ((x_px - ORIGIN_X) / SCALE, (y_px - ORIGIN_Y) / SCALE)
