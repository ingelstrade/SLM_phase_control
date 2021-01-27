import tkinter as tk
from tkinter import ttk
import numpy as np
from tkinter.filedialog import askopenfilename
import matplotlib.image as mpimg

print('types in')


def types():
    types = ['Background', 'Flat', 'Redirection', 'Binary', 'Lens',
             'Multibeam']
    return types


def new_type(frm_mid, typ):
    if typ == 'Flat':
        return type_flat(frm_mid)
    elif typ == 'Redirection':
        return type_dir(frm_mid)
    elif typ == 'Binary':
        return type_binary(frm_mid)
    elif typ == 'Background':
        return type_bg(frm_mid)
    elif typ == 'Lens':
        return type_lens(frm_mid)
    elif typ == 'Multibeam':
        return type_multibeams_cb(frm_mid)


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

    def save_(self):
        dict = {'filepath': self.lbl_file['text']}
        return dict

    def load_(self, dict):
        self.lbl_file['text'] = dict['filepath']
        try:
            self.img = mpimg.imread(dict['filepath'])
        except:
            print('File missing')

    def name_(self):
        return 'Background'

    def close_(self):
        self.frm_.destroy()


class type_flat(object):
    """shows flat settings for phase"""

    def __init__(self, parent):
        self.frm_ = tk.Frame(parent)
        self.frm_.grid(row=1, column=0, sticky='nsew')
        lbl_frm = tk.LabelFrame(self.frm_, text='Flat')
        lbl_frm.grid(row=0, column=0, sticky='ew')

        lbl_phi = tk.Label(lbl_frm, text='Phase shift (255=2pi):')
        vcmd = (parent.register(self.callback))
        self.strvar_flat = tk.StringVar()
        self.ent_flat = tk.Entry(
            lbl_frm, width=11,  validate='all',
            validatecommand=(vcmd, '%d', '%P', '%S'),
            textvariable=self.strvar_flat)
        lbl_phi.grid(row=0, column=0, sticky='e', padx=(10, 0), pady=5)
        self.ent_flat.grid(row=0, column=1, sticky='w', padx=(0, 10))

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
        if self.ent_flat.get() != '':
            phi = float(self.ent_flat.get())
        else:
            phi = 0
        phase = np.ones([600, 792])*phi
        return phase

    def save_(self):
        dict = {'flat_phase': self.ent_flat.get()}
        return dict

    def load_(self, dict):
        self.strvar_flat.set(dict['flat_phase'])

    def name_(self):
        return 'Flat'

    def close_(self):
        self.frm_.destroy()


class type_dir(object):
    """shows the settings for redirection"""

    def __init__(self, parent):
        self.frm_ = tk.Frame(parent)
        self.frm_.grid(row=2, column=0, sticky='nsew')
        lbl_frm = tk.LabelFrame(self.frm_, text='Redirection')
        lbl_frm.grid(row=0, column=0, sticky='ew', padx=5, pady=10)

        # Creating objects
        lbl_xdir = tk.Label(lbl_frm, text='Steepness along x-direction:')
        lbl_ydir = tk.Label(lbl_frm, text='Steepness along y-direction:')
        lbl_255 = tk.Label(lbl_frm, text='(255 corresponds to 2pi Rad)')
        vcmd = (parent.register(self.callback))
        self.strvar_xdir = tk.StringVar()
        self.strvar_ydir = tk.StringVar()
        self.ent_xdir = tk.Entry(
            lbl_frm, width=11,  validate='all',
            validatecommand=(vcmd, '%d', '%P', '%S'),
            textvariable=self.strvar_xdir)
        self.ent_ydir = tk.Entry(
            lbl_frm, width=11,  validate='all',
            validatecommand=(vcmd, '%d', '%P', '%S'),
            textvariable=self.strvar_ydir)

        # Setting up
        lbl_xdir.grid(row=0, column=0, sticky='e', padx=(10, 0), pady=5)
        lbl_ydir.grid(row=1, column=0, sticky='e', padx=(10, 0), pady=(0, 5))
        lbl_255.grid(row=2, sticky='ew', padx=(10, 10), pady=(0, 5))
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
                np.arange(0, float(xdir)*792, float(xdir))) - float(xdir)*792/2
        else:
            phx = np.zeros([600, 792])

        if ydir != '' and float(ydir) != 0:
            phy = np.outer(
                np.arange(0, float(ydir)*600, float(ydir)),
                np.ones([1, 792])) - float(ydir)*600/2
        else:
            phy = np.zeros([600, 792])

        phase = phx + phy
        return phase

    def save_(self):
        dict = {'ent_xdir': self.ent_xdir.get(),
                'ent_ydir': self.ent_ydir.get()}
        return dict

    def load_(self, dict):
        self.strvar_xdir.set(dict['ent_xdir'])
        self.strvar_ydir.set(dict['ent_ydir'])

    def name_(self):
        return 'Redirection'

    def close_(self):
        self.frm_.destroy()


