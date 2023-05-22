import pyautogui
import time
import math
import tkinter as tk
import threading
import keyboard
import os
import json


def open_circle():
    global state, root
    state = "opening_circle"
    if a != 0:
        for x in range(a + 1):
            t = x / a
            # t = -20 * t**7 + 70 * t**6 - 84 * t**5 + 35 * t**4
            t = -2 * t**3 + 3 * t**2
            for i in range(1, 9):
                canvas.moveto(
                    SubC[i - 1],
                    cx - 2.5 * cr * math.sin(pi * t * i / 4) - sr,
                    cy - 2.5 * cr * math.cos(pi * t * i / 4) - sr,
                )
            root[-1].update()
            time.sleep(delay)
    else:
        for i in range(1, 9):
            canvas.moveto(
                SubC[i - 1],
                cx - 2.5 * cr * math.sin(pi * i / 4) - sr,
                cy - 2.5 * cr * math.cos(pi * i / 4) - sr,
            )
        root[-1].update()
    state = "open_circle"


def open_menu(n):
    # print(n)
    global state, lcanvas, root
    state = "opening_menu"

    lc_w = round((fw - 13 * sr) * 0.04) * 25
    lc_h = round((fh - 6 * sr) * 0.04) * 25
    # print("a")

    # print(root)
    lcanvas = tk.Canvas(root[-1])
    # print("b")
    lcanvas.place(x=10 * sr, y=3 * sr, width=0, height=0)
    # textbar = canvas.create_rectangle(10 * sr, 3 * sr, 10 * sr, 3 * sr, fill="#D9D9D9")
    if a != 0:
        for x in range(a, -1, -1):
            t = x / a
            # t = -20 * t**7 + 70 * t**6 - 84 * t**5 + 35 * t**4
            t = -2 * t**3 + 3 * t**2
            for i in range(1, 9):
                canvas.moveto(
                    SubC[i - 1],
                    5 * sr
                    - 2.5 * cr * math.sin(pi * t * i / 4)
                    - sr
                    + (cx - 5 * sr) * t,
                    cy - 2.5 * cr * math.cos(pi * t * i / 4) - sr,
                )
            canvas.moveto(CenterC, 5 * sr - cr + (cx - 5 * sr) * t, cy - cr)

            lcanvas.place(
                x=10 * sr,
                y=3 * sr,
                width=lc_w * (1 - t),
                height=lc_h * (1 - t),
            )
            root[-1].update()

            time.sleep(delay)
    else:
        for i in range(1, 9):
            canvas.moveto(
                SubC[i - 1],
                4 * sr,
                cy - 2.5 * cr - sr,
            )
        canvas.moveto(CenterC, 5 * sr - cr, cy - cr)

        lcanvas.place(
            x=10 * sr,
            y=3 * sr,
            width=lc_w,
            height=lc_h,
        )
        root[-1].update()
    # print(lc_w, lc_h)
    # 10sr ~ fw - 3sr => fw - 13sr
    # print("a")
    textlist = []
    for i in range(3):
        text_temp = [
            canvas.create_rectangle(
                10 * sr + 10,
                3 * sr + 10 + 110 * i,
                fw / 4 + 6.75 * sr - 5,
                3 * sr + 100 + 10 + 110 * i,
                fill="#a0a0a0",
            ),
            canvas.create_rectangle(
                fw / 4 + 6.75 * sr + 5,
                3 * sr + 10 + 110 * i,
                fw - 3 * sr - 10,
                3 * sr + 100 + 10 + 110 * i,
                fill="#a0a0a0",
            ),
        ]
        textlist.append(text_temp)

    # scrollbar = tk.Scrollbar(lcanvas, command=lcanvas.yview, orient=tk.VERTICAL)
    # scrollbar.pack(side="right", fill="both")
    # lcanvas.configure(yscrollcommand=scrollbar.set)
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

    ans = dataload(n, "ans")

    for i, j in enumerate(textlist_title):
        j.config(text=i)
        j.bind("<Button-1>", lambda event, c=textlist_content, i=i: print_text(c, i))

        j.place(width=textt_w, height=text_h, x=0, y=text_h * i)

    for i, j in enumerate(textlist_content):
        j.config(text=ans[i])
        j.bind(
            "<Double-Button-1>",
            lambda event, j=j, i=i, x=textt_w, y=text_h, n=n: edit_text(
                i, j, x, y, n, ans
            ),
        )

        j.place(width=textc_w, height=text_h, x=textt_w, y=text_h * i)
    ready = True

    state = "opening_menu"


