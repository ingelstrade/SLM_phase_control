import tkinter as tk
from tkinter import ttk
import numpy as np
from tkinter.filedialog import askopenfilename
import matplotlib.image as mpimg

print('types in')


def types():
    types = ['Background', 'Redirection', 'Binary']
    return types


def new_type(frm_mid, typ):
    if typ == 'None':
        type_ref = type_none(frm_mid, 0)
        return type_ref
    elif typ == 'Redirection':
        return type_dir(frm_mid)
    elif typ == 'Binary':
        return type_binary(frm_mid)
    elif typ == 'Background':
        return type_bg(frm_mid)


class type_none(object):
    """shows no settings for phase"""

    def __init__(self, parent, row_):
        frm_ = tk.Frame(parent)
        frm_.grid(row=row_, column=0, sticky='nsew')


class type_bg(object):
    """shows background settings for phase"""

    def __init__(self, parent):
        self.frm_ = tk.Frame(parent)
        self.frm_.grid(row=0, column=0, sticky='nsew')
        lbl_frm = tk.LabelFrame(self.frm_, text='Background')
        lbl_frm.grid(row=0, column=0, sticky='ew')

        btn_open = tk.Button(lbl_frm, text='Open Background file',
                             command=self.open_file)
        self.lbl_file = tk.Label(lbl_frm, text='')
        btn_open.grid(row=0)
        self.lbl_file.grid(row=1)

    def open_file(self):
        filepath = askopenfilename(
            filetypes=[('Image Files', '*.bmp'), ('All Files', '*.*')]
        )
        if not filepath:
            return
        self.img = mpimg.imread(filepath)
        self.lbl_file['text'] = f'{filepath}'

    def phase(self):
        if self.lbl_file['text'] != '':
            phase = self.img
        else:
            phase = np.zeros([600, 792])
        return phase

    def close_(self):
        self.frm_.destroy()


class type_dir(object):
    """shows the settings for redirection"""

    def __init__(self, parent):
        self.frm_ = tk.Frame(parent)
        self.frm_.grid(row=1, column=0, sticky='nsew')
        lbl_frm = tk.LabelFrame(self.frm_, text='Redirection')
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
                np.arange(0, float(xdir), float(xdir)/792))
        else:
            phx = np.zeros([600, 792])

        if ydir != '' and float(ydir) != 0:
            phy = np.outer(
                np.arange(0, float(ydir), float(ydir)/600),
                np.ones([1, 792]))
        else:
            phy = np.zeros([600, 792])

        phase = phx + phy
        return phase

    def close_(self):
        self.frm_.destroy()


class type_binary(object):
    """shows binary settings for phase"""

    def __init__(self, parent):
        self.frm_ = tk.Frame(parent)
        self.frm_.grid(row=2, column=0, sticky='nsew')
        lbl_frm = tk.LabelFrame(self.frm_, text='Binary')
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
            tmp = float(self.ent_phi.get())
            phi = tmp*254/2  # Converting to 0-2pi = 0-254
        else:
            phi = 0

        phase_mat = np.zeros([600, 792])

        if direc == 'Horizontal':
            cutpixel = int(round(600*area/100))
            tmp = np.ones([cutpixel, 792])*phi
            phase_mat[0:cutpixel, :] = tmp
        elif direc == 'Vertical':
            cutpixel = int(round(792*area/100))
            tmp = np.ones([600, cutpixel])*phi
            phase_mat[:, 0:cutpixel] = tmp

        return phase_mat

    def close_(self):
        self.frm_.destroy()


class type_multibeams_cb(object):
    """shows multibeam checkerboard settings for phase"""

    def __init__(self, parent):
        frm_ = tk.Frame(parent)
        frm_.grid(row=0, column=0, sticky='nsew')
        lbl_frm = tk.LabelFrame(frm_, text='Multibeam')
        lbl_frm.grid(row=0, column=0, sticky='ew')

    def phase(self):
        phase = np.zeros([600, 792])
        return phase
