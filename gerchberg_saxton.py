from settings import slm_size, wavelength, chip_width, chip_height, pixel_size
import numpy as np
import tkinter as tk
from matplotlib import pyplot as plt
from matplotlib import image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

maxit = 100  # maximum number of iterations allowed

focal_length = 150e-3
distance = 500e-3

# coordinates in the SLM plane
x_slm = np.linspace(-chip_width/2, chip_width/2, slm_size[1])
y_slm = np.linspace(-chip_height/2, chip_height/2, slm_size[0])

# coordinates in the image plane
x_img = np.fft.fftshift(np.fft.fftfreq(slm_size[1], 
                                       pixel_size/(wavelength*focal_length)))
y_img = np.fft.fftshift(np.fft.fftfreq(slm_size[0], 
                                       pixel_size/(wavelength*focal_length)))


def gaussian(sigma, mu_x=slm_size[1]/2, mu_y=slm_size[0]/2):
    X = np.arange(slm_size[1])
    Y = np.arange(slm_size[0])
    x, y = np.meshgrid(X,Y)
    return np.exp(-1/2 * (((x-mu_x)**2+(y-mu_y)**2)/sigma**2))

def flat_top(r, dx=slm_size[1]/2, dy=slm_size[0]/2):
    X = np.arange(slm_size[1])
    Y = np.arange(slm_size[0])
    x, y = np.meshgrid(X,Y)
    return np.where((x-dx)**2+(y-dy)**2 < r**2, 1, 0)

shapes = {'2D Gaussian': gaussian, 'flat-top circle': flat_top}


def GS_algorithm(hologram, iterations):
    
    # initial guess for the phase 
    phi = np.random.rand(*slm_size) * 2 * np.pi - np.pi
    
    for i in range(iterations):
    
        # restore SLM-plane intensity
        A = np.ones(slm_size)
        f_slm = A*np.exp(1j*phi)
        
        # propagate
        x = np.fft.fftshift(np.fft.fft2(f_slm))
        B = np.abs(x)
        theta = np.angle(x)
        
        # apply constraints
        B = hologram
        f_img = B*np.exp(1j*theta)
        
        # invert propagation
        y = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(f_img)))
        A = np.abs(y)
        phi = np.angle(y)
    
    return A, phi


algorithms = {'Gerchberg-Saxton (GS)': GS_algorithm}



