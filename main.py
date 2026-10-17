import machine as M, time as T, os, waveshare as V, gc
W, B, cc, t_act = False, False, False, False
scr, last_scr, pin, page, gx, gy, active_plugins = "WALLPAPER", "NONE", "", 0, 0, 0, {}
last_touch_time, last_min = T.ticks_ms(), ""
try: import network; w = network.WLAN(network.STA_IF); w.active(True); W = w.isconnected()
except: pass
try: import bluetooth; b = bluetooth.BLE(); b.active(True); B = True
except: pass
f = M.SPI(1, 20000000, polarity=0, phase=0, sck=M.Pin(10), mosi=M.Pin(11), miso=M.Pin(12))
d = V.lcd_st7796(); d.bus = f; d.lcd_init(); t = V.touch_ft6336u(); rtc = M.RTC()
if rtc.datetime()[4:6] == (0, 0): rtc.datetime((2026, 10, 17, 6, 8, 58, 0, 0))
for p in ['/photos', '/notes', '/icons']:
    try: os.mkdir(p)
    except: pass
FONTS = {
    'A':[0x18,0x3C,0x66,0x7E,0x66,0x66,0x66,0x00], 'B':[0x7C,0x66,0x7C,0x66,0x66,0x7C,0x00,0x00], 'C':[0x3C,0x66,0x60,0x60,0x60,0x66,0x3C,0x00], 'D':[0x78,0x6C,0x66,0x66,0x66,0x6C,0x78,0x00],
    'E':[0x7E,0x60,0x7C,0x60,0x60,0x7E,0x00,0x00], 'F':[0x7E,0x60,0x7C,0x60,0x60,0x60,0x00,0x00], 'G':[0x3C,0x66,0x60,0x6E,0x66,0x66,0x3C,0x00], 'H':[0x66,0x66,0x7E,0x66,0x66,0x66,0x66,0x00],
    'I':[0x7E,0x18,0x18,0x18,0x18,0x18,0x7E,0x00], 'J':[0x06,0x06,0x06,0x06,0x66,0x66,0x3C,0x00], 'K':[0x66,0x6C,0x78,0x70,0x78,0x6C,0x66,0x00], 'L':[0x60,0x60,0x60,0x60,0x60,0x7E,0x00,0x00],
    'M':[0x66,0x7E,0x56,0x44,0x44,0x44,0x44,0x00], 'N':[0x66,0x76,0x5E,0x4E,0x46,0x46,0x46,0x00], 'O':[0x3C,0x66,0x66,0x66,0x66,0x66,0x3C,0x00], 'P':[0x7C,0x66,0x66,0x7C,0x60,0x60,0x60,0x00],
    'Q':[0x3C,0x66,0x66,0x66,0x6E,0x3C,0x0E,0x00], 'R':[0x7C,0x66,0x66,0x7C,0x6C,0x66,0x66,0x00], 'S':[0x3C,0x66,0x30,0x18,0x0C,0x66,0x3C,0x00], 'T':[0x7E,0x18,0x18,0x18,0x18,0x18,0x18,0x00],
    'U':[0x66,0x66,0x66,0x66,0x66,0x66,0x3C,0x00], 'V':[0x66,0x66,0x66,0x66,0x66,0x3C,0x18,0x00], 'W':[0x44,0x44,0x44,0x44,0x56,0x7E,0x66,0x00], 'X':[0x66,0x66,0x3C,0x18,0x3C,0x66,0x66,0x00],
    'Y':[0x66,0x66,0x66,0x3C,0x18,0x18,0x18,0x00], 'Z':[0x7E,0x06,0x0C,0x18,0x30,0x60,0x7E,0x00], '0':[0x3C,0x66,0x6E,0x76,0x66,0x66,0x3C,0x00], '1':[0x18,0x38,0x18,0x18,0x18,0x18,0x7E,0x00],
    '2':[0x3C,0x66,0x06,0x0C,0x30,0x60,0x7E,0x00], '3':[0x3C,0x66,0x06,0x1C,0x06,0x66,0x3C,0x00], '4':[0x0C,0x1C,0x3C,0x6C,0x7E,0x0C,0x0C,0x00], '5':[0x7E,0x60,0x7C,0x06,0x06,0x66,0x3C,0x00],
    '6':[0x3C,0x60,0x7C,0x66,0x66,0x66,0x3C,0x00], '7':[0x7E,0x06,0x0C,0x18,0x30,0x30,0x30,0x00], '8':[0x3C,0x66,0x66,0x3C,0x66,0x66,0x3C,0x00], '9':[0x3C,0x66,0x66,0x3E,0x06,0x0C,0x38,0x00],
    ':':[0x00,0x00,0x18,0x18,0x00,0x18,0x18,0x00], ' ':[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00], '<':[0x0C,0x18,0x30,0x60,0x30,0x18,0x0C,0x00], '*':[0x00,0x66,0x3C,0x7E,0x3C,0x66,0x00,0x00]
}
K = [["1","2","3","4","5","6","7","8","9","0"], ["Q","W","E","R","T","Y","U","I","O","P"], ["A","S","D","F","G","H","J","K","L"," "], ["Z","X","C","V","B","N","M",",",".","<="]]
N = [["1","2","3"], ["4","5","6"], ["7","8","9"], ["CLR","0","OK"]]
class DisplayWrapper:
    def __init__(self, draw_func): self.draw_square = draw_func
    def __getattr__(self, name): return self.draw_square
