import time
APP_NAME = "CALC"
ICON_IMAGE = "icon_calc.txt"  # Orange

calc_str = ""

def load_ui(display, writer):
    global calc_str
    calc_str = ""
    # Draw simple input register canvas tape
    for ox in range(15, 305, 5):
        for oy in range(65, 115, 5):
            display.draw_square(ox, oy, 4, 0x2104)

    # Build 3x3 simple math numpad blocks grid
    for r in range(3):
        for c in range(3):
            val = str(r * 3 + c + 1)
            kx, ky = 55 + (c * 75), 140 + (r * 60)
            for ox in range(kx, kx + 60, 5):
                for oy in range(ky, ky + 45, 5):
                    display.draw_square(ox, oy, 4, 0x5AEB)
            writer(val, kx + 24, ky + 15, 2, 0xFFFF)

def handle_touch(x, y, display, writer):
    global calc_str
    if 140 <= y <= 320 and 55 <= x <= 280:
        r, c = (y - 140) // 60, (x - 55) // 75
        if 0 <= r < 3 and 0 <= c < 3:
            calc_str += str(r * 3 + c + 1)
            # Re-flush output display area box cleanly
            for ox in range(15, 305, 5):
                for oy in range(65, 115, 5):
                    display.draw_square(ox, oy, 4, 0x2104)
            writer(calc_str, 25, 80, 2, 0xFFFF)
            time.sleep_ms(250)
            return True
    return False
