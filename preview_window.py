from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
import tkinter as tk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")


print('preview_window in')


class prev_screen(object):
    """"""

    def __init__(self, parent):
        self.parent = parent
        self.win = tk.Toplevel()
        self.win.title('SLM Phase Control - Preview')
        def handler(): return self.on_close_prev()
        btn_close = tk.Button(self.win, text='Close', command=handler)
        btn_close.grid(row=1)
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax1 = self.fig.add_subplot(221)
        self.ax2 = self.fig.add_subplot(222)
        self.ax3 = self.fig.add_subplot(223)
        self.ax4 = self.fig.add_subplot(224)
        self.img1 = FigureCanvasTkAgg(self.fig, self.win)
        self.tk_widget_fig = self.img1.get_tk_widget()
        self.tk_widget_fig.grid(row=0, sticky='nsew')
        self.update_plots()

    def update_plots(self):
        x = np.linspace(-40, 40, num=792)
        y = np.linspace(-30, 30, num=600)
        [X, Y] = np.meshgrid(x, y)

        x0 = 0  # center
        y0 = 0  # center
        sigma = 5  # beam waist
        A = 1  # peak of the beam
        res = ((X-x0)**2 + (Y-y0)**2)/(2*sigma**2)
        input_intensity = A * np.exp(-res)
        input_intensity[np.sqrt(X**2+Y**2) < 4] = 0

        input_phase = self.parent.get_phase()/255*2*3.1415926535897932384626433

        tmp = abs(input_intensity)*np.exp(1j*input_phase)

        focus_int = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(tmp)))

        self.ax1.clear()
        self.ax1.imshow(input_intensity)
        self.ax1.set_title('Intensity')
        self.ax1.set_ylabel('Input')
        #
        self.ax2.clear()
        self.ax2.imshow(input_phase)
        self.ax2.set_title('Phase')
        #
        self.ax3.clear()
        self.ax3.imshow(abs(focus_int))
        self.ax3.set_ylabel('In Focus')
        self.ax3.axis([360, 440, 270, 330])
        #
        self.ax4.clear()
        self.ax4.imshow(np.angle(focus_int))
        self.ax4.axis([360, 440, 270, 330])

        self.img1.draw()

    def on_close_prev(self):
        plt.close(self.fig)
        self.win.destroy()
        self.parent.prev_win_closed()
