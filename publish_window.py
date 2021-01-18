import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
print('publish_window in')


class pub_screen(object):
    """"""

    def __init__(self, parent, position):
        self.win = tk.Toplevel()
        try:
            self.win.geometry('792x600' + position)
        except tk.TclError:
            self.win.geometry('792x600')
            print('Not correct position')
        # self.win.attributes('-fullscreen', True)
        self.win.overrideredirect(1)
        def handler(event): return self.on_close()
        self.win.bind('<Escape>', handler)
        phase = parent.get_phase()
        img = Image.fromarray(np.uint8(phase))
        img.save('./phase.bmp')
        im = ImageTk.PhotoImage(img)
        lbl_img = tk.Label(self.win, image=im)
        lbl_img.image = im
        lbl_img.pack(fill='both', side=tk.TOP, expand=1)

    def on_close(self):
        self.win.destroy()
