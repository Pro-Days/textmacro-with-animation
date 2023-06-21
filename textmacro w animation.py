import json
from math import sin, cos
from math import pi as math_pi
import os
from threading import Thread as lb_thread
import time
import tkinter as tk
from webbrowser import open_new

import clipboard
import pyautogui
import pyperclip
from keyboard import is_pressed as kip
from keyboard import read_key as krk
from requests import get as rq_get


def version_check():
    try:
        response = rq_get(
            "https://api.github.com/repos/pro-days/textmacro-with-animation/releases/latest"
        )
        checked_version = response.json()["name"]
        if response.status_code == 200:
            if version == checked_version:
                update_label.config(text="최신버전 O", fg="green")
            else:
                update_url = response.json()["html_url"]
                update_label.bind("<Button-1>", lambda event: open_new(update_url))
                update_label.config(text="최신버전 X", fg="red")
        else:
            update_label.config(text="업데이트 확인 실패", fg="red")
    except:
        update_label.config(text="업데이트 확인 실패", fg="red")


def open_circle():
    global state, root, textlist_name
    state = "opening_circle"
    if frame != 0:
        for x in range(frame):
            t = x / frame
            t = -2 * t**3 + 3 * t**2
            for i in range(8):
                canvas.moveto(
                    SubC[i],
                    cx + 2.5 * cr * sin(pi * t * i / 4) - sr,
                    cy - 2.5 * cr * cos(pi * t * i / 4) - sr,
                )
            root[-1].update()
            time.sleep(delay)
    else:
        pass
    for i in range(8):
        canvas.moveto(
            SubC[i],
            cx + 2.5 * cr * sin(pi * i / 4) - sr,
            cy - 2.5 * cr * cos(pi * i / 4) - sr,
        )
    root[-1].update()
    state = "open_circle"

    textlist_name = [
        tk.Label(
            canvas,
            text=i,
            fg="#303030",
            # relief="solid",
            bg=colors[i],
            font=("맑은 고딕", 10, "bold"),
        )
        for i in range(8)
    ]

    for i in range(8):
        rgb = colors[i].replace("#", "")

        rgb = (int(rgb[:2], 16), int(rgb[2:4], 16), int(rgb[4:], 16))
        brightness = calculate_brightness(rgb)
        if brightness >= 0.5:
            textlist_name[i].config(fg="#303030")
        else:
            textlist_name[i].config(fg="#ffffff")

    names = dataload("name")

    for i, j in enumerate(textlist_name):
        j.config(text=names[i])
        j.bind(
            "<Button-1>",
            lambda event, n=i: open_menu(n) if state == "open_circle" else None,
        )
        j.place(
            width=sr,
            height=sr,
            x=(cx + 2.5 * cr * sin(pi * i / 4) - sr * 0.5),
            y=(cy - 2.5 * cr * cos(pi * i / 4) - sr * 0.5),
        )


