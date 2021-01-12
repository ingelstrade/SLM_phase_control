import tkinter as tk
from tkinter import ttk
import numpy as np
import tkinter.font as tkFont

print('types in')


def types():
    types = ['None', 'Redirection', 'Binary']
    return types


def new_type(frm_mid, typ):
    if typ == 'None':
        type_ref = type_none(frm_mid)
        return type_ref
    elif typ == 'Redirection':
        return type_dir(frm_mid)
    elif typ == 'Binary':
        return type_binary(frm_mid)


class type_none(object):
    """shows no settings for phase"""

    def __init__(self, parent):
        frm_ = tk.Frame(parent)
        frm_.grid(row=0, column=0, sticky='nsew')
        lbl_frm = tk.LabelFrame(frm_, text='')
        lbl_frm.grid(row=0, column=0, sticky='ew')

    def phase(self):
        phase = np.zeros([600, 800])
        return phase


class type_dir(object):
    """shows the settings for redirection"""

    def __init__(self, parent):
        frm_ = tk.Frame(parent)
        frm_.grid(row=0, column=0, sticky='nsew')
        lbl_frm = tk.LabelFrame(frm_, text='Redirection')
        lbl_frm.grid(row=0, column=0, sticky='ew', padx=5, pady=10)

        # Creating objects
        lbl_xdir = tk.Label(lbl_frm, text='Steepness along x-direction:')
        lbl_ydir = tk.Label(lbl_frm, text='Steepness along y-direction:')
        vcmd = (parent.register(self.callback))
        self.ent_xdir = tk.Entry(
            lbl_frm, width=11,  validate='all',
            validatecommand=(vcmd, '%d', '%P', '%S'))
        self.ent_ydir = tk.Entry(
            lbl_frm, width=11,  validate='all',
            validatecommand=(vcmd, '%d', '%P', '%S'))

        # Setting up
        lbl_xdir.grid(row=0, column=0, sticky='e', padx=(10, 0), pady=5)
        lbl_ydir.grid(row=1, column=0, sticky='e', padx=(10, 0), pady=(0, 5))
        self.ent_xdir.grid(row=0, column=1, sticky='w', padx=(0, 10))
        self.ent_ydir.grid(row=1, column=1, sticky='w', padx=(0, 10))

    def callback(self, action, P, text):
        # action=1 -> insert
        if(action == '1'):
            if text in '0123456789.-+':
                try:
                    float(P)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True

    def phase(self):
        xdir = self.ent_xdir.get()
        ydir = self.ent_ydir.get()

        if xdir != '' and float(xdir) != 0:
            phx = np.outer(
                np.ones([600, 1]),
                np.arange(0, float(xdir), float(xdir)/800))
        else:
            phx = np.zeros([600, 800])

        if ydir != '' and float(ydir) != 0:
            phy = np.outer(
                np.arange(0, float(ydir), float(ydir)/600),
                np.ones([1, 800]))
        else:
            phy = np.zeros([600, 800])

        phase = phx + phy
        return phase


class type_binary(object):
    """shows binary settings for phase"""

    def __init__(self, parent):
        frm_ = tk.Frame(parent)
        frm_.grid(row=0, column=0, sticky='nsew')
        lbl_frm = tk.LabelFrame(frm_, text='Binary')
        lbl_frm.grid(row=0, column=0, sticky='ew', padx=5, pady=10)

        # Creating entities
        lbl_dir = tk.Label(lbl_frm, text='Direction for split:')
        lbl_rat = tk.Label(lbl_frm, text='Area amount (in %):')
        lbl_phi = tk.Label(lbl_frm, text='Phase change (in pi):')
        self.cbx_dir = ttk.Combobox(
            lbl_frm,
            values=['Horizontal', 'Vertical'],
            state='readonly',
            width=10)
        self.ent_area = tk.Spinbox(lbl_frm, width=12, from_=0, to=100)
        vcmd = (parent.register(self.callback))
        self.ent_phi = tk.Entry(lbl_frm, width=12,  validate='all',
                                validatecommand=(vcmd, '%d', '%P', '%S'))

        # Setting up
        lbl_dir.grid(row=0, column=0, sticky='e', padx=(10, 0), pady=5)
        lbl_rat.grid(row=1, column=0, sticky='e', padx=(10, 0))
        lbl_phi.grid(row=2, column=0, sticky='e', padx=(10, 0), pady=5)
        self.cbx_dir.grid(row=0, column=1, sticky='w', padx=(0, 10))
        self.ent_area.grid(row=1, column=1, sticky='w', padx=(0, 10))
        self.ent_phi.grid(row=2, column=1, sticky='w', padx=(0, 10))

    def callback(self, action, P, text):
        # action=1 -> insert
        if(action == '1'):
            if text in '0123456789.-+':
                try:
                    float(P)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True

    def phase(self):
        direc = self.cbx_dir.get()
        if self.ent_area.get() != '':
            area = float(self.ent_area.get())
        else:
            area = 0
        if self.ent_phi.get() != '':
            phi = float(self.ent_phi.get())
        else:
            phi = 0

        phase_mat = np.zeros([600, 800])

        if direc == 'Horizontal':
            cutpixel = int(round(600*area/100))
            tmp = np.ones([cutpixel, 800])*phi
            phase_mat[0:cutpixel, :] = tmp
        elif direc == 'Vertical':
            cutpixel = int(round(800*area/100))
            tmp = np.ones([600, cutpixel])*phi
            phase_mat[:, 0:cutpixel] = tmp

        return phase_mat
