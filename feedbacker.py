import cam
import tkinter as tk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import gxipy as gx
from PIL import Image
import time
import draw_polygon


class feedbacker(object):
    """works back and forth with publish_window"""

    def __init__(self, pub_win):
        self.pub_win = pub_win
        self.win = tk.Toplevel()
        self.win.geometry('500x470+300+100')

        # creating frames
        frm_cam = tk.Frame(self.win)
        frm_bot = tk.Frame(self.win)
        frm_cam_but = tk.Frame(frm_cam)
        frm_cam_but_set = tk.Frame(frm_cam_but)

        # creating buttons n labels
        but_exit = tk.Button(frm_bot, text='EXIT', command=self.on_close)
        but_feedback = tk.Button(frm_bot, text='Feedback', command=self.feedback)
        but_cam_img = tk.Button(frm_cam_but, text='Get image', command=self.cam_img)
        but_cam_line = tk.Button(frm_cam_but, text='Get cont images', command=self.cam_cont_img)
        self.bVar_cam = tk.BooleanVar(self.win,True)
        but_cam_phi = tk.Button(frm_cam_but, text='Get phase', command=self.bVar_cam==False)
        lbl_phi = tk.Label(frm_bot, text='Phase shift (in pi):')
        vcmd = (self.win.register(self.callback))
        self.strvar_flat = tk.StringVar()
        self.ent_flat = tk.Entry(
            frm_bot, width=11,  validate='all',
            validatecommand=(vcmd, '%d', '%P', '%S'),
            textvariable=self.strvar_flat)
        lbl_cam_ind = tk.Label(frm_cam_but_set, text='Camera index:')
        self.strvar_cam_ind = tk.StringVar(self.win,'1')
        self.ent_cam_ind = tk.Entry(
            frm_cam_but_set, width=11,  validate='all',
            validatecommand=(vcmd, '%d', '%P', '%S'),
            textvariable=self.strvar_cam_ind)
        lbl_cam_exp = tk.Label(frm_cam_but_set, text='Camera exposure (us):')
        self.strvar_cam_exp = tk.StringVar(self.win,'1000')
        self.ent_cam_exp = tk.Entry(
            frm_cam_but_set, width=11,  validate='all',
            validatecommand=(vcmd, '%d', '%P', '%S'),
            textvariable=self.strvar_cam_exp)
        lbl_cam_gain = tk.Label(frm_cam_but_set, text='Camera gain (0-24):')
        self.strvar_cam_gain = tk.StringVar(self.win,'0')
        self.ent_cam_gain = tk.Entry(
            frm_cam_but_set, width=11,  validate='all',
            validatecommand=(vcmd, '%d', '%P', '%S'),
            textvariable=self.strvar_cam_gain)
        but_area1 = tk.Button(frm_bot, text='Select area1', command=self.set_area1)
        but_area2 = tk.Button(frm_bot, text='Select area2', command=self.set_area2)

        # setting up
        frm_cam.grid(row=0, column=0, sticky='nsew')
        frm_bot.grid(row=1, column=0, sticky='nsew')
        frm_cam_but.grid(row=1, column=0, sticky='nsew')

        # setting up buttons frm_cam
        but_cam_img.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5)
        but_cam_line.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5)
        but_cam_phi.grid(row=0, column=2, padx=5, pady=5, ipadx=5, ipady=5)
        frm_cam_but_set.grid(row=0, column=3, sticky='nsew')
        lbl_cam_ind.grid(row=0, column=0)
        self.ent_cam_ind.grid(row=0, column=1, padx=(0,10))
        lbl_cam_exp.grid(row=1, column=0)
        self.ent_cam_exp.grid(row=1, column=1, padx=(0,10))
        lbl_cam_gain.grid(row=2, column=0)
        self.ent_cam_gain.grid(row=2, column=1, padx=(0,10))

        # setting up buttons frm_bot
        lbl_phi.grid(row=0, column=0, sticky='e', padx=(10, 0), pady=5)
        self.ent_flat.grid(row=0, column=1, sticky='w', padx=(0, 10))
        but_exit.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=5)
        but_feedback.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=5)
        but_area1.grid(row=0, column=2)
        but_area2.grid(row=1, column=2)

        # setting up canvas
        self.fig = Figure(figsize=(4, 3), dpi=100)
        self.ax1 = self.fig.add_subplot(111)
        self.img1 = FigureCanvasTkAgg(self.fig, frm_cam)
        self.tk_widget_fig = self.img1.get_tk_widget()
        self.tk_widget_fig.grid(row=0, sticky='nsew')



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

    def feedback(self):
        if self.ent_flat.get() != '':
            phi = float(self.ent_flat.get())
        else:
            phi = 0
        self.pub_win.publish_img(self.pub_win.phase + phi*255)

    def init_cam(self, single):
        print("")
        print("Initializing......")
        print("")
        # create a device manager
        device_manager = gx.DeviceManager()
        dev_num, dev_info_list = device_manager.update_device_list()
        if dev_num is 0:
            print("Number of enumerated devices is 0")
            return

        # open the first device
        cam1 = device_manager.open_device_by_index(int(self.ent_cam_ind.get()))
        self.camdev = cam1

        # set exposure
        cam1.ExposureTime.set(float(self.ent_cam_exp.get()))

        # set gain
        cam1.Gain.set(float(self.ent_cam_gain.get()))

        if dev_info_list[0].get("device_class") == gx.GxDeviceClassList.USB2:
            # set trigger mode
            cam1.TriggerMode.set(gx.GxSwitchEntry.ON)
        else:
            # set trigger mode and trigger source
            cam1.TriggerMode.set(gx.GxSwitchEntry.ON)
            cam1.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)

        # start data acquisition
        cam1.stream_on()

        if single:
            self.acq_mono(self.camdev, 1)
            self.cam_on_close(self.camdev)
        else:
            self.acq_mono(self.camdev, 60)
            self.cam_on_close(self.camdev)

    def acq_mono(self, device, num):
        """
               :brief      acquisition function of mono device
               :param      device:     device object[Device]
               :param      num:        number of acquisition images[int]
        """
        for i in range(num):
            time.sleep(0.01)

            # send software trigger command
            device.TriggerSoftware.send_command()

            # get raw image
            raw_image = device.data_stream[0].get_image()
            if raw_image is None:
                print("Getting image failed.")
                continue

            # create numpy array with data from raw image
            numpy_image = raw_image.get_numpy_array()
            if numpy_image is None:
                continue

            # show acquired image
            # img = Image.fromarray(numpy_image, 'L')
            # img.show()
            self.ax1.clear()
            self.ax1.imshow(numpy_image)
            self.img1.draw()

            # print height, width, and frame ID of the acquisition image
            print("Frame ID: %d   Height: %d   Width: %d"
                  % (raw_image.get_frame_id(), raw_image.get_height(), raw_image.get_width()))


    def cam_on_close(self, device):

        # stop acquisition
        device.stream_off()

        # close device
        device.close_device()

    def cam_img(self):
        self.init_cam(True)
        # fft_array = np.fft.fft(numpy_array[750][1015:1075])
        # fft_array = fft_array[5:-5]
        # max_index = np.where(np.max(fft_array) == fft_array)[0][0]
        # print(np.angle(fft_array[max_index]))
        # print(numpy_array[750][1015:1075])
        #

    def cam_cont_img(self):
        self.init_cam(False)

    def cam_phi(self):
        pass

    def set_area1(self):
        poly_1 = draw_polygon.draw_polygon(self.ax1, self.fig)
        print(poly_1)

    def set_area2(self):
        poly_2 = draw_polygon.draw_polygon(self.ax1, self.fig)
        print(poly_2)

    def on_close(self):
        plt.close(self.fig)
        self.win.destroy()