def rect(x1, y1, w, h, col):
    if w > h:
        for o in range(0, w, h): d.draw_square(x1 + o, y1, h, col)
    else:
        for o in range(0, h, w): d.draw_square(x1, y1 + o, w, col)
def txt(s, x, y, z=2, c=0xFFFF):
    cx, cy = x, y
    for h in s.upper():
        if cx + (8 * z) > 310: cx = x; cy += 10 * z
        if h in FONTS:
            for r, row in enumerate(FONTS[h]):
                for g in range(8):
                    if (row >> (7 - g)) & 1: d.draw_square(cx + (g * z), cy + (r * z), z - 1, c)
            cx += 8 * z
        else: cx += 8 * z
def get_live_time(): return f"{rtc.datetime()[4]:02d}:{rtc.datetime()[5]:02d}"
def bar(title="PICO OS"):
    rect(0, 0, 320, 20, 0x5AEB); txt(get_live_time(), 5, 2, 2, 0xFFFF); txt("WIFI" if W else "1H", 240, 2, 2, 0x07E0)
    if scr not in ["HOME", "LOCK", "WALLPAPER"]: rect(5, 25, 40, 25, 0xF800); txt("<", 18, 30, 2, 0xFFFF); txt(title, 60, 30, 2, 0x07FF)
    else: txt(f"{title} P.{page+1}" if scr=="HOME" else title, 15, 30, 2, 0xFFE0)
def scan_and_link_apps():
    global active_plugins; import sys
    for k in list(sys.modules.keys()):
        if k.startswith('app_'): del sys.modules[k]
    active_plugins = {}
    for file in os.listdir('.'):
        if file.startswith('app_') and file.endswith('.py'):
            try: active_plugins[file[:-3]] = __import__(file[:-3])
            except Exception as e: print("Plugin error:", e)
    gc.collect()
