import tkinter as tk
import numpy as np
import tkinter.font as tkFont

print('types in')


def types():
    types = ['None', 'Redirection']
    return types


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

    def phase(self):
        phase = np.zeros([600, 800])
        return phase


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
        self.ent_xdir = tk.Entry(frm_dir, width=5)
        self.ent_ydir = tk.Entry(frm_dir, width=5)

        # Setting up
        # lbl_dir.grid(row=0, column=0, sticky='ew')
        frm_dir.grid(row=1, column=0)

        lbl_xdir.grid(row=0, column=0, sticky='e', padx=10, pady=5)
        lbl_ydir.grid(row=1, column=0, sticky='e', padx=10)
        self.ent_xdir.grid(row=0, column=1, sticky='w')
        self.ent_ydir.grid(row=1, column=1, sticky='w')

    def phase(self):
        xdir = self.ent_xdir.get()
        ydir = self.ent_ydir.get()

        if xdir.isnumeric() and float(xdir) != 0:
            phx = np.outer(
                np.ones([600, 1]),
                np.arange(0, float(xdir), float(xdir)/800))
        else:
            phx = np.zeros([600, 800])

        if ydir.isnumeric() and float(ydir) != 0:
            phy = np.outer(
                np.arange(0, float(ydir), float(ydir)/600),
                np.ones([1, 800]))
        else:
            phy = np.zeros([600, 800])

        phase = phx + phy
        return phase
