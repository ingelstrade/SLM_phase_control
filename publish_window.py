import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
print('publish_window in')


class pub_screen(object):
    """"""

    def __init__(self, parent):
        self.win = tk.Toplevel()
        self.win.geometry('800x600+500+200')
        # self.win.attributes('-fullscreen', True)
        self.win.title('SLM Phase Control - Publish')
        def handler(event): return self.on_close()
        self.win.bind('<Escape>', handler)
        phase = parent.get_phase()
        img = Image.fromarray(np.uint8(phase))
        img.save('./SLM_phase_control/phase.bmp')
        im = ImageTk.PhotoImage(img)
        print(img)
        print(im)
        lbl_img = tk.Label(self.win, image=im)
        lbl_img.image = im
        lbl_img.pack(fill='both', side=tk.TOP, expand=1)

    def on_close(self):
        self.win.destroy()
