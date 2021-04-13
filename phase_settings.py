import tkinter as tk
from tkinter import ttk
import numpy as np
from tkinter.filedialog import askopenfilename
import matplotlib.image as mpimg
import time

print('types in')


def types():
    types = ['Background', 'Flat', 'Tilt', 'Binary', 'Lens',
             'Multibeam', 'Vortex']
    return types


def new_type(frm_mid, typ):
    if typ == 'Flat':
        return type_flat(frm_mid)
    elif typ == 'Tilt':
        return type_tilt(frm_mid)
    elif typ == 'Binary':
        return type_binary(frm_mid)
    elif typ == 'Background':
        return type_bg(frm_mid)
    elif typ == 'Lens':
        return type_lens(frm_mid)
    elif typ == 'Multibeam':
        return type_multibeams_cb(frm_mid)
    elif typ == 'Vortex':
        return type_vortex(frm_mid)


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


class type_tilt(object):
    """shows the settings for redirection"""

    def __init__(self, parent):
        self.frm_ = tk.Frame(parent)
        self.frm_.grid(row=2, column=0, sticky='nsew')
        lbl_frm = tk.LabelFrame(self.frm_, text='Tilt')
        lbl_frm.grid(row=0, column=0, sticky='ew', padx=5, pady=10)

        # Creating objects
        lbl_xdir = tk.Label(lbl_frm, text='Steepness along x-direction:')
        lbl_ydir = tk.Label(lbl_frm, text='Steepness along y-direction:')
        lbl_255 = tk.Label(lbl_frm, text='(255 corresponds to 2pi Rad)')
        lbl_step = tk.Label(lbl_frm, text='(wasd) Step per click:')
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
        self.strvar_tstep = tk.StringVar()
        self.ent_tstep = tk.Entry(
            lbl_frm, width=11,  validate='all',
            validatecommand=(vcmd, '%d', '%P', '%S'),
            textvariable=self.strvar_tstep)

        # Setting up
        lbl_xdir.grid(row=0, column=0, sticky='e', padx=(10, 0), pady=5)
        lbl_ydir.grid(row=1, column=0, sticky='e', padx=(10, 0), pady=(0, 5))
        lbl_255.grid(row=2, sticky='ew', padx=(10, 10), pady=(0, 5))
        self.ent_xdir.grid(row=0, column=1, sticky='w', padx=(0, 10))
        self.ent_ydir.grid(row=1, column=1, sticky='w', padx=(0, 10))
        lbl_step.grid(row=3, column=0, sticky='e', padx=(10, 0), pady=(0, 5))
        self.ent_tstep.grid(row=3, column=1, sticky='w', padx=(0, 10))

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

        if ydir != '' and float(ydir) != 0:
            phy = np.outer(
                np.ones([600, 1]),
                np.linspace(0, float(ydir)*791, num=792)) - float(ydir)*792/2
        else:
            phy = np.zeros([600, 792])

        if xdir != '' and float(xdir) != 0:
            phx = np.outer(
                np.linspace(0, float(xdir)*599, num=600),
                np.ones([1, 792])) - float(xdir)*600/2
        else:
            phx = np.zeros([600, 792])

        phase = phx + phy
        del phx
        del phy
        return phase

    def left_(self):
        tmp = float(self.strvar_xdir.get()) + float(self.strvar_tstep.get())
        self.strvar_xdir.set(tmp)

    def right_(self):
        tmp = float(self.strvar_xdir.get()) - float(self.strvar_tstep.get())
        self.strvar_xdir.set(tmp)

    def up_(self):
        tmp = float(self.strvar_ydir.get()) + float(self.strvar_tstep.get())
        self.strvar_ydir.set(tmp)

    def down_(self):
        tmp = float(self.strvar_ydir.get()) - float(self.strvar_tstep.get())
        self.strvar_ydir.set(tmp)

    def save_(self):
        dict = {'ent_xdir': self.ent_xdir.get(),
                'ent_ydir': self.ent_ydir.get()}
        return dict

    def load_(self, dict):
        self.strvar_xdir.set(dict['ent_xdir'])
        self.strvar_ydir.set(dict['ent_ydir'])

    def name_(self):
        return 'Tilt'

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
        del tmp
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
    """shows lens settings for phase"""

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
        del X, Y, R
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

        # creating frames
        frm_n = tk.Frame(lbl_frm)
        frm_sprrad = tk.Frame(lbl_frm)
        frm_spr = tk.Frame(frm_sprrad)
        frm_rad = tk.Frame(frm_sprrad)
        frm_int = tk.Frame(lbl_frm)
        frm_pxsiz = tk.Frame(lbl_frm)

        # creating labels
        lbl_n = tk.Label(frm_n, text='n^2; n=:')
        lbl_hor = tk.Label(frm_int, text='Hor:')
        lbl_vert = tk.Label(frm_int, text='Vert:')
        lbl_intil = tk.Label(frm_int, text='Intensity tilt')
        lbl_insqr = tk.Label(frm_int, text='Intensity curve')
        lbl_horspr = tk.Label(frm_spr, text='Horizontal spread:')
        lbl_verspr = tk.Label(frm_spr, text='Vertical spread:')
        lbl_cph = tk.Label(frm_sprrad, text='Hyp.phase diff')
        lbl_rad = tk.Label(frm_rad, text='Radius:')
        lbl_amp = tk.Label(frm_rad, text='Amplitude:')
        lbl_pxsiz = tk.Label(frm_pxsiz, text='pixel size:')

        # creating entries
        vcmd = (parent.register(self.callback))
        self.strvar_n = tk.StringVar()
        self.ent_n = tk.Entry(frm_n, width=5,  validate='all',
                              validatecommand=(vcmd, '%d', '%P', '%S'),
                              textvariable=self.strvar_n)
        self.strvar_hpt = tk.StringVar()
        self.ent_hpt = tk.Entry(frm_spr, width=5,  validate='all',
                                validatecommand=(vcmd, '%d', '%P', '%S'),
                                textvariable=self.strvar_hpt)
        self.strvar_vpt = tk.StringVar()
        self.ent_vpt = tk.Entry(frm_spr, width=5,  validate='all',
                                validatecommand=(vcmd, '%d', '%P', '%S'),
                                textvariable=self.strvar_vpt)
        self.strvar_rad = tk.StringVar()
        self.ent_rad = tk.Entry(frm_rad, width=5,  validate='all',
                                validatecommand=(vcmd, '%d', '%P', '%S'),
                                textvariable=self.strvar_rad)
        self.strvar_amp = tk.StringVar()
        self.ent_amp = tk.Entry(frm_rad, width=5,  validate='all',
                                validatecommand=(vcmd, '%d', '%P', '%S'),
                                textvariable=self.strvar_amp)
        self.strvar_hit = tk.StringVar()
        self.ent_hit = tk.Entry(frm_int, width=5,  validate='all',
                                validatecommand=(vcmd, '%d', '%P', '%S'),
                                textvariable=self.strvar_hit)
        self.strvar_vit = tk.StringVar()
        self.ent_vit = tk.Entry(frm_int, width=5,  validate='all',
                                validatecommand=(vcmd, '%d', '%P', '%S'),
                                textvariable=self.strvar_vit)
        self.strvar_his = tk.StringVar()
        self.ent_his = tk.Entry(frm_int, width=5,  validate='all',
                                validatecommand=(vcmd, '%d', '%P', '%S'),
                                textvariable=self.strvar_his)
        self.strvar_vis = tk.StringVar()
        self.ent_vis = tk.Entry(frm_int, width=5,  validate='all',
                                validatecommand=(vcmd, '%d', '%P', '%S'),
                                textvariable=self.strvar_vis)
        self.strvar_pxsiz = tk.StringVar()
        self.ent_pxsiz = tk.Entry(frm_pxsiz, width=5,  validate='all',
                                  validatecommand=(vcmd, '%d', '%P', '%S'),
                                  textvariable=self.strvar_pxsiz)

        # setup
        frm_n.grid(row=0, sticky='nsew')
        frm_sprrad.grid(row=1, sticky='nsew')
        frm_int.grid(row=2, sticky='nsew')
        frm_pxsiz.grid(row=3, sticky='nsew')

        frm_spr.grid(row=1, column=0, sticky='nsew')
        frm_rad.grid(row=1, column=1, sticky='ew')

        lbl_n.grid(row=0, column=0, sticky='e', padx=(10, 0), pady=(5, 10))
        self.ent_n.grid(row=0, column=1, sticky='w',
                        padx=(0, 10), pady=(5, 10))

        lbl_horspr.grid(row=0, column=0, sticky='e', padx=(10, 0))
        lbl_verspr.grid(row=1, column=0, sticky='e', padx=(10, 0))
        self.ent_hpt.grid(row=0, column=1, sticky='w')
        self.ent_vpt.grid(row=1, column=1, sticky='w')

        lbl_cph.grid(row=0, column=1, sticky='ew')

        lbl_rad.grid(row=0, column=0, sticky='e', padx=(15, 0))
        lbl_amp.grid(row=1, column=0, sticky='e', padx=(15, 0))
        self.ent_rad.grid(row=0, column=1, sticky='w', padx=(0, 5))
        self.ent_amp.grid(row=1, column=1, sticky='w', padx=(0, 5))

        lbl_hor.grid(row=1, column=0, sticky='e', padx=(10, 0))
        lbl_vert.grid(row=2, column=0, sticky='e', padx=(10, 0))
        lbl_intil.grid(row=0, column=1, padx=5, pady=(10, 0))
        lbl_insqr.grid(row=0, column=2, padx=(0, 5), pady=(10, 0))
        self.ent_hit.grid(row=1, column=1)
        self.ent_his.grid(row=1, column=2, padx=(0, 5))
        self.ent_vit.grid(row=2, column=1, pady=(0, 5))
        self.ent_vis.grid(row=2, column=2, padx=(0, 5), pady=(0, 5))

        lbl_pxsiz.grid(row=0, column=0, sticky='e', padx=(10, 0), pady=5)
        self.ent_pxsiz.grid(row=0, column=1, sticky='w')

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
        if self.ent_rad.get() != '':
            tmprad = float(self.ent_rad.get())
        else:
            tmprad = 0
        if self.ent_amp.get() != '':
            amp = float(self.ent_amp.get())
        else:
            amp = 0
        radsign = np.sign(tmprad)
        rad = np.abs(tmprad)
        x = tilts
        y = tilts
        [X, Y] = np.meshgrid(x, y)
        R = np.sqrt(X**2+Y**2)
        Z = amp*radsign*(np.sqrt(rad**2+R**2)-rad)
        ind = 0
        for row in Z:
            for elem in row:
                phases[:, :, ind] = elem + phases[:, :, ind]
                ind += 1

        # setting up for intensity control
        if self.ent_hit.get() != '':
            xit = float(self.ent_hit.get())
        else:
            xit = 0
        if self.ent_vit.get() != '':
            yit = float(self.ent_vit.get())
        else:
            yit = 0
        if self.ent_his.get() != '':
            xis = float(self.ent_his.get())
        else:
            xis = 0
        if self.ent_vis.get() != '':
            yis = float(self.ent_vis.get())
        else:
            yis = 0
        intensities = np.ones(n**2)
        totnum = np.ceil((600*(792+n)/(n**2)))  # nbr of pixels for each phase
        #          plus n in second dimension to account for noneven placement
        phase_nbr = np.outer(np.arange(n**2), np.ones([int(totnum)]))

        # modifying linear intensities
        if xit != 0:
            xits = np.linspace(-((n-1)/2*xit), ((n-1)/2*xit), num=n)
        else:
            xits = np.zeros(n)
        if yit != 0:
            yits = np.linspace(-((n-1)/2*yit), ((n-1)/2*yit), num=n)
        else:
            yits = np.zeros(n)
        ii = 0
        for tmpx in xits:
            intensities[n*ii:n*(ii+1)] = (tmpx + yits + 1)
            ii += 1

        # modifying square intensities
        spread = tilts
        xiss = -xis * (spread**2 - spread[0]**2)
        yiss = -yis * (spread**2 - spread[0]**2)
        ii = 0
        for tmpx in xiss:
            intensities[n*ii:n*(ii+1)] += (tmpx + yiss + 1)
            ii += 1

        # creating the intensity arrays (which phase to have at which pixel)
        intensities[intensities < 0] = 0
        intensities = intensities/np.sum(intensities)*n**2  # normalize
        tmpint = intensities-1
        beam = 0
        strong_beams = []
        strong_beams_int = []
        weak_beams = []
        weak_beams_int = []
        for intens in tmpint:
            if intens > 0:
                strong_beams.append(beam)
                strong_beams_int.append(intens)
            elif intens < 0:
                weak_beams.append(beam)
                weak_beams_int.append(intens)
            beam += 1
        # normalize to one
        strong_beams_int = strong_beams_int/np.sum(strong_beams_int)
        for wbeam, wbeam_int in zip(weak_beams, weak_beams_int):
            nbr_pixels = np.ceil(np.abs(wbeam_int)*totnum)  # nbrpxls to change
            nbr_each = np.ceil(nbr_pixels*strong_beams_int)
            strt = 0
            for nbr, sbeam in zip(nbr_each, strong_beams):
                phase_nbr[int(wbeam), strt:(strt+int(nbr))] = sbeam
                strt += int(nbr)
        rng = np.random.default_rng()
        rng.shuffle(phase_nbr, axis=1)  # mixing so the changed are not tgether
        col = np.zeros(n**2)  # keeping track of which column in phase_nbr

        if self.ent_pxsiz.get() != '':
            pxsiz = int(self.ent_pxsiz.get())
        else:
            pxsiz = 1
        # creating the total phase by adding the different ones
        xrange = np.arange(0, 792, 1)
        yrange = np.arange(0, 600, 1)
        tot_phase = np.zeros([600, 792])
        [X, Y] = np.meshgrid(xrange, yrange)
        def f(x): return np.int(x)
        f2 = np.vectorize(f)
        ind_phase = f2(
            (np.floor(X/pxsiz) % n)*n + (np.floor(Y/pxsiz) % n))
        for x in xrange:
            for y in yrange:
                try:
                    tot_phase[y, x] = phases[
                        y, x, int(phase_nbr[ind_phase[y, x], int(col[ind_phase[y, x]])])]
                except IndexError:
                    pass
                col[ind_phase[y, x]] += 1
        return tot_phase

    def phase_tilt(self, xdir, ydir):
        if xdir != '' and float(xdir) != 0:
            phx = np.outer(
                np.ones([600, 1]),
                np.linspace(0, float(xdir)*791, num=792)) - float(xdir)*792/2
        else:
            phx = np.zeros([600, 792])

        if ydir != '' and float(ydir) != 0:
            phy = np.outer(
                np.linspace(0, float(ydir)*599, num=600),
                np.ones([1, 792])) - float(ydir)*600/2
        else:
            phy = np.zeros([600, 792])

        phase = phx + phy
        return phase

    def save_(self):
        dict = {'n': self.ent_n.get(),
                'hpt': self.ent_hpt.get(),
                'rad': self.ent_rad.get(),
                'hit': self.ent_hit.get(),
                'his': self.ent_his.get(),
                'vpt': self.ent_vpt.get(),
                'amp': self.ent_amp.get(),
                'vit': self.ent_vit.get(),
                'vis': self.ent_vis.get(),
                'pxsiz': self.ent_pxsiz.get()}
        return dict

    def load_(self, dict):
        self.strvar_n.set(dict['n'])
        self.strvar_hpt.set(dict['hpt'])
        self.strvar_rad.set(dict['rad'])
        self.strvar_hit.set(dict['hit'])
        self.strvar_his.set(dict['his'])
        self.strvar_vpt.set(dict['vpt'])
        self.strvar_amp.set(dict['amp'])
        self.strvar_vit.set(dict['vit'])
        self.strvar_vis.set(dict['vis'])
        self.strvar_pxsiz.set(dict['pxsiz'])

    def name_(self):
        return 'Multibeam'

    def close_(self):
        self.frm_.destroy()