def open_menu(n):
    # print(n)
    global state, lcanvas, root, textlist_name, lc_w, lc_h
    state = "opening_menu"
    # print(n)
    # print(lcanvas)

    for i, j in enumerate(textlist_name):
        j.destroy() if i != n else None
    # print(textlist_name)

    lc_w = round((fw - 13 * sr) * 0.04) * 25
    lc_h = round((fh - 6 * sr) * 0.04) * 25
    # print("frame")

    lcanvas = tk.Canvas(root[-1])
    lcanvas.place(x=10 * sr, y=3 * sr, width=0, height=0)

    for i in range(8):
        canvas.tag_raise(SubC[i])
    canvas.tag_raise(SubC[n])
    # canvas.lower(lcanvas)
    # canvas.itemconfig(SubC[7 - n], fill="red")
    # print(root)

    # root[-1].lower(lcanvas)
    # print("b")
    # root[-1].lift(canvas)

    count = 10
    textt_w = round(lc_w * 0.1)
    textc_w = round(lc_w * 0.9)
    text_h = round(lc_h * 0.1)

    textlist_title = [
        tk.Label(
            lcanvas,
            text=i,
            fg="gray",
            relief="solid",
            font=("맑은 고딕", 20, "bold"),
        )
        for i in range(count)
    ]
    textlist_content = [
        tk.Label(
            lcanvas,
            text=i,
            fg="gray",
            relief="solid",
            font=("맑은 고딕", 20, "bold"),
        )
        for i in range(count)
    ]

    global ready
    ready = False

    ans = dataload("ans", n)

    for i, j in enumerate(textlist_title):
        j.config(text=i)
        j.bind(
            "<Button-1>",
            lambda event, c=textlist_content, i=i: print_text(c, i)
            if state == "open_menu"
            else None,
        )

        j.place(width=textt_w, height=text_h, x=0, y=text_h * i)

    for i, j in enumerate(textlist_content):
        j.config(text=ans[i])
        j.bind(
            "<Double-Button-1>",
            lambda event, j=j, i=i, x=textt_w, y=text_h, n=n: edit_text(
                i, j, x, y, n, ans
            )
            if state == "open_menu"
            else None,
        )

        j.place(width=textc_w, height=text_h, x=textt_w, y=text_h * i)
    ready = True

    # textbar = canvas.create_rectangle(10 * sr, 3 * sr, 10 * sr, 3 * sr, fill=gray_color)
    if frame != 0:
        sr4 = 4 * sr
        sr05 = 0.5 * sr
        cysr = cy - sr
        srcr = 5 * sr - cr
        cxsr = cx - 5 * sr
        for x in range(frame - 1, -1, -1):
            t = precalc_menu[x][0][2]
            cxsrt = cxsr * t
            for i in range(8):
                moveto_x = sr4 - cr * precalc_menu[x][i][0] + cxsrt
                moveto_y = cysr - cr * precalc_menu[x][i][1]
                canvas.moveto(
                    SubC[i],
                    moveto_x,
                    moveto_y,
                )
                if i == n:
                    textlist_name[i].place(
                        x=moveto_x + sr05,
                        y=moveto_y + sr05,
                    )
            canvas.moveto(CenterC, srcr + cxsrt)

            lcanvas.place(
                width=lc_w * (1 - t),
                height=lc_h * (1 - t),
            )
            root[-1].update()

            time.sleep(delay)
    else:
        pass
    for i in range(1, 9):
        canvas.moveto(
            SubC[i - 1],
            4 * sr,
            cy - 2.5 * cr - sr,
        )
    canvas.moveto(CenterC, 5 * sr - cr, cy - cr)
    textlist_name[n].place(
        x=(4.5 * sr),
        y=(cy - 2.5 * cr - sr * 0.5),
    )

    lcanvas.place(
        x=10 * sr,
        y=3 * sr,
        width=lc_w,
        height=lc_h,
    )
    root[-1].update()
    # print(lc_w, lc_h)
    # 10sr ~ fw - 3sr => fw - 13sr
    # print("frame")
    # textlist = []

    # scrollbar = tk.Scrollbar(lcanvas, command=lcanvas.yview, orient=tk.VERTICAL)
    # scrollbar.pack(side="right", fill="both")
    # lcanvas.configure(yscrollcommand=scrollbar.set)

    textlist_name[n].bind(
        "<Button-1>",
        lambda event, n=n: close_menu(n) if state == "open_menu" else None,
    )

    for i in range(8):
        canvas.tag_bind(
            SubC[i],
            "<Button-1>",
            lambda event, n=n: close_menu(n) if state == "open_menu" else None,
        )

    state = "open_menu"