class type_binary(object):
    """shows binary settings for phase"""

    def __init__(self, parent):
        self.frm_ = tk.Frame(parent)
        self.frm_.grid(row=3, column=0, sticky='nsew')
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

    def save_(self):
        dict = {'direc': self.cbx_dir.get(),
                'area': self.ent_area.get(),
                'phi': self.ent_phi.get()}
        return dict

    def load_(self, dict):
        tmpind = self.cbx_dir['values'].index(dict['direc'])
        self.cbx_dir.current(tmpind)
        self.ent_area.delete(0, tk.END)
        self.ent_phi.delete(0, tk.END)
        self.ent_area.insert(0, dict['area'])
        self.ent_phi.insert(0, dict['phi'])

    def name_(self):
        return 'Binary'

    def close_(self):
        self.frm_.destroy()


class type_lens(object):
    """shows multibeam checkerboard settings for phase"""

    def __init__(self, parent):
        self.frm_ = tk.Frame(parent)
        self.frm_.grid(row=4, column=0, sticky='nsew')
        lbl_frm = tk.LabelFrame(self.frm_, text='Lens')
        lbl_frm.grid(row=0, column=0, sticky='ew')

        # creating labels
        lbl_rad = tk.Label(lbl_frm, text='Radius [mm]:')
        lbl_fac = tk.Label(lbl_frm, text='Multiplication factor [Rad/mmglas]:')

        # creating entries
        vcmd = (parent.register(self.callback))
        self.strvar_rad = tk.StringVar()
        self.ent_rad = tk.Entry(lbl_frm, width=5,  validate='all',
                                validatecommand=(vcmd, '%d', '%P', '%S'),
                                textvariable=self.strvar_rad)
        self.strvar_fac = tk.StringVar()
        self.ent_fac = tk.Entry(lbl_frm, width=5,  validate='all',
                                validatecommand=(vcmd, '%d', '%P', '%S'),
                                textvariable=self.strvar_fac)
        self.strvar_fac.set('150000')

        # setup
        lbl_rad.grid(row=0, column=0, sticky='e', padx=(10, 0), pady=5)
        lbl_fac.grid(row=1, column=0, sticky='e', padx=(10, 0))
        self.ent_rad.grid(row=0, column=1, sticky='w', padx=(0, 10))
        self.ent_fac.grid(row=1, column=1, sticky='w', padx=(0, 10), pady=5)

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
        # getting the hyperbolical curve on the phases
        if self.ent_rad.get() != '':
            rad = float(self.ent_rad.get())
        else:
            rad = 1000000
        if self.ent_fac.get() != '':
            fac = float(self.ent_fac.get())
        else:
            fac = 0
        radsign = np.sign(rad)
        rad = np.abs(rad)
        x = np.linspace(-7.92, 7.92, num=792)  # chipsize 15.84*12mm
        y = np.linspace(-6, 6, num=600)
        [X, Y] = np.meshgrid(x, y)
        R = np.sqrt(X**2+Y**2)  # radius on a 2d array
        Z = fac*radsign*(np.sqrt(rad**2+R**2)-rad)
        return Z

    def save_(self):
        dict = {'rad': self.ent_rad.get(),
                'fac': self.ent_fac.get()}
        return dict

    def load_(self, dict):
        self.strvar_rad.set(dict['rad'])
        self.strvar_fac.set(dict['fac'])

    def name_(self):
        return 'Lens'

    def close_(self):
        self.frm_.destroy()


