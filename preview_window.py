import tkinter as tk
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

print('preview_window in')


class prev_screen(object):
    """"""

    def __init__(self, parent):
        self.win = tk.Toplevel()
        self.win.geometry('600x500')
        self.win.title('SLM Phase Control - Preview')
        def handler(): return self.on_close_prev()
        btn_close = tk.Button(self.win, text='Close', command=handler)
        btn_close.pack(side=tk.BOTTOM)

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

        input_phase = parent.get_phase()/254*2*3.141592653589793238462643383279

        tmp = abs(input_intensity)*np.exp(1j*input_phase)

        focus_int = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(tmp)))

        fig1, ax1 = plt.subplots(nrows=2, ncols=2)
        ax1[0, 0].imshow(input_intensity)
        ax1[0, 0].set_title('Input int')

        ax1[0, 1].imshow(input_phase)
        ax1[0, 1].set_title('Input phase')

        ax1[1, 0].imshow(abs(focus_int))
        ax1[1, 0].set_ylabel('In Focus')
        ax1[1, 0].axis([360, 440, 270, 330])

        ax1[1, 1].imshow(np.angle(focus_int))
        # ax1[1, 1].set_title('Focus phase')
        ax1[1, 1].axis([360, 440, 270, 330])

        img1 = FigureCanvasTkAgg(fig1, self.win)
        img1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    def on_close_prev(self):
        self.win.destroy()