def close_menu(n):
    # print(n)
    global state, lcanvas, root, textlist_name, lc_w, lc_h
    state = "closing_menu"

    lc_w = round((fw - 13 * sr) * 0.04) * 25
    lc_h = round((fh - 6 * sr) * 0.04) * 25
    # time.sleep(delay * 100)
    # textbar = canvas.create_rectangle(10 * sr, 3 * sr, 10 * sr, 3 * sr, fill=gray_color)
    if frame != 0:
        # print("frame")
        sr4 = 4 * sr
        sr05 = 0.5 * sr
        cysr = cy - sr
        srcr = 5 * sr - cr
        for x in range(frame):
            t = precalc_menu[x][0][2]
            cxsrt = (cx - 5 * sr) * t
            for i in range(8):
                moveto_x = sr4 - cr * precalc_menu[x][i][0] + cxsrt
                moveto_y = cysr - cr * precalc_menu[x][i][1]
                canvas.moveto(
                    SubC[i],
                    moveto_x,
                    moveto_y,
                )
                if i == n:
                    textlist_name[i].place(
                        x=moveto_x + sr05,
                        y=moveto_y + sr05,
                    )
            canvas.moveto(CenterC, srcr + cxsrt)

            lcanvas.place(
                width=lc_w * (1 - t),
                height=lc_h * (1 - t),
            )

            root[-1].update()
            time.sleep(delay)
    else:
        pass
    for i in range(8):
        canvas.moveto(
            SubC[i],
            cx + 2.5 * cr * sin(pi * i / 4) - sr,
            cy - 2.5 * cr * cos(pi * i / 4) - sr,
        )
    canvas.moveto(CenterC, -cr + cx, cy - cr)
    root[-1].update()

    lcanvas.destroy()
    textlist_name[n].destroy()
    for i in range(8):
        canvas.tag_bind(
            SubC[i],
            "<Button-1>",
            lambda event, n=i: open_menu(n)
            if state == "open_circle" and not naming
            else None,
        )

    textlist_name = [
        tk.Label(
            canvas,
            text=i,
            fg="#303030",
            # relief="solid",
            bg=colors[i],
            font=("맑은 고딕", 10, "bold"),
        )
        for i in range(8)
    ]

    for i in range(8):
        rgb = colors[i].replace("#", "")

        rgb = (int(rgb[:2], 16), int(rgb[2:4], 16), int(rgb[4:], 16))
        brightness = calculate_brightness(rgb)
        if brightness >= 0.5:
            textlist_name[i].config(fg="#303030")
        else:
            textlist_name[i].config(fg="#ffffff")

    for i in range(8):
        canvas.itemconfig(SubC[i], fill=colors[i])
        textlist_name[i].config(bg=colors[i])

    names = dataload("name")

    for i, j in enumerate(textlist_name):
        j.config(text=names[i])
        j.bind(
            "<Button-1>",
            lambda event, n=i: open_menu(n) if state == "open_circle" else None,
        )
        j.place(
            width=sr,
            height=sr,
            x=(cx + 2.5 * cr * sin(pi * i / 4) - sr * 0.5),
            y=(cy - 2.5 * cr * cos(pi * i / 4) - sr * 0.5),
        )

    state = "open_circle"


