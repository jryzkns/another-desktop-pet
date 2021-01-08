from os.path import join as pj
from random import randint as ri
import tkinter as tk

STATE_IDLE  = 0
STATE_I2S   = 1
STATE_SLEEP = 2
STATE_S2I   = 3
STATE_WL    = 4
STATE_WR    = 5

class Pet(tk.Tk):

    def __init__(self):

        # SETUP WINDOW
        tk.Tk.__init__(self)
        self.screen_w = self.winfo_screenwidth()
        self.screen_h = self.winfo_screenheight()
        self.config(highlightbackground = 'black')
        self.overrideredirect(True)
        self.wm_attributes(
            '-transparentcolor',    'black',
            "-topmost",             1)
        self.label = tk.Label(self, bd = 0, bg = 'black')
        self.label.pack()

        self.dx, self.dy = 0, 0
        
        # BINDINGS; COULD BIND EXTRA THINGS DOWN THE LINE
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonPress-3>", self.handle_rclick)
        self.bind("<B1-Motion>", self.do_move)

        # PET ATTRIBUTES
        self.x, self.y = 100, 100
        self.state = STATE_S2I  # initial state is waking up
        self.movespeed = 3
        self.event_num = ri(1,3)

        get_frame_buffer = lambda path, n_frames : \
            [tk.PhotoImage(file=path, format = f'gif -index {frame_idx}')
                for frame_idx in range(n_frames)]

        self.anim_idx = 0
        self.anims = {
            STATE_IDLE  : get_frame_buffer(pj("assets", "idle.gif"),  5),
            STATE_I2S   : get_frame_buffer(pj("assets", "i2s.gif"),   8),
            STATE_SLEEP : get_frame_buffer(pj("assets", "sleep.gif"), 3),
            STATE_S2I   : get_frame_buffer(pj("assets", "s2i.gif"),   8),
            STATE_WL    : get_frame_buffer(pj("assets", "wl.gif"),    8),
            STATE_WR    : get_frame_buffer(pj("assets", "wr.gif"),    8)}

        # TODO: what does this do?
        self.first_last = {
            STATE_IDLE  : (1, 10),
            STATE_I2S   : (10, 11),
            STATE_SLEEP : (10, 16),
            STATE_S2I   : (1, 2),
            STATE_WL    : (1, 10),
            STATE_WR    : (1, 10)}

        self.transition_timer = {
            STATE_IDLE  : 400,
            STATE_I2S   : 100,
            STATE_SLEEP : 1000,
            STATE_S2I   : 100,
            STATE_WL    : 100,
            STATE_WR    : 100}

    def validate_xy(self):
        self.x, self.y = \
            0                     if self.x < 0 else \
            self.screen_w - 100   if self.x + 100 > self.screen_w else \
            self.x, \
            0                     if self.y < 0 else \
            self.screen_h - 100   if self.y + 100 > self.screen_h else \
            self.y

    def handle_rclick(self, event): print("bye!"); self.quit()

    def start_move(self, e): self.dx, self.dy = e.x, e.y

    def do_move(self, e):

        dx, dy = e.x - self.dx, e.y - self.dy
        self.x, self.y = self.winfo_x() + dx, self.winfo_y() + dy
        self.validate_xy()
        self.geometry(f"100x100+{self.x}+{self.y}")

    def update(self):

        self.anim_idx = (self.anim_idx + 1) % len(self.anims[self.state])
        self.event_num = ri(*self.first_last[self.state])

        if self.state == STATE_WL: self.x -= self.movespeed
        if self.state == STATE_WR: self.x += self.movespeed

        self.validate_xy()
        self.geometry(f'100x100+{self.x}+{self.y}')
        self.label.configure(image=self.anims[self.state][self.anim_idx])
        self.after(1, self.event)

    def event(self):

        if self.event_num in idle_num:     self.state = STATE_IDLE
        elif self.event_num == 5:          self.state = STATE_I2S
        elif self.event_num in walk_left:  self.state = STATE_WL
        elif self.event_num in walk_right: self.state = STATE_WR
        elif self.event_num in sleep_num:  self.state = STATE_SLEEP
        elif self.event_num == 14:         self.state = STATE_S2I
        self.after(self.transition_timer[self.state], self.update)

idle_num =[1,2,3,4]
sleep_num = [10,11,12,13,15]
walk_left = [6,7]
walk_right = [8,9]

cat = Pet()
cat.after(1, cat.update)
cat.mainloop()