class type_vortex(object):
    """shows vortex settings for phase"""

    def __init__(self, parent):
        self.frm_ = tk.Frame(parent)
        self.frm_.grid(row=6, column=0, sticky='nsew')
        lbl_frm = tk.LabelFrame(self.frm_, text='Vortex')
        lbl_frm.grid(row=0, column=0, sticky='ew')

        lbl_vor = tk.Label(lbl_frm, text='Vortex order:')
        vcmd = (parent.register(self.callback))
        self.strvar_vor = tk.StringVar()
        self.ent_vor = tk.Entry(
            lbl_frm, width=11,  validate='all',
            validatecommand=(vcmd, '%d', '%P', '%S'),
            textvariable=self.strvar_vor)
        lbl_vor.grid(row=0, column=0, sticky='e', padx=(10, 0), pady=5)
        self.ent_vor.grid(row=0, column=1, sticky='w', padx=(0, 10))

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
        if self.ent_vor.get() != '':
            vor = float(self.ent_vor.get())
        else:
            vor = 0
        x = np.linspace(-7.92, 7.92, num=792)  # chipsize 15.84*12mm
        y = np.linspace(-6, 6, num=600)
        [X, Y] = np.meshgrid(x, y)
        theta = np.arctan(Y/X)
        theta[X < 0] += np.pi
        phase = theta*255/(2*np.pi)*vor
        return phase

    def save_(self):
        dict = {'vort_ord': self.ent_vor.get()}
        return dict

    def load_(self, dict):
        self.strvar_vor.set(dict['vort_ord'])

    def name_(self):
        return 'Vortex'

    def close_(self):
        self.frm_.destroy()