def setup():
    global root, fw, fh, fl, ft, fr, fb, canvas, cx, cy, cr, sr, sc_y, frame, CenterC, SubC, fore, delay, lcanvas

    fore = pyautogui.getActiveWindow()  # type: ignore
    fw, fh, fl, ft, fr, fb = (
        fore.size.width,
        fore.size.height,
        fore.left,
        fore.top,
        fore.right,
        fore.bottom,
    )

    root.append(tk.Tk())
    root[-1].geometry(f"{fw}x{fh}+{fl}+{ft}")
    root[-1].wm_attributes("-transparentcolor", "#fffffe")
    root[-1].wm_attributes("-topmost", 1)
    root[-1].attributes("-alpha", 0.75)
    root[-1].overrideredirect(True)

    cx = fw * 0.5
    cy = fh * 0.5
    cr = fw * 0.05
    sr = cr * 0.5

    # print(lcanvas)

    canvas = tk.Canvas(
        root[-1], width=fw, height=fh, bg="#fffffe", bd=0, highlightthickness=0
    )

    canvas.pack()

    CenterC = canvas.create_oval(cx - cr, cy - cr, cx + cr, cy + cr, fill=gray_color)
    canvas.tag_bind(
        CenterC,
        "<Double-Button-1>",
        lambda event: edit_name_onoff(),
    )

    sc_y = cy - cr - 3 * sr

    SubC = []

    for i in range(8):
        SubC.append(
            canvas.create_oval(cx - sr, sc_y - sr, cx + sr, sc_y + sr, fill=colors[i])
        )
        canvas.tag_bind(
            SubC[-1],
            "<Button-1>",
            lambda event, n=i: open_menu(n)
            if state == "open_circle" and not naming
            else None,
        )
        # canvas.tag_bind(
        #     SubC[-1],
        #     "<Button-1>",
        #     lambda event, n=i - 1: threading.Thread(target=open_menu, args=[n]).start()
        #     if state == "open_circle"
        #     else None,
        # )
        # canvas.tag_bind(
        #     SubC[-1],
        #     "<Button-1>",
        #     lambda event, n=i - 1: threading.Thread(target=open_menu, args=[n]).start()
        #     if state == "open_circle"
        #     else None,
        # )

    # https://www.figma.com/file/jw0nKJKBxyUwgF7i1bSDNn/Untitled?node-id=1-105&t=bU9TFem7HstFPAHs-0
    global combobox_anspeed
    delay = 0.016
    # print(frame)

    open_circle()

    root[-1].mainloop()


def kbinput():
    global state
    while startkey_stored:
        # print("111")
        if kip(start_key):
            # print("123")
            if state == "window":
                lb_thread(target=setup, daemon=True).start()
            # elif state == "open_circle":
            #     threading.Thread(target=open_menu, daemon=True, args=n).start()
            time.sleep(0.2)
        time.sleep(0.05)


# def framecount():
#     global frame
#     while True:
#         frame = (
#             round(90 / int(combobox_anspeed.get()))
#             if combobox_anspeed.get() != "x"
#             else 0
#         )
#         time.sleep(0.2)


def edit_name_onoff():
    global naming, textlist_name, editing_name
    if state == "open_circle" and not editing_name:
        if naming:
            naming = False
            canvas.itemconfig(CenterC, fill=gray_color)

            for i, j in enumerate(textlist_name):
                j.bind(
                    "<Button-1>",
                    lambda event, n=i: open_menu(n) if state == "open_circle" else None,
                )
        else:
            naming = True
            canvas.itemconfig(CenterC, fill="#A0B0FF")

            for i, j in enumerate(textlist_name):
                j.bind(
                    "<Button-1>",
                    lambda event, i=i, j=j: edit_name(i, j)
                    if state == "open_circle"
                    else None,
                )
    else:
        pass


def print_text(c, i):
    global root, state
    if ready:
        fore.activate()
        pre = clipboard.paste()
        pyperclip.copy(c[i].cget("text"))

        pyautogui.hotkey("ctrl", "v")
        pyperclip.copy(pre)
        # threading.Thread(target=write_text, args=[c[i].cget("text")]).start()
        # pyautogui.write(c[i].cget("text"), interval=0)
        # print(c[i].cget("text"))
        root[-1].destroy()
        state = "window"


def write_text(text):
    pyautogui.write(text, interval=0.01)
    global state, temp, thread_key
    state = "window"
    # print(state)
    # window.destroy()


def edit_name(i, j):
    global editing_name
    editing_name = True
    text = j.cget("text")

    editing_ent = tk.Entry(
        canvas,
        fg="gray",
        relief="solid",
        bg="#f0f0f0",
        font=("맑은 고딕", 10, "bold"),
    )
    editing_ent.place(
        width=j.winfo_width(), height=j.winfo_height(), x=j.winfo_x(), y=j.winfo_y()
    )
    editing_ent.insert(0, text)
    editing_ent.bind(
        "<Return>",
        lambda event, i=i, j=j, ent=editing_ent: saveNameEntryValue(i, j, ent),
    )