def setup():
    global root, fw, fh, fl, ft, fr, fb, canvas, cx, cy, cr, sr, sc_y, a, CenterC, SubC, fore, delay

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
    root[-1].wm_attributes("-transparentcolor", "white")
    root[-1].wm_attributes("-topmost", 1)
    root[-1].attributes("-alpha", 0.75)
    root[-1].overrideredirect(True)
    canvas = tk.Canvas(
        root[-1], width=fw, height=fh, bg="white", bd=0, highlightthickness=0
    )

    canvas.pack()

    cx = fw * 0.5
    cy = fh * 0.5
    cr = fw * 0.05
    sr = cr * 0.5

    CenterC = canvas.create_oval(cx - cr, cy - cr, cx + cr, cy + cr)
    canvas.itemconfig(CenterC, fill="#D9D9D9")

    sc_y = cy - cr - 3 * sr

    SubC = []
    for i in range(1, 9):
        SubC.append(canvas.create_oval(cx - sr, sc_y - sr, cx + sr, sc_y + sr))
        canvas.itemconfig(SubC[-1], fill="#D9D9D9")
        canvas.tag_bind(
            SubC[-1],
            "<Button-1>",
            lambda event, n=i - 1: open_menu(n) if state == "open_circle" else None,
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
    a = round(90 / int(combobox_anspeed.get())) if combobox_anspeed.get() != "x" else 0
    delay = 0.0166

    open_circle()

    root[-1].mainloop()


def kbinput():
    global temp
    while True:
        if keyboard.is_pressed("f9"):
            if state == "window":
                threading.Thread(target=setup, daemon=True).start()
            # elif state == "open_circle":
            #     threading.Thread(target=open_menu, daemon=True, args=n).start()
            time.sleep(0.2)
        time.sleep(0.05)


def print_text(c, i):
    global root
    if ready:
        fore.activate()
        threading.Thread(target=write_text, args=[c[i].cget("text")]).start()
        # pyautogui.write(c[i].cget("text"), interval=0)
        # print(c[i].cget("text"))
        root[-1].destroy()


def write_text(text):
    pyautogui.write(text, interval=0.01)
    global state, temp, thread_key
    state = "window"
    # print(state)
    # window.destroy()


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
            lambda event, text=text, i=i, j=j, ent=editing_ent, ans=ans: saveEntryValue(
                i, j, ent, n, ans
            ),
        )


def saveEntryValue(i, j, ent, n, ans: list):
    ans[i] = ent.get()
    datasave(n, ans)
    # print("destroy", ent.get())
    j.config(text=ent.get())
    ent.destroy()


def dataload(n: int, type) -> list:
    if os.path.isfile(file):
        try:
            with open(file, "r") as f:
                json_object = json.load(f)

                ans = json_object["Ans"][str(n)]
                speed = json_object["speed"]
        except:
            ans = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
            speed = 0
            datamake()
    else:
        ans = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        speed = 0
        datamake()
    if type == "ans":
        return ans
    else:
        return speed


def datasave(n: int, ans: list):
    with open(file, "r") as f:
        json_object = json.load(f)

    json_object["Ans"][str(n)] = ans

    with open(file, "w") as f:
        json.dump(json_object, f)


def datamake():
    json_object = {"Ans": {"0": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], "1": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], "2": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], "3": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], "4": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], "5": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], "6": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], "7": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]}, "speed": 0}
    with open(file, "w") as f:
        json.dump(json_object, f)


def exit_window():
    global combobox_anspeed
    speed = combobox_anspeed.get()
    speed = int(speed) - 1 if speed != "x" else 5
    with open(file, "r") as f:
        json_object = json.load(f)

    json_object["speed"] = speed

    with open(file, "w") as f:
        json.dump(json_object, f)

    window.destroy()


thread_key = threading.Thread(target=kbinput, daemon=True)
thread_key.start()

# global window
window = tk.Tk()


window.title("TWA")
window.geometry("300x300+100+100")
window.resizable(False, False)


path = os.path.join(os.path.dirname(__file__), "icon.ico")
if os.path.isfile(path):
    window.iconbitmap(path)


state = "window"
pi = math.pi
ready = False
file = "C:\\ProDays\\PDAnsMacro.json"
# root_num = 0
root = []


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
frame_anspeedC.pack(pady=10)

combobox_anspeed = tk.ttk.Combobox(
    frame_anspeedC,
    font=("맑은 고딕", 10),
    values=["1", "2", "3", "4", "5", "x"],
    state="readonly",
    justify="center",
)

speed = dataload(0, "speed")
combobox_anspeed.current(speed)
combobox_anspeed.pack()
combobox_anspeed.bind("<<ComboboxSelected>>", None)


frame_quit = tk.Frame(window, width=100, height=50)
frame_quit.pack_propagate(False)
frame_quit.pack(pady=40)

quit_bt = tk.Button(
    frame_quit,
    text="QUIT",
    width=100,
    borderwidth=1,
    relief="solid",
    font=("맑은 고딕", 10),
    bg="white",
    anchor="center",
    command=exit_window,
)
quit_bt.pack()


window.mainloop()
