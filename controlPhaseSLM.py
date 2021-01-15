import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import numpy as np
import phase_settings
import preview_window
import publish_window


class main_screen(object):
    """"""

    def __init__(self, parent):
        """Constructor"""
        self.main_win = parent
        self.main_win.title('SLM Phase Control')

        self.main_win.columnconfigure(0, minsize=250, weight=1)
        self.main_win.rowconfigure(2, minsize=100, weight=1)

        # creating frames
        frm_top = tk.Frame(self.main_win)
        self.frm_mid = tk.Frame(self.main_win)
        frm_bot = tk.Frame(self.main_win)

        # Creating labels
        lbl_title = tk.Label(
            self.main_win,
            text='Control Phase',
            font=tkFont.Font(family='Lucida Grande', size=20))
        lbl_screen = tk.Label(frm_top, text='Screen:')

        # Creating buttons
        but_prev = tk.Button(frm_bot, text='Preview', command=self.open_prev)
        but_pub = tk.Button(frm_bot, text='Publish', command=self.open_pub)
        but_exit = tk.Button(frm_bot, text='EXIT', command=self.exit_prog)

        # Creating combobox
        cbx_scr = ttk.Combobox(frm_top, value=['None'])
        cbx_scr.current(0)

        # Setting up general structure
        lbl_title.grid(row=0, column=0, sticky='ew')
        frm_top.grid(row=1, column=0, sticky='ew')
        self.frm_mid.grid(row=2, column=0, sticky='nsew')
        frm_bot.grid(row=3, column=0)

        # Setting up top frame
        lbl_screen.grid(row=0, column=0, sticky='e', padx=10, pady=10)
        cbx_scr.grid(row=0, column=1, sticky='w')
        self.setup_box(frm_top)  # sets up the checkboxes separately

        # Setting up bot frame
        but_prev.grid(row=0, column=0, padx=10, pady=5, ipadx=5)
        but_pub.grid(row=0, column=1, pady=5, ipadx=5)
        but_exit.grid(row=0, column=2, padx=10, pady=5, ipadx=5)

    def open_prev(self):
        self.prev_win = preview_window.prev_screen(self)

    def open_pub(self):
        self.pub_win = publish_window.pub_screen(self)

    def setup_box(self, frm_):
        frm_box = tk.LabelFrame(frm_, text='Phases enabled')
        frm_box.grid(column=1)
        types = phase_settings.types()  # reads in the different phase types
        self.vars = []  # init a list holding the variables from the boxes
        self.phase_refs = []  # init a list to hold the references to types
        self.active_phases = []
        commands = [self.ss_bg, self.ss_dir, self.ss_bi]
        for ind, typ in enumerate(types):
            self.var_ = (tk.IntVar())
            self.vars.append(self.var_)
            self.phase_refs.append(0)  # just filling it with 0 to start with
            self.box_ = tk.Checkbutton(frm_box, text=typ,
                                       variable=self.vars[ind],
                                       onvalue=1, offvalue=0,
                                       command=commands[ind])
            self.box_.grid(row=ind, sticky='w')

    def ss_bg(self):
        self.start_stop_t(0, 'Background')

    def ss_dir(self):
        self.start_stop_t(1, 'Redirection')

    def ss_bi(self):
        self.start_stop_t(2, 'Binary')

    def start_stop_t(self, ind, typ):
        if self.vars[ind].get() == 1:
            self.phase_refs[ind] = phase_settings.new_type(self.frm_mid, typ)
            self.active_phases.append(self.phase_refs[ind])
        else:
            if self.phase_refs[ind] != 0:
                self.phase_refs[ind].close_()
                self.active_phases.remove(self.phase_refs[ind])
            self.phase_refs[ind] = 0

#   gets the phase from the active phase types. 0-2pi is 0-254
    def get_phase(self):
        phase = np.zeros([600, 792])
        for phase_types in self.active_phases:
            phase += phase_types.phase()
        return phase

    def exit_prog(self):
        self.main_win.destroy()


root = tk.Tk()

main = main_screen(root)


root.mainloop()