def saveNameEntryValue(i, j, ent):
    global editing_name
    names = dataload("name")
    names[i] = ent.get()
    datasave(names, type="names")
    # print("destroy", ent.get())
    j.config(text=ent.get())
    ent.destroy()
    editing_name = False


def edit_text(i, j, x, y, n, ans):
    if ready:
        text = j.cget("text")

        editing_ent = tk.Entry(
            lcanvas,
            fg="gray",
            relief="solid",
            bg="#f0f0f0",
            font=("맑은 고딕", 20, "bold"),
        )
        editing_ent.place(width=j.winfo_width(), height=j.winfo_height(), x=x, y=y * i)
        editing_ent.insert(0, text)
        editing_ent.bind(
            "<Return>",
            lambda event, i=i, j=j, ent=editing_ent, ans=ans: saveEntryValue(
                i, j, ent, n, ans
            ),
        )


def saveEntryValue(i, j, ent, n, ans: list):
    ans[i] = ent.get()
    datasave(ans, type="ans", n=n)
    # print("destroy", ent.get())
    j.config(text=ent.get())
    ent.destroy()


def dataload(type, n=0) -> list:
    if os.path.isfile(file):
        try:
            with open(file, "r") as f:
                json_object = json.load(f)

                ans = json_object["Ans"][str(n)]
                speed = json_object["speed"]
                start_key = json_object["start_key"]
                names = json_object["Names"]
                colors = json_object["colors"]
        except:
            ans = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
            speed = 0
            start_key = "f9"
            names = ["1", "2", "3", "4", "5", "6", "7", "8"]
            colors = [
                "#ff6961",
                "#ffb480",
                "#f8f38d",
                "#42d6a4",
                "#08cad1",
                "#59adf6",
                "#9d94ff",
                "#c780e8",
            ]
            datamake()
    else:
        ans = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        speed = 0
        start_key = "f9"
        names = ["1", "2", "3", "4", "5", "6", "7", "8"]
        colors = [
            "#ff6961",
            "#ffb480",
            "#f8f38d",
            "#42d6a4",
            "#08cad1",
            "#59adf6",
            "#9d94ff",
            "#c780e8",
        ]
        datamake()
    if type == "ans":
        return ans
    elif type == "start_key":
        return start_key
    elif type == "speed":
        return speed
    elif type == "name":
        return names
    elif type == "colors":
        return colors
    else:
        return None


def datasave(savedata: list, type: str, n=0):
    with open(file, "r") as f:
        json_object = json.load(f)

    if type == "ans":
        json_object["Ans"][str(n)] = savedata
    elif type == "names":
        json_object["Names"] = savedata

    with open(file, "w") as f:
        json.dump(json_object, f)


def datamake():
    json_object = {
        "Ans": {
            "0": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
            "1": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
            "2": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
            "3": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
            "4": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
            "5": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
            "6": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
            "7": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
        },
        "speed": 2,
        "start_key": "f9",
        "Names": ["1", "2", "3", "4", "5", "6", "7", "8"],
        "colors": [
            "#ff6961",
            "#ffb480",
            "#f8f38d",
            "#42d6a4",
            "#08cad1",
            "#59adf6",
            "#9d94ff",
            "#c780e8",
        ],
    }
    if not os.path.isdir("C:\\ProDays"):
        os.mkdir("C:\\ProDays")
    with open(file, "w") as f:
        json.dump(json_object, f)


def saveall():
    global combobox_anspeed
    speed = combobox_anspeed.get()
    speed = int(speed) - 1 if speed != "x" else 5

    colors = [colors_var[i].get() for i in range(8)]
    with open(file, "r") as f:
        json_object = json.load(f)

    json_object["speed"] = speed
    json_object["colors"] = colors

    with open(file, "w") as f:
        json.dump(json_object, f)


