import urequests as requests
APP_NAME = "STORE"
ICON_IMAGE = "icon_store.txt"
GITHUB_URL = "https://githubusercontent.com"
store_items = []
def load_ui(display, txt):
    global store_items
    display.draw_square(0, 20, 320, 460, 0)
    txt("OS APP STORE", 90, 40, 2, 0xF81F)
    for bx in range(5, 45, 5):
        for by in range(25, 50, 5):
            display.draw_square(bx, by, 5, 0xF800)
    txt("<", 18, 30, 2, 0xFFFF)
    try:
        txt("CONNECTING...", 85, 120, 2, 0xFFFF)
        res = requests.get(GITHUB_URL)
        if res.status_code == 200:
            display.draw_square(85, 120, 160, 0)
            lines = res.text.split("\n")
            store_items = []
            for idx, line in enumerate(lines):
                if "|" in line:
                    parts = line.strip().split("|")
                    if len(parts) == 3:
                        name, icon_url, code_url = parts
                        store_items.append({"name": name, "icon": icon_url, "url": code_url})
                        ry = 90 + (idx * 60)
                        display.draw_square(30, ry, 40, 0x07FF)
                        txt(name.upper(), 90, ry + 10, 2, 0xFFFF)
                        txt("[INSTALL]", 210, ry + 12, 1, 0x07E0)
        res.close()
    except Exception as e:
        print("Network download fail:", e)
        txt("WIFI REQUIREMENT ERROR", 40, 140, 2, 0xF800)
def handle_touch(x, y, display, txt):
    if 5 <= x <= 45 and 25 <= y <= 50:
        return "HOME"
    for idx, item in enumerate(store_items):
        ry = 90 + (idx * 60)
        if ry <= y <= ry + 40:
            txt(f"DOWNLOADING {item['name']}...", 30, 400, 1, 0xFFE0)
            try:
                res = requests.get(item["url"])
                if res.status_code == 200:
                    with open(f"app_{item['name'].lower()}.py", "w") as f:
                        f.write(res.text)
                    txt("INSTALL SUCCESSFUL!", 30, 420, 1, 0x07E0)
                res.close()
            except:
                txt("DOWNLOAD TIMEOUT CRASH", 30, 420, 1, 0xF800)
    return None