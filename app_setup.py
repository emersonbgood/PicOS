import machine as M, os, gc, time as T, waveshare as V
d = V.lcd_st7796()
APP_NAME = "SETTINGS"
ICON_COLOR = 0x7BEF
ICON_IMAGE = "icon_settings.txt"
page = 0
sub_menu = "MAIN"
cfg = {"WIFI": True, "BT": False, "PASS": True, "WALL": True}

def draw_switch(display, x, y, active):
    if active:
        for o in range(0, 40, 20): display.draw_square(x + o, y, 20, 0x07E0)
        display.draw_square(x + 20, y, 20, 0xFFFF)
    else:
        for o in range(0, 40, 20): display.draw_square(x + o, y, 20, 0x7BEF)
        display.draw_square(x, y, 20, 0xFFFF)

def draw_row(display, txt, text, y):
    for o in range(0, 280, 20): display.draw_square(20 + o, y, 20, 0x2104)
    txt(text, 30, y + 12, 2, 0xFFFF)
    txt(">", 280, y + 12, 2, 0x7BEF)

def load_ui(display, txt):
    global page, sub_menu
    d.lcd_fill(0) # Wipes screen instantly at hardware speed to fix the 1-minute lag
    for bx in range(5, 45, 5):
        for by in range(25, 50, 5): display.draw_square(bx, by, 5, 0xF800)
    txt("<", 18, 30, 2, 0xFFFF)
    
    if sub_menu == "MAIN":
        txt("SETTINGS", 60, 30, 2, 0xFFFF)
        display.draw_square(270, 30, 15, 0x07E0)
        display.draw_square(278, 24, 6, 0x07FF)
        if page == 0:
            draw_row(display, txt, "WIRELESS WIFI NETWORK", 70)
            draw_row(display, txt, "BLUETOOTH MESH LE", 130)
            draw_row(display, txt, "SECURITY PASSCODE", 190)
            draw_row(display, txt, "GRADIENT WALLPAPER", 250)
            for o in range(0, 100, 20): display.draw_square(110 + o, 400, 20, 0x5AEB)
            txt("NEXT", 140, 412, 2, 0xFFFF)
        elif page == 1:
            draw_row(display, txt, "STORAGE AND SD CARD", 70)
            draw_row(display, txt, "SYSTEM METRICS (INFO)", 130)
            draw_row(display, txt, "TIME & CLOCK SETUP", 190)
            for o in range(0, 100, 20): display.draw_square(110 + o, 400, 20, 0x5AEB)
            txt("PREV", 140, 412, 2, 0xFFFF)
            
    elif sub_menu in ["WIFI", "BT", "PASS", "WALL"]:
        titles = {"WIFI": "WIFI CFG", "BT": "BLUETOOTH", "PASS": "PASSCODE", "WALL": "WALLPAPER"}
        txt(titles[sub_menu], 60, 30, 2, 0x07FF)
        txt("ENABLE SERVICE", 30, 100, 2, 0xFFFF)
        draw_switch(display, 240, 95, cfg[sub_menu])
        txt("-STYLE OPTIONS MENU ACTIVE", 20, 180, 1, 0x7BEF)
        
    elif sub_menu == "INFO":
        txt("SYSTEM INFO", 60, 30, 2, 0x07FF)
        fs = os.statvfs('/')
        disk_free = (fs * fs) / 1024
        ram_free = gc.mem_free() / 1024
        txt("OS VERSION: PICOOS V3.0", 20, 90, 2, 0xFFFF)
        txt("CHIP ARCH: RP2040 DUAL 32BIT", 20, 130, 2, 0xFFFF)
        txt(f"FREE FLASH: {disk_free:.1f} KB", 20, 170, 2, 0xFFFF)
        txt(f"FREE HEAP: {ram_free:.1f} KB", 20, 210, 2, 0xFFFF)
        txt("SPI BUS: HARDCODED SPI1", 20, 250, 2, 0xFFFF)
        
    elif sub_menu in ["STORAGE", "TIME"]:
        txt(sub_menu + " UTILS", 60, 30, 2, 0xFFFF)
        txt("UTILITY MANAGEMENT ACTIVE", 20, 120, 2, 0x07E0)

def handle_touch(x, y, display, txt):
    global page, sub_menu
    if 5 <= x <= 45 and 25 <= y <= 50:
        if sub_menu != "MAIN":
            sub_menu = "MAIN"; load_ui(display, txt); T.sleep_ms(150); return None
        return "HOME"
        
    if sub_menu == "MAIN":
        if page == 0:
            if 70 <= y <= 110: sub_menu = "WIFI"
            elif 130 <= y <= 170: sub_menu = "BT"
            elif 190 <= y <= 230: sub_menu = "PASS"
            elif 250 <= y <= 290: sub_menu = "WALL"
            elif 390 <= y <= 450 and 100 <= x <= 220: page = 1
            load_ui(display, txt); T.sleep_ms(150)
        elif page == 1:
            if 70 <= y <= 110: sub_menu = "STORAGE"
            elif 130 <= y <= 170: sub_menu = "INFO"
            elif 190 <= y <= 230: sub_menu = "TIME"
            elif 390 <= y <= 450 and 100 <= x <= 220: page = 0
            load_ui(display, txt); T.sleep_ms(150)
            
    elif sub_menu in ["WIFI", "BT", "PASS", "WALL"]:
        if 80 <= y <= 120 and 220 <= x <= 300:
            cfg[sub_menu] = not cfg[sub_menu]
            load_ui(display, txt); T.sleep_ms(150)
            
    return None

