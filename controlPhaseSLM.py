import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import numpy as np
from tkinter.filedialog import askopenfilename, asksaveasfilename
import json
import os
import time
import phase_settings
import preview_window
import publish_window


class main_screen(object):
    """"""

    def __init__(self, parent):
        """Constructor"""
        self.main_win = parent
        self.main_win.title('SLM Phase Control')

        self.main_win.columnconfigure(0, minsize=250, weight=1)
        self.main_win.rowconfigure(2, minsize=100, weight=1)
        self.pub_win = None

        # creating frames
        frm_top = tk.Frame(self.main_win)
        self.frm_mid = tk.Frame(self.main_win)
        frm_bot = tk.Frame(self.main_win)
        frm_topb = tk.Frame(frm_top)
        self.frm_side = tk.Frame(self.main_win)

        # Creating labels
        lbl_title = tk.Label(
            self.main_win,
            text='Control Phase',
            font=tkFont.Font(family='Lucida Grande', size=20))
        lbl_screen = tk.Label(frm_top, text='SLM screen position:')

        # Creating buttons
        but_prev = tk.Button(frm_bot, text='Preview', command=self.open_prev)
        but_pub = tk.Button(frm_bot, text='Publish', command=self.open_pub)
        but_exit = tk.Button(frm_bot, text='EXIT', command=self.exit_prog)
        but_save = tk.Button(frm_topb, text='Save Settings', command=self.save)
        but_load = tk.Button(frm_topb, text='Load Settings', command=self.load)
        self.but_scan = tk.Button(
            frm_topb, text='Scan Options', command=self.scan_options,
            relief="raised")

        # Creating entry
        self.ent_scr = tk.Entry(frm_top, width=15)
        self.ent_scr.insert(tk.END, '+right+down')

        # Setting up general structure
        lbl_title.grid(row=0, column=0, sticky='ew')
        frm_top.grid(row=1, column=0, sticky='ew')
        self.frm_mid.grid(row=2, column=0, sticky='nsew')
        frm_bot.grid(row=3, column=0)
        self.frm_side.grid(row=1, column=1, sticky='nsew')

        # Setting up top frame
        lbl_screen.grid(row=0, column=0, sticky='e', padx=10, pady=10)
        self.ent_scr.grid(row=0, column=1, sticky='w', padx=(0, 10))
        self.setup_box(frm_top)  # sets up the checkboxes separately
        frm_topb.grid(row=1, column=1, sticky='nsew')
        but_save.grid(row=0, padx=5, pady=5)
        but_load.grid(row=1, padx=5)
        self.but_scan.grid(row=2, padx=5, pady=5)

        # Setting up bot frame
        but_prev.grid(row=0, column=0, padx=10, pady=5, ipadx=5)
        but_pub.grid(row=0, column=1, pady=5, ipadx=5)
        but_exit.grid(row=0, column=2, padx=10, pady=5, ipadx=5)

    def open_prev(self):
        if self.but_scan['relief'] == 'sunken':
            if self.but_enable_scan['relief'] == 'sunken':
                if self.strvar_delay.get() != '':
                    delay = float(self.strvar_delay.get())
                else:
                    delay = 1
                filelist = self.load_filelist()
                var = tk.IntVar()
                for filepath in filelist:
                    if self.var_stop_scan.get():
                        self.var_stop_scan.set(0)
                        return
                    root.after(int(delay*1000), var.set, 1)
                    self.load(filepath)
                    self.prev_win = preview_window.prev_screen(self)
                    root.wait_variable(var)
            else:
                self.prev_win = preview_window.prev_screen(self)
        else:
            self.prev_win = preview_window.prev_screen(self)

    def open_pub(self):
        if self.but_scan['relief'] == 'sunken':
            if self.but_enable_scan['relief'] == 'sunken':
                if self.strvar_delay.get() != '':
                    delay = float(self.strvar_delay.get())
                else:
                    delay = 1
                filelist = self.load_filelist()
                var = tk.IntVar()
                for filepath in filelist:
                    if self.var_stop_scan.get():
                        self.var_stop_scan.set(0)
                        return
                    root.after(int(delay*1000), var.set, 1)
                    self.load(filepath)
                    if self.pub_win is not None:
                        self.pub_win.update_img(self.get_phase())
                    else:
                        self.pub_win = publish_window.pub_screen(
                            self, self.ent_scr.get())
                    root.wait_variable(var)
            else:
                if self.pub_win is not None:
                    self.pub_win.update_img(self.get_phase())
                else:
                    self.pub_win = publish_window.pub_screen(
                        self, self.ent_scr.get())
        else:
            if self.pub_win is not None:
                self.pub_win.update_img(self.get_phase())
            else:
                self.pub_win = publish_window.pub_screen(self,
                                                         self.ent_scr.get())

    def pub_win_closed(self):
        self.pub_win = None

    def setup_box(self, frm_):
        frm_box = tk.LabelFrame(frm_, text='Phases enabled')
        frm_box.grid(column=0)
        self.types = phase_settings.types()  # reads in  different phase types
        self.vars = []  # init a list holding the variables from the boxes
        self.phase_refs = []  # init a list to hold the references to types
        self.active_phases = []
        self.commands = [self.start_stop_0, self.start_stop_1,
                         self.start_stop_2, self.start_stop_3,
                         self.start_stop_4, self.start_stop_5,
                         self.start_stop_6]
        for ind, typ in enumerate(self.types):
            self.var_ = (tk.IntVar())
            self.vars.append(self.var_)
            self.phase_refs.append(0)  # just filling it with 0 to start with
            self.box_ = tk.Checkbutton(frm_box, text=typ,
                                       variable=self.vars[ind],
                                       onvalue=1, offvalue=0,
                                       command=self.commands[ind])
            self.box_.grid(row=ind, sticky='w')

