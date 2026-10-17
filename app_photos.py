import os

APP_NAME = "PHOTOS"
ICON_IMAGE = "icon_photos.txt"
g_idx = 0

def load_ui(display, writer):
    global g_idx
    files = [f for f in os.listdir('/photos') if f.endswith('.txt')]
    writer(f"GALLERY FILES: {len(files)}", 60, 30, 2, 0x780F)
    if not files:
        writer("EMPTY GALLERY", 80, 200, 2, 0x5AEB)
        return
    if g_idx >= len(files): g_idx = 0
    writer(f"VIEW [{g_idx+1}/{len(files)}]:", 15, 95, 2, 0xFFE0)
    
    # Render Prev/Next button boxes
    for o in range(0, 100, 5): display.draw_square(20 + o, 140, 4, 0x5AEB)
    writer("PREV", 45, 150, 2, 0xFFFF)
    for o in range(0, 100, 5): display.draw_square(200 + o, 140, 4, 0x5AEB)
    writer("NEXT", 230, 150, 2, 0xFFFF)
    
    # Internal Viewframe Box Canvas Fill
    for ox in range(10, 310, 5):
        for oy in range(195, 470, 5): display.draw_square(ox, oy, 4, 0x2104)
        
    try:
        with open(f"/photos/{files[g_idx]}", "r") as f:
            for line in f:
                p = line.strip().split(',')
                if len(p) == 2 and 15 <= int(p[0]) <= 305 and 200 <= int(p[1]) <= 465:
                    display.draw_square(int(p[0]), int(p[1]), 4, 0x07FF)
    except: pass

def handle_touch(x, y, display, writer):
    global g_idx
    files = [f for f in os.listdir('/photos') if f.endswith('.txt')]
    if not files: return False
    if 20 <= x <= 120 and 140 <= y <= 175:
        g_idx = (g_idx - 1) % len(files)
        load_ui(display, writer)
        return True
    elif 200 <= x <= 300 and 140 <= y <= 175:
        g_idx = (g_idx + 1) % len(files)
        load_ui(display, writer)
        return True
    return False
