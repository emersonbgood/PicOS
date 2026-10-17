APP_NAME = "PAINT"
ICON_COLOR = 0x07FF
ICON_IMAGE = "icon_paint.txt" # Updated to point to your new text file layout!
def load_ui(display, txt):
    # Main.py already cleared the screen to black! Just draw the Save Button.
    # We step the blocks horizontally to build a clean 60x20 green button mesh.
    display.draw_square(240, 430, 20, 0x07E0)
    display.draw_square(260, 430, 20, 0x07E0)
    display.draw_square(280, 430, 20, 0x07E0)
    txt("SAVE", 255, 432, 2, 0xFFFF)

def handle_touch(x, y, display, txt):
    # 1. Check if user clicks the Bottom-Right Save button mesh area
    if 240 <= x <= 310 and 420 <= y <= 480:
        return "HOME"
        
    # 2. Draw continuous Cyan dots anywhere else on the canvas frame space
    # Keep drawing boundaries strictly locked between the status bar and save button zone
    if 25 <= y <= 410:
        display.draw_square(x, y, 4, 0x07FF)
        
    return None