# It is a bit not so nice, but box commands cant send args. currently able to
# run 5 different phase types
    def start_stop_0(self):
        self.start_stop_t(0)

    def start_stop_1(self):
        self.start_stop_t(1)

    def start_stop_2(self):
        self.start_stop_t(2)

    def start_stop_3(self):
        self.start_stop_t(3)

    def start_stop_4(self):
        self.start_stop_t(4)

    def start_stop_5(self):
        self.start_stop_t(5)

    def start_stop_6(self):
        self.start_stop_t(6)

    def start_stop_t(self, ind):
        if self.vars[ind].get() == 1:
            self.phase_refs[ind] = phase_settings.new_type(self.frm_mid,
                                                           self.types[ind])
            self.active_phases.append(self.phase_refs[ind])
        else:
            if self.phase_refs[ind] != 0:
                self.phase_refs[ind].close_()
                self.active_phases.remove(self.phase_refs[ind])
            self.phase_refs[ind] = 0

#   gets the phase from the active phase types. 0-2pi is 0-254
    def get_phase(self):
        phase = np.zeros([600, 792])
        for phase_types in self.active_phases:
            phase += phase_types.phase()
        return phase

    def save(self, filepath=None):
        """Save the current settings as a new file."""
        if filepath is None:
            filepath = asksaveasfilename(
                defaultextension='txt',
                filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')]
            )
            if not filepath:
                return
        dict = {}
        with open(filepath, 'w') as f:
            for phase in self.active_phases:
                dict[phase.name_()] = phase.save_()
            f.write(json.dumps(dict))

    def load(self, filepath=None):
        if filepath is None:
            filepath = askopenfilename(
                filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')]
            )
            if not filepath:
                return
        with open(filepath, 'r') as f:
            dics = json.loads(f.read())
        for num, var in enumerate(self.vars):  # resetting everything
            var.set(0)
            self.commands[num]()
        for key in dics.keys():
            try:
                ind = self.types.index(key)
                self.vars[ind].set(1)
                self.commands[ind]()
                self.phase_refs[ind].load_(dics[key])
            except ValueError:
                print(key + ' value problems.')

    def scan_options(self):
        if self.but_scan.config('relief')[-1] == 'sunken':
            self.so_frm.destroy()
            self.but_scan.config(relief="raised")
        else:
            self.but_scan.config(relief="sunken")
            self.so_frm = tk.LabelFrame(self.frm_side, text='Scan options')
            self.so_frm.grid(row=0, sticky='nsew')

            # creating frames
            frm_scpar = tk.Frame(self.so_frm)
            frm_file = tk.Frame(self.so_frm)
            frm_load = tk.Frame(self.so_frm)
            frm_but = tk.Frame(self.so_frm)

            # creating labels
            lbl_scpar = tk.Label(frm_scpar, text='Scan parameter')
            lbl_val = tk.Label(frm_scpar, text='Value (strt:stop:num)')
            lbl_actf = tk.Label(frm_file, text='Active file:')
            self.lbl_file = tk.Label(frm_file, text='')
            lbl_delay = tk.Label(
                frm_load, text='Delay between each phase [s]:')

            # creating entries
            self.cbx_scpar = ttk.Combobox(
                frm_scpar, values=['Select'], postcommand=self.scan_params)
            self.cbx_scpar.current(0)
            vcmd = (self.frm_side.register(self.callback))
            self.strvar_val = tk.StringVar()
            ent_val = tk.Entry(frm_scpar,  width=10,  validate='all',
                               validatecommand=(vcmd, '%d', '%P', '%S'),
                               textvariable=self.strvar_val)
            self.strvar_delay = tk.StringVar()
            ent_delay = tk.Entry(frm_load, width=5, validate='all',
                                 validatecommand=(vcmd, '%d', '%P', '%S'),
                                 textvariable=self.strvar_delay)

            # creating buttons
            self.but_crt = tk.Button(
                self.so_frm, text='Create loading file',
                command=self.create_loadingfile)
            but_openload = tk.Button(
                self.so_frm, text='Open existing loading file',
                command=self.open_loadingfile)
            self.but_enable_scan = tk.Button(
                frm_but, text='Enable scan', command=self.enable_scan)
            but_stop_scan = tk.Button(
                frm_but, text='Stop scan', command=self.stop_scan)

            # setup
            frm_scpar.grid(row=0, sticky='nsew')
            self.but_crt.grid(row=1, sticky='ew')
            but_openload.grid(row=2, sticky='ew')
            frm_file.grid(row=3, sticky='w')
            frm_load.grid(row=4, sticky='nsew')
            frm_but.grid(row=5)

            self.but_enable_scan.grid(row=0, column=0, padx=5, pady=5)
            but_stop_scan.grid(row=0, column=1, padx=5, pady=5)

            lbl_scpar.grid(row=0, column=0, sticky='e')
            lbl_val.grid(row=1, column=0, sticky='e')
            self.cbx_scpar.grid(row=0, column=1, sticky='w')
            ent_val.grid(row=1, column=1, sticky='w')

            lbl_actf.grid(row=0, column=0)
            self.lbl_file.grid(row=0, column=1)

            lbl_delay.grid(row=0, column=0, sticky='e')
            ent_delay.grid(row=0, column=1, sticky='w')

    def callback(self, action, P, text):
        # action=1 -> insert
        if(action == '1'):
            if text in '0123456789.-+:':
                #    try:
                #        float(P)
                return True
            #    except ValueError:
            #        return False
            else:
                return False
        else:
            return True

    def scan_params(self):
        scparams = []
        for phase in self.active_phases:
            phparam = phase.save_()
            for param in phparam.keys():
                scparams.append(phase.name_() + ':' + param)
        self.cbx_scpar['values'] = scparams
        return

    def create_loadingfile(self):
        if self.strvar_val.get() != '':
            strval = self.strvar_val.get()
            listval = strval.split(':', 3)
            try:
                strt = float(listval[0])
                stop = float(listval[1])
                num = int(listval[2])
                val_range = np.linspace(strt, stop, num)
            except (ValueError, IndexError) as err:
                self.but_crt['text'] = f'Create loading file : {err}'
                return

        else:
            print('Empty value')
            return
        print(f'{strt}_{stop}_{num}')

        cwd = os.getcwd()
        print('current cwd is {}'.format(cwd))
        dirstr = '\\SLM_phase_scan_files'
        if not os.path.exists(cwd + dirstr):
            os.mkdir(cwd + dirstr)
        # create folder
        scparam = self.cbx_scpar.get().split(':')
        folder_str = '\\{}_{}_{}_{}_{}'.format(
            scparam[0], scparam[1], strt, stop, num)
        cwd = cwd + dirstr + folder_str
        if not os.path.exists(cwd):
            os.mkdir(cwd)

        # create file for filepaths
        ind = self.types.index(scparam[0])
        param_dic = self.phase_refs[ind].save_()
        with open(cwd + '\\' + 'filepaths.txt', 'w') as logfile:
            for val in val_range:
                param_dic[scparam[1]] = val
                self.phase_refs[ind].load_(param_dic)
                filepath = f'{cwd}\\{val}.txt'
                print(filepath)
                self.save(filepath)
                logfile.write(filepath + '\n')
        self.lbl_file['text'] = cwd + '\\' + 'filepaths.txt'

        self.but_crt['text'] = 'Create loading file : OK'
        return

    def open_loadingfile(self):
        filepath = askopenfilename(
            filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')]
        )
        if not filepath:
            return
        self.lbl_file['text'] = f'{filepath}'
        return

    def enable_scan(self):
        self.var_stop_scan = tk.IntVar(value=0)
        if self.but_enable_scan['relief'] == 'sunken':
            self.but_enable_scan['relief'] = 'raised'
            self.but_enable_scan['text'] = 'Enable scan'
        else:
            self.but_enable_scan['relief'] = 'sunken'
            self.but_enable_scan['text'] = 'Scan enabled'
        return

    def load_filelist(self):
        filelistpath = self.lbl_file['text']
        with open(filelistpath, 'r') as f:
            text = f.read()
            stringlist = text.split('\n')
            return stringlist[0:-1]

    def stop_scan(self):
        self.var_stop_scan.set(1)
        return

    def exit_prog(self):
        self.main_win.destroy()


root = tk.Tk()

main = main_screen(root)


root.mainloop()
