import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import numpy as np
from tkinter.filedialog import askopenfilename, asksaveasfilename


class main_screen(object):
    """"""

    def __init__(self, parent):
        """Constructor"""
        self.main_win = parent
        self.main_win.title('SLM Phase Control')

        self.main_win.columnconfigure(0, minsize=500, weight=1)
        self.main_win.rowconfigure(2, minsize=400, weight=1)

        # creating frames
        frm_top = tk.Frame(self.main_win)
        self.frm_mid = tk.Frame(self.main_win, relief='sunken')
        frm_bot = tk.Frame(self.main_win)

        # Creating labels
        lbl_title = tk.Label(
            self.main_win,
            text='Control Phase',
            font=tkFont.Font(family='Lucida Grande', size=20))
        lbl_screen = tk.Label(frm_top, text='Screen:')
        lbl_type = tk.Label(frm_top, text='Type:')

        # Creating buttons
        but_prev = tk.Button(frm_bot, text='Preview', command=self.open_prev)
        but_pub = tk.Button(frm_bot, text='Publish', command=self.open_pub)
        but_exit = tk.Button(frm_bot, text='EXIT', command=self.exit_prog)

        # Creating combobox
        cbx_scr = ttk.Combobox(frm_top, value=['None'])
        cbx_scr.current(0)
        self.cbx_type = ttk.Combobox(
            frm_top,
            value=['None'],
            state='readonly',
            postcommand=self.list_of_types)
        self.cbx_type.current(0)
        self.cbx_type.bind('<<ComboboxSelected>>', self.new_type)

        # Setting up general structure
        lbl_title.grid(row=0, column=0, sticky='ew')
        frm_top.grid(row=1, column=0, sticky='ew')
        self.frm_mid.grid(row=2, column=0, sticky='nsew')
        frm_bot.grid(row=3, column=0)

        # Setting up top frame
        lbl_screen.grid(row=0, column=0, sticky='e', padx=10, pady=10)
        cbx_scr.grid(row=0, column=1, sticky='w')
        lbl_type.grid(row=1, column=0, sticky='e', padx=10)
        self.cbx_type.grid(row=1, column=1, sticky='w')

        # Setting up bot frame
        but_prev.grid(row=0, column=0, padx=10, pady=5, ipadx=5)
        but_pub.grid(row=0, column=1, pady=5, ipadx=5)
        but_exit.grid(row=0, column=2, padx=10, pady=5, ipadx=5)

    def open_prev(self):
        self.prev_win = prev_screen(self.main_win)

    def open_pub(self):
        self.pub_win = pub_screen(self.main_win)

    def exit_prog(self):
        self.main_win.destroy()

    # The different types
    def list_of_types(self):
        self.cbx_type['values'] = ['None', 'Redirection']

    def new_type(self, event):
        type = self.cbx_type.get()
        if type == 'None':
            self.type = type_none(self.frm_mid)
            self.main_win.title(type)
        elif type == 'Redirection':
            self.type = type_dir(self.frm_mid)
            self.main_win.title(type)


class type_none(object):
    """shows no settings for phase"""

    def __init__(self, parent):
        lbl_ = tk.Label(
            parent,
            text='',
            font=tkFont.Font(family='Lucida Grande', size=12))

        frm_ = tk.Frame(parent)
        lbl_.grid(row=0, column=0, sticky='ew')
        frm_.grid(row=1, column=0, sticky='nsew')


class type_dir(object):
    """shows the settings for redirection"""

    def __init__(self, parent):
        lbl_dir = tk.Label(
            parent,
            text='Redirection',
            font=tkFont.Font(family='Lucida Grande', size=12))

        # Creating objects
        frm_dir = tk.Frame(parent, relief='ridge')
        lbl_xdir = tk.Label(frm_dir, text='Steepness along x-direction:')
        lbl_ydir = tk.Label(frm_dir, text='Steepness along y-direction:')
        ent_xdir = tk.Entry(frm_dir, width=5)
        ent_ydir = tk.Entry(frm_dir, width=5)

        # Setting up
        lbl_dir.grid(row=0, column=0, sticky='ew')
        frm_dir.grid(row=1, column=0)

        lbl_xdir.grid(row=0, column=0, sticky='e')
        lbl_ydir.grid(row=1, column=0, sticky='e')
        ent_xdir.grid(row=0, column=1, sticky='w')
        ent_ydir.grid(row=1, column=1, sticky='w')


class prev_screen(object):
    """"""

    def __init__(self, parent):
        self.win = tk.Toplevel()
        self.win.geometry('400x300')
        self.win.title('SLM Phase Control - Preview')
        def handler(): return self.on_close_prev()
        btn_close = tk.Button(self.win, text='Close', command=handler)
        btn_close.pack()

    def on_close_prev(self):
        self.win.destroy()


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


root = tk.Tk()

main = main_screen(root)


# Creating other windows
# wind_prev = tk.Toplevel()
# wind_pub = tk.Toplevel()


# Setting up preview window
# wind_prev.geometry('400x300')
# wind_prev.title('Control Phase - Preview')


root.mainloop()
