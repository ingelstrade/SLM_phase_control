import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import numpy as np
from tkinter.filedialog import askopenfilename, asksaveasfilename
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class main_screen(object):
    """"""

    def __init__(self, parent):
        """Constructor"""
        self.main_win = parent
        self.main_win.title('SLM Phase Control')

        self.main_win.columnconfigure(0, minsize=300, weight=1)
        self.main_win.rowconfigure(2, minsize=200, weight=1)

        # creating frames
        frm_top = tk.Frame(self.main_win)
        self.frm_mid = tk.Frame(self.main_win, relief='sunken')
        frm_bot = tk.Frame(self.main_win)

        # Creating labels
        lbl_title = tk.Label(
            self.main_win,
            text='Control Phase',
            font=tkFont.Font(family='Lucida Grande', size=20))
        lbl_screen = tk.Label(frm_top, text='Screen:')
        lbl_type = tk.Label(frm_top, text='Type:')

        # Creating buttons
        but_prev = tk.Button(frm_bot, text='Preview', command=self.open_prev)
        but_pub = tk.Button(frm_bot, text='Publish', command=self.open_pub)
        but_exit = tk.Button(frm_bot, text='EXIT', command=self.exit_prog)

        # Creating combobox
        cbx_scr = ttk.Combobox(frm_top, value=['None'])
        cbx_scr.current(0)
        self.cbx_type = ttk.Combobox(
            frm_top,
            value=['None'],
            state='readonly',
            postcommand=self.list_of_types)
        self.cbx_type.current(0)
        self.cbx_type.bind('<<ComboboxSelected>>', self.new_type)
        self.type = type_none(self.frm_mid)

        # Setting up general structure
        lbl_title.grid(row=0, column=0, sticky='ew')
        frm_top.grid(row=1, column=0, sticky='ew')
        self.frm_mid.grid(row=2, column=0, sticky='nsew')
        frm_bot.grid(row=3, column=0)

        # Setting up top frame
        lbl_screen.grid(row=0, column=0, sticky='e', padx=10, pady=10)
        cbx_scr.grid(row=0, column=1, sticky='w')
        lbl_type.grid(row=1, column=0, sticky='e', padx=10)
        self.cbx_type.grid(row=1, column=1, sticky='w')

        # Setting up bot frame
        but_prev.grid(row=0, column=0, padx=10, pady=5, ipadx=5)
        but_pub.grid(row=0, column=1, pady=5, ipadx=5)
        but_exit.grid(row=0, column=2, padx=10, pady=5, ipadx=5)

    def open_prev(self):
        self.prev_win = prev_screen(self)

    def open_pub(self):
        self.pub_win = pub_screen(self)

    def exit_prog(self):
        self.main_win.destroy()

    # The different types
    def list_of_types(self):
        self.cbx_type['values'] = ['None', 'Redirection']

    def new_type(self, event):
        type = self.cbx_type.get()
        if type == 'None':
            self.type = type_none(self.frm_mid)
        elif type == 'Redirection':
            self.type = type_dir(self.frm_mid)

    def type(self):
        return self.type


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
        lbl_dir.grid(row=0, column=0, sticky='ew')
        frm_dir.grid(row=1, column=0)

        lbl_xdir.grid(row=0, column=0, sticky='e')
        lbl_ydir.grid(row=1, column=0, sticky='e')
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


class prev_screen(object):
    """"""

    def __init__(self, parent):
        self.win = tk.Toplevel()
        self.win.geometry('600x500')
        self.win.title('SLM Phase Control - Preview')
        def handler(): return self.on_close_prev()
        btn_close = tk.Button(self.win, text='Close', command=handler)
        btn_close.pack(side=tk.BOTTOM)

        x = np.linspace(-40, 40, num=800)
        y = np.linspace(-30, 30, num=600)
        [X, Y] = np.meshgrid(x, y)

        x0 = 0  # center
        y0 = 0  # center
        sigma = 5  # beam waist
        A = 1  # peak of the beam
        res = ((X-x0)**2 + (Y-y0)**2)/(2*sigma**2)
        input_intensity = A * np.exp(-res)
        input_intensity[np.sqrt(X**2+Y**2) < 4] = 0

        input_phase = parent.type.phase()

        tmp = abs(input_intensity)*np.exp(1j*input_phase)

        focus_int = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(tmp)))

        fig1, ax1 = plt.subplots(nrows=2, ncols=2, figsize=(20, 15), dpi=100)
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


class pub_screen(object):
    """"""

    def __init__(self, parent):
        self.win = tk.Toplevel()
        self.win.attributes('-fullscreen', True)
        self.win.title('SLM Phase Control - Publish')
        def handler(): return self.on_close_prev()
        btn_close = tk.Button(self.win, text='Close', command=handler)
        btn_close.pack()

    def on_close_prev(self):
        self.win.destroy()


root = tk.Tk()

main = main_screen(root)


root.mainloop()