def store_startkey():
    global start_key, startkey_stored
    startkey_stored = False
    start_key = krk()

    with open(file, "r") as f:
        json_object = json.load(f)
    json_object["start_key"] = start_key

    with open(file, "w") as f:
        json.dump(json_object, f)

    time.sleep(0.2)
    startkey_stored = True
    thread_key = lb_thread(target=kbinput, daemon=True)
    thread_key.start()
    startkey_button.config(text=start_key)


def rt_colorchange(i, j):
    global colors
    try:
        j.configure(fg=colors_var[i].get())
        # print(colors_var[i].get())

        rgb = str(colors_var[i].get()).replace("#", "")

        rgb = (int(rgb[:2], 16), int(rgb[2:4], 16), int(rgb[4:], 16))
        brightness = calculate_brightness(rgb)
        # print(brightness)
        if brightness >= 0.5:
            j.configure(bg="#303030")
            try:
                textlist_name[i].config(fg="#303030")
            except:
                pass
        else:
            j.configure(bg="#ffffff")
            try:
                textlist_name[i].config(fg="#ffffff")
            except:
                pass
        # print("pass1")

        colors = [colors_var[i].get() for i in range(8)]

        # if state == ("open_circle" or "open_menu"):
        try:
            for i in range(8):
                canvas.itemconfig(SubC[i], fill=colors[i])
            # print(1)
        except:
            pass

        for i in range(8):
            try:
                textlist_name[i].config(bg=colors[i])
                # print(1)
            except:
                pass
    except:
        j.configure(fg="#303030")
        j.configure(bg="#ffffff")


def calculate_brightness(rgb):
    r_weight = 0.299
    g_weight = 0.587
    b_weight = 0.114

    brightness = (rgb[0] * r_weight + rgb[1] * g_weight + rgb[2] * b_weight) / 255

    return brightness


def calc_sct(event):
    global precalc_menu, frame
    precalc_menu = []
    frame = (
        round(90 / int(combobox_anspeed.get())) if combobox_anspeed.get() != "x" else 0
    )
    for x in range(frame):
        t = -2 * (x / frame) ** 3 + 3 * (x / frame) ** 2

        menu_i = []
        for i in range(8):
            menu_i.append(
                [
                    2.5 * sin(pi * t * (8 - i) / 4),
                    2.5 * cos(pi * t * (8 - i) / 4),
                    t,
                ]
            )
        precalc_menu.append(menu_i)


# global window
window = tk.Tk()


window.title("TWA")
window.geometry("400x400+100+100")
window.resizable(False, False)


path = os.path.join(os.path.dirname(__file__), "icon.ico")
if os.path.isfile(path):
    window.iconbitmap(path)


state = "window"
pi = math_pi
ready = False
file = "C:\\ProDays\\PDAnsMacro.json"
root = []
version = "v1.4.0"
naming = False
startkey_stored = True
gray_color = "#d9d9d9"
start_key = dataload("start_key")
editing_name = False

thread_key = lb_thread(target=kbinput, daemon=True)
thread_key.start()


frame_navigator = tk.Frame(window, width=400, height=45)
frame_navigator.pack_propagate(False)
frame_navigator.pack()

# 업데이트 체크
frame_update = tk.Frame(frame_navigator, width=200, height=45)
frame_update.pack_propagate(False)
frame_update.place(x=0, y=0)

update_label = tk.Label(
    frame_update,
    text="업데이트 확인중",
    fg="gray",
    relief="solid",
    font=("맑은 고딕", 12, "bold"),
    width=30,
    height=20,
    borderwidth=1.5,
)
update_label.pack()

thread_version = lb_thread(target=version_check, daemon=True)
thread_version.start()


# 설명 링크
frame_descr = tk.Frame(frame_navigator, width=200, height=45)
frame_descr.pack_propagate(False)
frame_descr.place(x=200, y=0)

descr_label = tk.Label(
    frame_descr,
    text="설명 확인하기",
    fg="blue",
    borderwidth=1.5,
    relief="solid",
    font=("맑은 고딕", 12, "bold"),
    width=30,
    height=20,
)
descr_label.pack()
descr_label.bind(
    "<Button-1>",
    lambda event: open_new(
        "https://github.com/Pro-Days/textmacro-with-animation#readme"
    ),
)


