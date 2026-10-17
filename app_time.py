# app_time.py - PicoOS v3.0 Green Theme Clock Plugin
import machine as M

APP_NAME = "CLOCK"
ICON_IMAGE = "icon_clock.txt"

rtc = M.RTC()

def get_time_string():
    t_data = rtc.datetime()
    return f"{t_data[4]:02d}:{t_data[5]:02d}:{t_data[6]:02d}"

def get_date_string():
    t_data = rtc.datetime()
    return f"{t_data[0]}-{t_data[1]:02d}-{t_data[2]:02d}"

def draw_interface(display, txt):
    # Clear screen frame block using small safe squares
    for space in range(60, 480, 40):
        for bx in range(0, 320, 40):
            display.draw_square(bx, space, 40, 0)
            
    # Draw a custom red back button inside the app so you can leave
    for bx in range(5, 45, 5):
        for by in range(25, 50, 5):
            display.draw_square(bx, by, 5, 0xF800)
    txt("<", 18, 30, 2, 0xFFFF)
    
    # Print the clock interface labels
    txt("REAL TIME CLOCK", 65, 80, 2, 0x07E0)
    txt(get_date_string(), 90, 260, 2, 0x07E0)

def load_ui(display, txt):
    draw_interface(display, txt)
    txt(get_time_string(), 50, 140, 4, 0xFFFF)

def handle_touch(x, y, display, txt):
    # If user taps the red back button area, instantly escape back to home
    if 5 <= x <= 45 and 25 <= y <= 50:
        return "HOME"
        
    # Continuously tick the seconds smoothly
    txt(get_time_string(), 50, 140, 4, 0xFFFF)
    return None