class type_multibeams_cb(object):
    """shows multibeam checkerboard settings for phase"""

    def __init__(self, parent):
        self.frm_ = tk.Frame(parent)
        self.frm_.grid(row=5, column=0, sticky='nsew')
        lbl_frm = tk.LabelFrame(self.frm_, text='Multibeam')
        lbl_frm.grid(row=0, column=0, sticky='ew')

        # creating labels
        lbl_n = tk.Label(lbl_frm, text='n^2; n=:')
        lbl_hor = tk.Label(lbl_frm, text='Hor:')
        lbl_vert = tk.Label(lbl_frm, text='Vert:')
        lbl_phdif = tk.Label(lbl_frm, text='Phase tilt diff')
        lbl_phsq = tk.Label(lbl_frm, text='Phase square diff')
        lbl_intil = tk.Label(lbl_frm, text='Intensity tilt')
        lbl_insqr = tk.Label(lbl_frm, text='Intensity curve')

        # creating entries
        vcmd = (parent.register(self.callback))
        self.ent_n = tk.Entry(lbl_frm, width=5,  validate='all',
                              validatecommand=(vcmd, '%d', '%P', '%S'))
        self.ent_hpt = tk.Entry(lbl_frm, width=5,  validate='all',
                                validatecommand=(vcmd, '%d', '%P', '%S'))
        self.ent_vpt = tk.Entry(lbl_frm, width=5,  validate='all',
                                validatecommand=(vcmd, '%d', '%P', '%S'))
        self.ent_hps = tk.Entry(lbl_frm, width=5,  validate='all',
                                validatecommand=(vcmd, '%d', '%P', '%S'))
        self.ent_vps = tk.Entry(lbl_frm, width=5,  validate='all',
                                validatecommand=(vcmd, '%d', '%P', '%S'))
        self.ent_hit = tk.Entry(lbl_frm, width=5,  validate='all',
                                validatecommand=(vcmd, '%d', '%P', '%S'))
        self.ent_vit = tk.Entry(lbl_frm, width=5,  validate='all',
                                validatecommand=(vcmd, '%d', '%P', '%S'))
        self.ent_his = tk.Entry(lbl_frm, width=5,  validate='all',
                                validatecommand=(vcmd, '%d', '%P', '%S'))
        self.ent_vis = tk.Entry(lbl_frm, width=5,  validate='all',
                                validatecommand=(vcmd, '%d', '%P', '%S'))

        # setup
        lbl_n.grid(row=0, column=0, sticky='e', padx=(10, 0), pady=(5, 10))
        self.ent_n.grid(row=0, column=1, sticky='w',
                        padx=(0, 10), pady=(5, 10))
        lbl_hor.grid(row=2, column=0, sticky='e', padx=(10, 0), pady=5)
        lbl_vert.grid(row=3, column=0, sticky='e', padx=(10, 0), pady=(5, 5))
        lbl_phdif.grid(row=1, column=1, padx=5)
        lbl_phsq.grid(row=1, column=2)
        lbl_intil.grid(row=1, column=3, padx=5)
        lbl_insqr.grid(row=1, column=4, padx=(0, 5))
        self.ent_hpt.grid(row=2, column=1)
        self.ent_hps.grid(row=2, column=2)
        self.ent_hit.grid(row=2, column=3)
        self.ent_his.grid(row=2, column=4, padx=(0, 5))
        self.ent_vpt.grid(row=3, column=1, pady=(0, 5))
        self.ent_vps.grid(row=3, column=2, pady=(0, 5))
        self.ent_vit.grid(row=3, column=3, pady=(0, 5))
        self.ent_vis.grid(row=3, column=4, padx=(0, 5), pady=(0, 5))

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
        if self.ent_n.get() != '':
            n = int(self.ent_n.get())
        else:
            n = 1

        # getting the different phases for the beams
        if self.ent_hpt.get() != '':
            xtilt = float(self.ent_hpt.get())
        else:
            xtilt = 0
        if self.ent_vpt.get() != '':
            ytilt = float(self.ent_vpt.get())
        else:
            ytilt = 0
        tilts = np.arange(-n+1, n+1, 2)  # excluding the last
        xtilts = tilts*xtilt/2
        ytilts = tilts*ytilt/2
        phases = np.zeros([600, 792, n*n])
        ind = 0
        for xdir in xtilts:
            for ydir in ytilts:
                phases[:, :, ind] = self.phase_tilt(xdir, ydir)
                ind += 1

        # getting the hyperbolical curve on the phases
        if self.ent_hps.get() != '':
            xps = float(self.ent_hps.get())
        else:
            xps = 0
        if self.ent_vps.get() != '':
            yps = float(self.ent_vps.get())
        else:
            yps = 0
        xsign = np.sign(xps)
        ysign = np.sign(yps)
        xrad = np.abs(xps)
        yrad = np.abs(yps)
        x = np.linspace(-7.92, 7.92, num=792)  # chipsize 15.84*12mm
        y = np.linspace(-6, 6, num=600)
        [X, Y] = np.meshgrid(x, y)
        R = np.sqrt(X**2+Y**2)
        Z = yrad*xsign*(np.sqrt(xrad**2+R**2)-xrad)
        for ind in range(n**2):
            phases[:, :, ind] += Z

        # creating the total phase by adding the different ones
        xrange = np.arange(0, 792, 1)
        yrange = np.arange(0, 600, 1)
        tot_phase = np.zeros([600, 792])
        for x in xrange:
            for y in yrange:
                ind_phase = (x % n)*n + (y % n)  # x*n^1 + y*n^0 but x,y mod n
                tot_phase[y, x] = phases[y, x, ind_phase]

        return tot_phase

    def phase_tilt(self, xdir, ydir):
        print(xdir, ydir)
        if xdir != '' and float(xdir) != 0:
            phx = np.outer(
                np.ones([600, 1]),
                np.arange(0, float(xdir)*792, float(xdir))) - float(xdir)*792/2
        else:
            phx = np.zeros([600, 792])

        if ydir != '' and float(ydir) != 0:
            phy = np.outer(
                np.arange(0, float(ydir)*600, float(ydir)),
                np.ones([1, 792])) - float(ydir)*600/2
        else:
            phy = np.zeros([600, 792])

        phase = phx + phy
        return phase

    def save_(self):
        dict = {'n': self.ent_n.get(),
                'hpt': self.ent_hpt.get(),
                'hps': self.ent_hps.get(),
                'hit': self.ent_hit.get(),
                'his': self.ent_his.get(),
                'vpt': self.ent_vpt.get(),
                'vps': self.ent_vps.get(),
                'vit': self.ent_vit.get(),
                'vis': self.ent_vis.get()}
        return dict

    def load_(self, dict):
        self.ent_n.delete(0, tk.END)
        self.ent_hpt.delete(0, tk.END)
        self.ent_hps.delete(0, tk.END)
        self.ent_hit.delete(0, tk.END)
        self.ent_his.delete(0, tk.END)
        self.ent_vpt.delete(0, tk.END)
        self.ent_vps.delete(0, tk.END)
        self.ent_vit.delete(0, tk.END)
        self.ent_vis.delete(0, tk.END)
        self.ent_n.insert(0, dict['n'])
        self.ent_hpt.insert(0, dict['hpt'])
        self.ent_hps.insert(0, dict['hps'])
        self.ent_hit.insert(0, dict['hit'])
        self.ent_his.insert(0, dict['his'])
        self.ent_vpt.insert(0, dict['vpt'])
        self.ent_vps.insert(0, dict['vps'])
        self.ent_vit.insert(0, dict['vit'])
        self.ent_vis.insert(0, dict['vis'])

    def name_(self):
        return 'Multibeam'

    def close_(self):
        self.frm_.destroy()
