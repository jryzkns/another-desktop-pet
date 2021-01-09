from os.path import join
from random import choice
import tkinter as tk

STATE_IDLE  = 0
STATE_I2S   = 1
STATE_SLEEP = 2
STATE_S2I   = 3
STATE_WL    = 4
STATE_WR    = 5

ASSETS_PATH = "assets"

class Pet(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        self.screen_w = self.winfo_screenwidth()
        self.screen_h = self.winfo_screenheight()
        self.config(highlightbackground = 'black')
        self.overrideredirect(True)
        self.wm_attributes(
            '-transparentcolor',  'black',
            "-topmost",           1)
        self.label = tk.Label(self, bd = 0, bg = 'black')
        self.label.pack()

        self.dx, self.dy = 0, 0
        self.dragging = False
        self.holding_rb = False

        self.bind("<ButtonPress-1>",   self.lclick_start)
        self.bind("<ButtonRelease-1>", self.lclick_end)
        self.bind("<B1-Motion>",       self.lclick_hold)
        self.bind("<ButtonPress-3>",   self.rclick_start)
        self.bind("<ButtonRelease-3>", self.rclick_end)
        self.bind("<Key>",             self.handle_key)

        self.x, self.y = 100, 100
        self.state = STATE_SLEEP
        self.movespeed = 3

        gif_buffer = lambda path, n_frames : \
            [tk.PhotoImage(file=path, format = f'gif -index {frame_idx}')
                for frame_idx in range(n_frames)]

        self.anim_buffer, self.update_rate = [], 250 # ms
        self.frames = {
            STATE_IDLE  : gif_buffer(join(ASSETS_PATH, "idle.gif"),  5),
            STATE_I2S   : gif_buffer(join(ASSETS_PATH, "i2s.gif"),   8),
            STATE_SLEEP : gif_buffer(join(ASSETS_PATH, "sleep.gif"), 3),
            STATE_S2I   : gif_buffer(join(ASSETS_PATH, "s2i.gif"),   8),
            STATE_WL    : gif_buffer(join(ASSETS_PATH, "wl.gif"),    8),
            STATE_WR    : gif_buffer(join(ASSETS_PATH, "wr.gif"),    8)}

        self.state_xsition = {
            STATE_IDLE  : [ STATE_IDLE ] * 3 + [ STATE_I2S, STATE_WL, STATE_WR ],
            STATE_I2S   : [ STATE_SLEEP ],
            STATE_SLEEP : [ STATE_SLEEP ] * 4 + [ STATE_S2I ],
            STATE_S2I   : [ STATE_IDLE ],
            STATE_WL    : [ STATE_WL, STATE_WR, STATE_IDLE ],
            STATE_WR    : [ STATE_WL, STATE_WR, STATE_IDLE ]}

    def validate_xy(self):
        self.x, self.y = \
            0                     if self.x < 0 else \
            self.screen_w - 100   if self.x + 100 > self.screen_w else \
            self.x, \
            0                     if self.y < 0 else \
            self.screen_h - 100   if self.y + 100 > self.screen_h else \
            self.y

    def lclick_start (self, e): self.dx, self.dy = e.x, e.y; self.dragging = True
    def lclick_end   (self, e): self.dragging = False
    def lclick_hold  (self, e):
        dx, dy = e.x - self.dx, e.y - self.dy
        self.x, self.y = self.winfo_x() + dx, self.winfo_y() + dy
        self.validate_xy()
        self.geometry(f"100x100+{self.x}+{self.y}")

    def rclick_start (self, event): self.holding_rb = True
    def rclick_end   (self, event): self.holding_rb = False

    def update(self):

        if len(self.anim_buffer) == 0:
            self.state = choice(self.state_xsition[self.state])
            self.anim_buffer += self.frames[self.state]

        if not self.dragging:
            if self.state == STATE_WL: self.x -= self.movespeed
            if self.state == STATE_WR: self.x += self.movespeed

        self.validate_xy()
        self.geometry(f'100x100+{self.x}+{self.y}')

        self.label.configure(image=self.anim_buffer[0])
        self.anim_buffer = self.anim_buffer[1:]

        self.after(self.update_rate, self.update)

    def handle_key(self, event):
        if not self.holding_rb: return
        ch = event.char
        if ch == 'x':
            self.quit()

p = Pet(); p.after(1, p.update); p.mainloop()