class GS_window(object):
    """create a window to access the algorithm from the main program"""

    def __init__(self, parent):
        self.parent = parent
        self.win = tk.Toplevel()
        self.win.title('SLM Phase Control - Hologram Generator')
        self.vcmd = (parent.parent.register(parent.callback))
        
        # Settings frame
        frm_set = tk.LabelFrame(self.win, text='Settings')        
        lbl_d = tk.Label(frm_set, text='distance SLM-lens [mm]:')
        self.strvar_d = tk.StringVar(value=distance*1e3)
        self.ent_d = tk.Entry(frm_set, width=8, validate='all',
                              validatecommand=(self.vcmd, '%d', '%P', '%S'),
                              textvariable=self.strvar_d)
        lbl_f = tk.Label(frm_set, text='focal length [mm]:')
        self.strvar_f = tk.StringVar(value=focal_length*1e3)
        self.ent_f = tk.Entry(frm_set, width=8, validate='all',
                              validatecommand=(self.vcmd, '%d', '%P', '%S'),
                              textvariable=self.strvar_f)
        lbl_algorithm = tk.Label(frm_set, text='Algorithm')
        self.cbx_alg = tk.ttk.Combobox(frm_set, values=list(algorithms.keys()))
        lbl_it = tk.Label(frm_set, text='number of iterations:')
        self.ent_it = tk.Spinbox(frm_set, width=5, from_=1, to=maxit)
        lbl_d.grid(row=0, column=0, sticky='e')
        self.ent_d.grid(row=0, column=1, sticky='w')
        lbl_f.grid(row=1, column=0, sticky='e')
        self.ent_f.grid(row=1, column=1, sticky='w')
        lbl_algorithm.grid(row=2, column=0, sticky='e')
        self.cbx_alg.grid(row=2, column=1, sticky='w')
        lbl_it.grid(row=3, column=0, sticky='e')
        self.ent_it.grid(row=3, column=1, sticky='w')
        
        # Frame for loading images to be turned into a hologram
        frm_load = tk.LabelFrame(self.win, width=250,
                                 text='Load hologram image')  
        btn_open = tk.Button(frm_load, text='Open hologram image',
                             command=self.open_file)
        lbl_act_file = tk.Label(frm_load, text='File containing hologram to produce:', 
                                justify='left')
        self.lbl_file = tk.Label(frm_load, text='', wraplength=190,
                                 justify='left', foreground='gray')
        btn_open.grid(row=0)
        lbl_act_file.grid(row=1)
        self.lbl_file.grid(row=2)
        
        # Frame for generating images to be turned into a hologram
        self.frm_gen = tk.LabelFrame(self.win, text='Generate hologram image')
        lbl_algorithm = tk.Label(self.frm_gen, text='Algorithm')
        self.cbx_shape = tk.ttk.Combobox(self.frm_gen, values=list(shapes.keys()))
        lbl_algorithm.grid(row=0, column=0, sticky='e')
        self.cbx_shape.grid(row=0, column=1, sticky='w')
        self.btn_gen = tk.Button(self.frm_gen, text='Generate image',
                                 command=self.generate_image)
        self.render_image_generator()
        
        # Frame for generating the actual hologram and for figures
        self.frm_calc = tk.LabelFrame(self.win, text='Phase pattern generator algorithm')
        self.btn_gen = tk.Button(self.frm_calc, text='Calculate phase',
                                 command=self.calculate_phase)
        self.prepare_figure()
        self.btn_gen.grid(row=0)
        self.tk_widget_fig.grid(row=1, sticky='nsew', pady=5)

        # Main layout
        btn_ok = tk.Button(self.win, text='OK', command=self.take_pattern)
        btn_close = tk.Button(self.win, text='Close', command=self.close_GS)
        frm_set.grid(row=0, columnspan=2, sticky='nw', padx=5, pady=5)
        frm_load.grid(row=1, column=0, sticky='nw', padx=5, pady=5)
        self.frm_gen.grid(row=1, column=1, sticky='nw', padx=5, pady=5)
        self.frm_calc.grid(row=2, columnspan=2, sticky='nw', padx=5, pady=5)
        btn_ok.grid(row=3, column=0, padx=5, pady=5)
        btn_close.grid(row=3, column=1, padx=5, pady=5)

    
    def render_image_generator(self):
        # may later be called by each change of self.cbx_shape
        self.varnames = ['r', 'dx', 'dy']
        lbl_texts = ['r [mm]:', 'dx [mm]:', 'dy [mm]:']
        self.labels = [tk.Label(self.frm_gen, text=lbl_text) for lbl_text in lbl_texts]
        self.strvars = [tk.StringVar() for lbl_text in lbl_texts]
        self.entries = [tk.Entry(self.frm_gen, width=11,  validate='all',
                                 validatecommand=(self.vcmd, '%d', '%P', '%S'),
                                 textvariable=strvar)
                        for strvar in self.strvars]
        for ind, label in enumerate(self.labels):
            label.grid(row=ind+1, column=0, sticky='e', padx=(10, 0))
        for ind, entry in enumerate(self.entries):
            entry.grid(row=ind+1, column=1, sticky='w', padx=(0, 10))
        self.btn_gen.grid(row=(len(self.entries)+1), columnspan=2)
    
    def prepare_figure(self):
        plt.rc('font', size=8)
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax1 = self.fig.add_subplot(221)
        self.ax1.set_title('desired focus shape (input)', fontsize=8)
        self.ax2 = self.fig.add_subplot(222)
        self.ax2.set_title('generated phase pattern (output)', fontsize=8)
        self.ax3 = self.fig.add_subplot(223)
        self.ax3.set_title('intensity in the focus', fontsize=8)
        self.ax4 = self.fig.add_subplot(224)
        self.ax4.set_title('phase in the focus', fontsize=8)
        self.fig.tight_layout()
        self.img1 = FigureCanvasTkAgg(self.fig, self.frm_calc)
        self.tk_widget_fig = self.img1.get_tk_widget()
        
    def open_file(self):
            filepath = tk.filedialog.askopenfilename(
                filetypes=[('CSV data arrays', '*.csv'), ('Image Files', '*.bmp'), 
                           ('All Files', '*.*')]
            )
            if not filepath:
                return
            if filepath[-4:] == '.csv':
                self.img = np.loadtxt(filepath, delimiter=',')
            else:
                self.img = image.imread(filepath)
            self.lbl_file['text'] = f'{filepath}'
    
    def generate_image(self):
        # TODO!
        pass
    
    def calculate_phase(self):
        # TODO!
        pass
        
    def take_pattern(self):
        # TODO!
        pass

    def close_GS(self):
        #plt.close(self.fig)
        self.win.destroy()
        self.parent.gen_win = None



if __name__ == '__main__':
    
    A = np.ones(slm_size)
    B, phi = GS_algorithm(flat_top(7), 15)
    f_slm = abs(A)*np.exp(1j*phi)
    
    fft = np.fft.fftshift(np.fft.fft2(f_slm))
    
    plt.imshow(phi, cmap='twilight', interpolation='None',
               extent=[x_slm[0]*1e3,x_slm[-1]*1e3,y_slm[0]*1e3,y_slm[-1]*1e3])
    plt.xlabel('[mm]')
    plt.ylabel('[mm]')
    plt.colorbar(label='phase [rad]')
    plt.show()
    
    plt.imshow(np.abs(fft), cmap='inferno',
               extent=[x_img[0]*1e3,x_img[-1]*1e3,y_img[0]*1e3,y_img[-1]*1e3])
    plt.xlabel('[mm]')
    plt.ylabel('[mm]')
    plt.colorbar()
    plt.show()
    