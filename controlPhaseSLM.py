import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import numpy as np
from tkinter.filedialog import askopenfilename, asksaveasfilename
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import types_of_phases
import preview_window
import publish_window


class main_screen(object):
    """"""

    def __init__(self, parent):
        """Constructor"""
        self.main_win = parent
        self.main_win.title('SLM Phase Control')

        self.main_win.columnconfigure(0, minsize=300, weight=1)
        self.main_win.rowconfigure(2, minsize=200, weight=1)

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
        self.type = types_of_phases.type_none(self.frm_mid)

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
        self.prev_win = preview_window.prev_screen(self)

    def open_pub(self):
        self.pub_win = publish_window.pub_screen(self)

    def exit_prog(self):
        self.main_win.destroy()

    # The different types
    def list_of_types(self):
        self.cbx_type['values'] = types_of_phases.types()

    def new_type(self, event):
        type = self.cbx_type.get()
        if type == 'None':
            self.type = types_of_phases.type_none(self.frm_mid)
        elif type == 'Redirection':
            self.type = types_of_phases.type_dir(self.frm_mid)

    def get_type(self):
        return self.type


root = tk.Tk()

main = main_screen(root)


root.mainloop()
