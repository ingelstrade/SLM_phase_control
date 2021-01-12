import tkinter as tk

print('publish_window in')


class pub_screen(object):
    """"""

    def __init__(self, parent):
        self.win = tk.Toplevel()
        self.win.attributes('-fullscreen', True)
        self.win.title('SLM Phase Control - Publish')
        def handler(): return self.on_close_prev()
        btn_close = tk.Button(self.win, text='Close', command=handler)
        btn_close.pack()

    def on_close_prev(self):
        self.win.destroy()