def draw_txt_icon(f_name, kx, ky):
    try:
        with open("/icons/" + f_name, "r") as f: lines = f.readlines()
        if not lines: return False
        
        # Parse the dimension header (e.g., "15x15" or "30x30")
        header = lines[0].strip().lower()
        if "x" in header:
            grid_w = int(header.split("x")[0])
            pixel_lines = lines[1:] # Skip header line
        else:
            grid_w = 15 # Fallback to default if header is missing
            pixel_lines = lines
            
        # Dynamically calculate block scaling to fit your 60x60 home screen slots
        scale = 60 // grid_w 
        
        for r_idx, line in enumerate(pixel_lines):
            line = line.strip()
            if not line: continue
            for c_idx in range(0, len(line), 4):
                hx = line[c_idx:c_idx+4]
                if len(hx) < 4: break
                rgb = int(hx, 16); r, g, b = (rgb >> 8) & 0x0F, (rgb >> 4) & 0x0F, rgb & 0x0F
                color_16bit = (((r<<1)|(r>>3)) << 11) | (((g<<2)|(g>>2)) << 5) | ((b<<1)|(b>>3))
                rect(kx + ((c_idx // 4) * scale), ky + (r_idx * scale), scale, scale, color_16bit)
        return True
    except: return False
def draw_wallpaper():
    if last_scr in ["HOME", "WALLPAPER"]: return
    d.lcd_fill(0)
    for y in range(20, 480, 16):
        for x in range(0, 320, 16):
            dist_tl = (x*x + y*y)**0.5; dist_br = ((320-x)**2 + (480-y)**2)**0.5
            if dist_tl < 180: rect(x, y, 16, 16, (int(63 * (1.0 - (dist_tl / 180.0))) & 0x3F) << 5)
            elif dist_br < 180:
                cv = int(31 * (1.0 - (dist_br / 180.0))); rect(x, y, 16, 16, (cv & 0x1F) | ((cv * 2 & 0x3F) << 5))
def l_wallpaper(): global last_scr, last_min; draw_wallpaper(); bar("PICO OS"); last_min = get_live_time(); txt(last_min, 95, 180, 4, 0xFFFF); txt("  SWIPE UP TO       UNLOCK", 50, 400, 2, 0xFFFF); last_scr = "WALLPAPER"
def l_lock():
    global pin, last_scr; d.lcd_fill(0); bar("LOCKED"); pin = ""
    txt("ENTER PASSCODE", 80, 50, 2, 0xFFFF); rect(60, 80, 200, 35, 0x2104)
    for r, row in enumerate(N):
        for c, v in enumerate(row): kx, ky = 50 + (c * 80), 130 + (r * 60); rect(kx, ky, 60, 45, 0x5AEB); txt(v, kx + 15 if len(v) > 1 else kx + 24, ky + 15, 2, 0xFFFF)
    last_scr = "LOCK"
def l_home():
    global last_scr; gc.collect(); draw_wallpaper(); bar("HOME"); apps = sorted(list(active_plugins.items()))
    for idx in range(min(4, len(apps) - (page * 4))):
        m_name, mod = apps[(page * 4) + idx]; kx, ky = 55 + (idx % 2) * 150, 90 + (idx // 2) * 120; img = getattr(mod, 'ICON_IMAGE', '')
        if not img or not draw_txt_icon(img, kx, ky): rect(kx, ky, 60, 60, getattr(mod, 'ICON_COLOR', 0x2104))
        txt(getattr(mod, 'APP_NAME', "APP"), kx + 5, ky + 70, 2, 0xFFFF)
    last_scr = "HOME"
scan_and_link_apps(); l_wallpaper(); dw = DisplayWrapper(d.draw_square)
while True:
    if T.ticks_diff(T.ticks_ms(), last_touch_time) > 60000 and scr != "WALLPAPER": scr, last_scr = "WALLPAPER", "NONE"; l_wallpaper()
    cur_time = get_live_time()
    if scr == "HOME" and not cc and cur_time != last_min: bar("HOME"); last_min = cur_time
    elif scr == "WALLPAPER" and cur_time != last_min: rect(95, 180, 130, 35, 0x0000); txt(cur_time, 95, 180, 4, 0xFFFF); last_min = cur_time
    t.read_touch_data(); coords = t.get_touch_xy()
    if coords is not None:
        last_touch_time = T.ticks_ms()
        for co in coords:
            x, y = co['x'], co['y']
            if not t_act: gx, gy, t_act = x, y, True
            if cc:
                if 50 <= x <= 160 and 240 <= y <= 290: cc = False; l_home() if scr not in ["LOCK", "WALLPAPER"] else (l_wallpaper() if scr == "WALLPAPER" else l_lock()); T.sleep_ms(300)
                elif 170 <= x <= 270 and 240 <= y <= 290: M.reset()
                break
            if scr not in ["HOME", "LOCK", "WALLPAPER"]:
                if 5 <= x <= 45 and 25 <= y <= 50: scr = "HOME"; l_home(); T.sleep_ms(300); break
                if hasattr(active_plugins[scr], 'handle_touch') and active_plugins[scr].handle_touch(x, y, dw, txt) == "HOME": scr = "HOME"; l_home(); T.sleep_ms(300); break
            elif scr == "LOCK":
                if 130 <= y <= 370 and 50 <= x <= 270:
                    r, c = (y - 130) // 60, (x - 50) // 80
                    if 0 <= r < 4 and 0 <= c < 3:
                        v = N[r][c]
                        if v == "CLR": pin = ""
                        elif v == "OK":
                            if pin == "1234": scr = "HOME"; l_home()
                            else: pin = ""; txt("ERROR", 110, 60, 2, 0xF800); T.sleep_ms(600); l_lock()
                        else:
                            if len(pin) < 4: pin += v
                        rect(60, 80, 200, 35, 0x2104); txt("*" * len(pin), 130, 90, 2, 0xFFFF); T.sleep_ms(50)
                        while t.get_touch_xy() is not None: t.read_touch_data(); T.sleep_ms(10)
                        break
            elif scr == "HOME":
                apps = sorted(list(active_plugins.items()))
                for idx in range(min(4, len(apps) - (page * 4))):
                    m_name, mod = apps[(page * 4) + idx]; kx, ky = 55 + (idx % 2) * 150, 90 + (idx // 2) * 120
                    if kx <= x <= kx + 60 and ky <= y <= ky + 60:
                        scr = m_name; d.lcd_fill(0); bar(getattr(mod, 'APP_NAME', "APP"))
                        if hasattr(mod, 'load_ui'): mod.load_ui(dw, txt)
                        T.sleep_ms(300); break
    else:
        if t_act:
            t_act = False
            if scr == "WALLPAPER" and gy - y > 60: scr = "LOCK"; l_lock()
            elif gy > 100 and gy < 380 and scr == "HOME":
                if gx - x > 60 and (page + 1) * 4 < len(active_plugins): page += 1; last_scr = "NONE"; l_home()
                elif x - gx > 60 and page > 0: page -= 1; last_scr = "NONE"; l_home()
            elif gx < 80 and gy > 400: d.lcd_fill(0xFFFF); T.sleep_ms(80); d.lcd_fill(0); l_home() if scr not in ["LOCK", "WALLPAPER"] else (l_wallpaper() if scr == "WALLPAPER" else l_lock())
            elif gx > 240 and gy < 80:
                cc = True; rect(40, 40, 240, 320, 0x2104); txt("CONTROL CENTER", 75, 60, 2, 0x07FF); rect(50, 240, 105, 50, 0xF800); txt("CLOSE", 80, 255, 2, 0xFFFF); rect(165, 240, 105, 50, 0xFD20); txt("REBOOT", 190, 255, 2, 0xFFFF)
    T.sleep_ms(15)