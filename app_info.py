APP_NAME = "INFO"
ICON_IMAGE = "icon_info.txt"

def load_ui(display, writer):
    writer("HARDWARE METRICS", 60, 30, 2, 0xFFE0)
    writer("CPU: RP2040 DUAL CORE", 15, 100, 2, 0xFFFF)
    writer("FREQ: 133 MHZ SPEED", 15, 150, 2, 0xFFFF)
    writer("RAM: 264 KB SRAM FLUID", 15, 200, 2, 0xFFFF)
    writer("DISPLAY: ST7796S IPS", 15, 250, 2, 0xFFFF)

def handle_touch(x, y, display, writer):
    return False