# 애니메이션 속도
frame_anspeedT = tk.Frame(window, width=200, height=50)
frame_anspeedT.pack_propagate(False)
frame_anspeedT.pack(pady=10)

tk.Label(
    frame_anspeedT,
    text="애니메이션 속도",
    fg="black",
    borderwidth=1,
    relief="solid",
    font=("맑은 고딕", 10),
    width=20,
    height=10,
).pack()


frame_anspeedC = tk.Frame(window, width=100, height=50)
frame_anspeedC.pack_propagate(False)
frame_anspeedC.pack(pady=0)

combobox_anspeed = tk.ttk.Combobox(
    frame_anspeedC,
    font=("맑은 고딕", 10),
    values=["1", "2", "3", "4", "5", "x"],
    state="readonly",
    justify="center",
)


frame_startkey = tk.Frame(window, width=251, height=45)
frame_startkey.pack_propagate(False)
frame_startkey.pack(pady=0)

# 시작키설정
frame_startkeyT = tk.Frame(frame_startkey, width=112.5, height=45)
frame_startkeyT.pack_propagate(False)
frame_startkeyT.place(x=0.5, y=0)

tk.Label(
    frame_startkeyT,
    text="시작키설정",
    fg="black",
    borderwidth=1,
    relief="solid",
    font=("맑은 고딕", 10),
    width=20,
    height=10,
).pack()

frame_startkeyK = tk.Frame(frame_startkey, width=112.5, height=45)
frame_startkeyK.pack_propagate(False)
frame_startkeyK.place(x=137.5, y=0)

startkey_button = tk.Button(
    frame_startkeyK,
    text=start_key,
    width=10,
    borderwidth=1,
    relief="solid",
    font=("맑은 고딕", 10),
    bg="white",
    anchor="center",
    command=store_startkey,
)
startkey_button.place(width=112.5, height=45)


speed = dataload("speed")
combobox_anspeed.current(speed)
combobox_anspeed.pack()
combobox_anspeed.bind("<<ComboboxSelected>>", calc_sct)
calc_sct(None)

# thread_frame = threading.Thread(target=framecount, daemon=True)
# thread_frame.start()


frame_colors = tk.Frame(window, width=400, height=80)
frame_colors.pack_propagate(False)
frame_colors.pack(pady=20)

colors_var = [tk.StringVar() for i in range(8)]
colors = dataload("colors")
colors_entry = [
    tk.Entry(
        frame_colors,
        textvariable=colors_var[i],
        fg=colors[i],
        borderwidth=1,
        relief="solid",
        justify="center",
        font=("맑은 고딕", 10),
    )
    for i in range(8)
]

for i, j in enumerate(colors_entry):
    if i < 4:
        j.place(x=i * 100, y=0, width=100, height=40)
    else:
        j.place(x=(i - 4) * 100, y=40, width=100, height=40)
    colors_var[i].set(colors[i])

    rgb = str(colors_var[i].get()).replace("#", "")

    rgb = (int(rgb[:2], 16), int(rgb[2:4], 16), int(rgb[4:], 16))
    brightness = calculate_brightness(rgb)
    if brightness >= 0.5:
        j.configure(bg="#303030")
    else:
        j.configure(bg="#ffffff")

    # colors_var[i].trace("w", lambda a, b, c, i=i: print(i))
    colors_var[i].trace("w", lambda a, b, c, i=i, j=j: rt_colorchange(i, j))


frame_quit = tk.Frame(window, width=100, height=50)
frame_quit.pack_propagate(False)
frame_quit.pack(pady=0)

quit_bt = tk.Button(
    frame_quit,
    text="저장",
    width=100,
    borderwidth=1,
    relief="solid",
    font=("맑은 고딕", 10),
    bg="white",
    anchor="center",
    command=saveall,
)
quit_bt.pack()

window.mainloop()
