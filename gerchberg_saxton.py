from settings import slm_size, wavelength, chip_width, chip_height, pixel_size
import numpy as np
import tkinter as tk
from matplotlib import pyplot as plt

focal_length = 150e-3
distance = 500e-3


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
        vcmd = (parent.parent.register(parent.callback))
        
        frm_set = tk.LabelFrame(self.win, text='Settings')        
        
        lbl_d = tk.Label(frm_set, text='distance SLM-lens [mm]:')
        self.strvar_d = tk.StringVar(value=distance*1e3)
        self.ent_d = tk.Entry(frm_set, width=8, validate='all',
                              validatecommand=(vcmd, '%d', '%P', '%S'),
                              textvariable=self.strvar_d)
        lbl_f = tk.Label(frm_set, text='focal length [mm]:')
        self.strvar_f = tk.StringVar(value=focal_length*1e3)
        self.ent_f = tk.Entry(frm_set, width=8, validate='all',
                              validatecommand=(vcmd, '%d', '%P', '%S'),
                              textvariable=self.strvar_f)
        lbl_algorithm = tk.Label(frm_set, text='Algorithm')
        self.cbx_scpar = tk.ttk.Combobox(frm_set, values=list(algorithms.keys()))
        btn_close = tk.Button(self.win, text='Close', command=self.close_GS)
        
        lbl_d.grid(row=0, column=0, sticky='e')
        self.ent_d.grid(row=0, column=1, sticky='w')
        lbl_f.grid(row=1, column=0, sticky='e')
        self.ent_f.grid(row=1, column=1, sticky='w')
        lbl_algorithm.grid(row=2, column=0, sticky='e')
        self.cbx_scpar.grid(row=2, column=1, sticky='w')
        
        frm_set.grid(row=0)
        btn_close.grid(row=1)
        '''self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax1 = self.fig.add_subplot(221)
        self.ax2 = self.fig.add_subplot(222)
        self.ax3 = self.fig.add_subplot(223)
        self.ax4 = self.fig.add_subplot(224)
        self.img1 = FigureCanvasTkAgg(self.fig, self.win)
        self.tk_widget_fig = self.img1.get_tk_widget()
        self.tk_widget_fig.grid(row=0, sticky='nsew')
        self.update_plots()'''

    def close_GS(self):
        #plt.close(self.fig)
        self.win.destroy()
        self.parent.gen_win = None



# coordinates in the SLM plane
x_slm = np.linspace(-chip_width/2, chip_width/2, slm_size[1])
y_slm = np.linspace(-chip_height/2, chip_height/2, slm_size[0])

# coordinates in the image plane
x_img = np.fft.fftshift(np.fft.fftfreq(slm_size[1], 
                                       pixel_size/(wavelength*focal_length)))
y_img = np.fft.fftshift(np.fft.fftfreq(slm_size[0], 
                                       pixel_size/(wavelength*focal_length)))


def normalized(data):
    return data/np.max(data)


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
    