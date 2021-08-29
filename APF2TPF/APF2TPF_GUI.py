# created by F Covella - end Jan to beginning of Feb 2021

# difference in importing libraries from python 3
from Tkinter import Toplevel, Frame, Label, Canvas, LabelFrame, Radiobutton, StringVar, OptionMenu, Button, IntVar, HORIZONTAL, VERTICAL, NORMAL, DISABLED, Entry
from ttk import Progressbar, Style, Scrollbar, Treeview
from tkFileDialog import asksaveasfilename, askdirectory, askopenfile
import Tkinter as tk 
from PIL import Image, ImageTk
from TPF_library import TPF 
import INTXMM_library
import APF2TPF_3options
from datetime import datetime
import time


class FrameLogo:
    def __init__(self, master):
        self.labelframe0 = LabelFrame(master, text="Mission", font=('Helvetica', 12), fg='black')  
        self.labelframe0.grid(row=1, column=0, padx=(800, 20), pady=5, sticky='W') 
        # The padding options padx and pady of the grid and pack methods can take a 2-tuple 
        # that represent the left/right and top/bottom padding.
        self.pic_location = "Integral_logo.png"
	    # relative path of the figure, it used to be absolute path: 
	    # C:\\Users\\Francesca Covella\\Documents\\Project_first\\APF2TPF_Local_Py3\\
        self.picture = self.create_logo(self.pic_location, 1, 1, 60) #("Integral_logo.png", 1, 1, 60) 
        # absolute path of picture
        self.signature = self.create_signature("Author: Francesca Covella", 2, 1)


    def create_signature(self, author, row, column):
        signature = Label(self.labelframe0, text=author, font=('Helvetica', 12), fg='#00bfff') #or bfff
        signature.grid(row=row, column=column, padx=0, sticky='WE')
        return signature

    
    def create_logo(self, image_name, row, column, padx):
        pic = Image.open(image_name)
        resized_pic = pic.resize((150, 150), Image.ANTIALIAS)
        pic = ImageTk.PhotoImage(resized_pic)
        pic_label = Label(self.labelframe0, image=pic)
        pic_label.image = pic
        pic_label.grid(row=row, column=column, padx=padx, sticky='E')
        return pic_label


class FrameInstructions:
    def __init__(self, master):
        # Please select the following
        # 1. Folder containing the .APF file you wish you convert to .TPF 
        # 2. The sequence name you want to retrieve the .TPF for, or select "ALL" (sequences)
        # 3. If you did not press "ALL" in step 2, select the time of uplink for 
        # the sequence you are interested in, or select "ALL" (uplink times)
        # 4. Press the "GENERATE .TPF" button
        # The generation of the file(s) might take a few seconds.
        # Thanks for using this application and have a lovely day.
        self.labelframe1 = LabelFrame(master, text="Instructions", font=('Helvetica', 12), fg='black')  
        self.labelframe1.grid(row=1, column=0, padx=20, pady=5, sticky='W') 
        self.line1 = self.create_instruction("Welcome! Please follow these steps: ", 1, 0)
        self.line2 = self.create_instruction("1. Click on the folder corresponding to the revolution and version of interest and press OK", 2, 0)
        self.line3 = self.create_instruction("2. Press the 'LOAD .APF' button", 3, 0)
        self.line4 = self.create_instruction("3. Select the sequence of interest, or select 'ALL' (sequences)", 4, 0)
        self.line5 = self.create_instruction("4. If you did not press 'ALL' in step 2, select the time of uplink for the", 5, 0)
        self.line6 = self.create_instruction("   selected sequence, or select 'ALL' (uplink times)", 6, 0)
        self.line7 = self.create_instruction("5. Save your Options and press the 'GENERATE .TPF' button", 7, 0)
        self.line8 = self.create_instruction(" ", 8, 0)
        self.line9 = self.create_instruction("The generation of the file(s) might take a few seconds.", 9, 0)
        self.line10 = self.create_instruction("Thanks for using this application and have a lovely day. Arrivederci e grazie!", 10, 0)


    def create_instruction(self, text, row, column):
        instruction = Label(self.labelframe1, text=text, width=80, anchor='nw', font=('Helvetica', 11), fg='black')
        instruction.grid(row=row, column=column, sticky='E')
        return instruction


class FrameSelectArgs:
    def __init__(self, master):
        # Set Revolution, Version, Sequence and Time
        self.labelframe2 = LabelFrame(master, text="Options", font=('Helvetica', 12), fg='black')  
        self.labelframe2.grid(row=2, column=0, padx=(20, 20), pady=(5, 5), sticky='EW') 
        self.directory = " "
        self.apf_file = ''
        self.epo_file = ''
        self.rrrr_vv = "" 
        self.lb_rrrr_vv = self.create_label("Select the correct directory: [ RRRR_VV ]      ", 1, 0, 'blue')
        self.inputs = "inputs/"
	# C:\\Users\\Francesca Covella\\Documents\\Project_first\\APF2TPF_Local_Py3\\inputs\\
        self.btn_rrrr_vv = self.create_button("Search folder", 1, 1, 10, 5, NORMAL, lambda: self.select_apf_dir(self.inputs))
        # Guide the user in scosii_homedir/MPS/data
        self.btn_loading = self.create_button("LOAD .APF", 1, 2, 10, 5, DISABLED, self.parse_uplink_time)
        self.loading_bar = self.create_progressbar(2, 2)
        self.seq = self.create_label("Select sequence: [ SEQUENCE NAME / ALL ]", 3, 0, 'gray')
        self.list_of_s = ['GESTAN02', 'KEDATA02', 'LEDATA02', 'DEBPG100', 'DEBPG200']
        self.sDict = {}
        self.time_chosen = []
        # which button has been pressed the latest
        self.flag = None
        self.btn_GESTAN02 = self.create_button("GESTAN02", 3, 1, 10, 5, DISABLED, self.GESTAN02_uplink_time)
        self.btn_KEDATA02 = self.create_button("KEDATA02", 3, 2, 10, 5, DISABLED, self.KEDATA02_uplink_time)
        self.btn_LEDATA02 = self.create_button("LEDATA02", 4, 1, 10, 5, DISABLED, self.LEDATA02_uplink_time)
        self.btn_DEBPG100 = self.create_button("DEBPG100", 4, 2, 10, 5, DISABLED, self.DEBPG100_uplink_time)
        self.btn_DEBPG200 = self.create_button("DEBPG200", 5, 1, 10, 5, DISABLED, self.DEBPG200_uplink_time)
        self.btn_ALL      = self.create_button("ALL", 5, 2, 10, 5, DISABLED, self.all_sequences)
        self.btn_reselect_seq = self.create_button("Reselect Sequence", 6, 2, 10, 5, DISABLED, self.reactivate_buttons)
        self.time = self.create_label("Time of uplink: [ YYYY-MM-DDThh:mm:ssZ ]", 7, 0, 'gray')
        self.btn_save_options = self.create_button("Save Options", 8, 1, 20, 5, DISABLED, self.save_options)


    def create_button(self, test, row, column, padx, pady, state, function):
        btn = Button(self.labelframe2, text=test, font=('Helvetica', 12), fg='black', padx=padx, state=state, command=function)
        btn.grid(row=row, column=column, padx=padx, pady=pady, sticky='E')
        return btn


    def create_button_in_toplevel_window(self, location, text, row, column, padx, pady, state, function):
        btn = Button(location, text=text, font=('Helvetica', 12), fg='black', width = 40, padx=padx, state=state, command=function)
        btn.grid(row=row, column=column, padx=padx, pady=pady, sticky='E')
        return btn


    def create_label(self, text, row, column, color):
        lb = Label(self.labelframe2, text=text, width=50, font=('Helvetica', 12), fg=color)
        lb.grid(row=row, column=column, sticky='E')
        return lb


    def create_progressbar(self, row, column):
        s = Style()
        s.theme_use('clam')
        s.configure("pink.Horizontal.TProgressbar", foreground='pink', background='pink')
        p = Progressbar(self.labelframe2, style="pink.Horizontal.TProgressbar", orient = HORIZONTAL, 
              length = 120, mode = 'determinate')
        p.grid(row=row, column=column, padx=(10, 10), sticky='E')
        return p
    

    def bar(self): 
        import time 
        self.loading_bar['value'] = 33
        self.labelframe2.update_idletasks() 
        time.sleep(0.5) 
        self.loading_bar['value'] = 66
        self.labelframe2.update_idletasks() 
        time.sleep(0.5) 
        self.loading_bar['value'] = 100
        self.labelframe2.update_idletasks() 
        time.sleep(0.5) 
    

    def enable_menu(self, menu):
        menu.configure(state=NORMAL)


    def disable_menu(self, menu):
        menu.configure(state=DISABLED)


    def change_button_state(self, state, button):
        button.configure(state=state)


    def create_toplevel_window(self, title):
        tl = Toplevel(self.labelframe2)
        tl.resizable(0, 0) 
        tl.title(title)
        # create a canvas
        canvas = Canvas(tl)
        canvas.grid(row=0, column=0, sticky="W")
        # scrolling bar
        sbar = Scrollbar(tl, orient=VERTICAL, command=canvas.yview)
        sbar.grid(row=0, column=1, sticky="ns")
        # configure
        canvas.configure(yscrollcommand = sbar.set)
        # bind
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        frame = Frame(canvas)
        canvas.create_window((0,0), window=frame, anchor="nw")
        return frame


    def select_apf_dir(self, folder):
        ''' give the user te option to pick the .APF that he/she wants to use to create
        the .TPF(s)'''
        self.directory = askdirectory(initialdir=folder) #(**mustexist)
        if len(self.directory) > 0:
            self.change_button_state(NORMAL, self.btn_loading)
        self.rrrr_vv = self.directory[(len(self.directory)-7):(len(self.directory))]
        self.apf_file = self.directory + "/" + self.rrrr_vv + ".APF"
        self.epo_file = self.directory + "/" + self.rrrr_vv + ".EPO"
        self.lb_rrrr_vv.configure(text="Select the correct directory: [ {} ] ".format(self.rrrr_vv), fg='dark green')
        print(self.apf_file)
        return self.rrrr_vv, self.apf_file, self.epo_file


    def parse_uplink_time(self):
        self.sDict = INTXMM_library.create_dictionary_from_apf(self.apf_file, self.list_of_s)
        self.bar()
        print("dictionary created!")
        self.seq.configure(fg='blue')
        self.change_button_state(NORMAL, self.btn_GESTAN02)
        self.change_button_state(NORMAL, self.btn_KEDATA02)
        self.change_button_state(NORMAL, self.btn_LEDATA02)
        self.change_button_state(NORMAL, self.btn_DEBPG100)
        self.change_button_state(NORMAL, self.btn_DEBPG200)
        self.change_button_state(NORMAL, self.btn_ALL)


    def all_sequences(self):
        self.change_button_state(DISABLED, self.btn_GESTAN02)
        self.change_button_state(DISABLED, self.btn_KEDATA02)
        self.change_button_state(DISABLED, self.btn_LEDATA02)
        self.change_button_state(DISABLED, self.btn_DEBPG100)
        self.change_button_state(DISABLED, self.btn_DEBPG200)
        self.change_button_state(NORMAL, self.btn_reselect_seq)
        self.seq.configure(text="Select sequence: [ ALL ] ", fg='dark green')
        self.time.configure(text="Time of uplink: [ ALL ]", fg="dark green")
        self.change_button_state(NORMAL, self.btn_save_options)
        self.flag = self.sDict.keys() #"ALL"
        self.time_chosen = "ALL"


    def GESTAN02_uplink_time(self):
        # disactivate all the other sequences
        self.change_button_state(DISABLED, self.btn_KEDATA02)
        self.change_button_state(DISABLED, self.btn_LEDATA02)
        self.change_button_state(DISABLED, self.btn_DEBPG100)
        self.change_button_state(DISABLED, self.btn_DEBPG200)
        self.change_button_state(DISABLED, self.btn_ALL)
        self.change_button_state(NORMAL, self.btn_reselect_seq)
        self.flag = "GESTAN02"
        self.seq.configure(text="Select sequence: [ {} ] ".format(self.flag), fg='dark green')
        tl_GESTAN02 = self.create_toplevel_window("GESTAN02 uplink time(s)")
        row = 0
        column = 0 
        if len(self.sDict["GESTAN02"]["uplink_times"]) > 1:
            self.create_button_in_toplevel_window(tl_GESTAN02, "all instances", row, column, 10, 5, NORMAL, self.get_all_uplink_times)
        for elem in self.sDict["GESTAN02"]["uplink_times"]:
            row += 1 
            self.create_button_in_toplevel_window(tl_GESTAN02, elem, row, column, 10, 5, NORMAL, lambda t=elem: self.get_uplink_time(t))


    def KEDATA02_uplink_time(self):
        self.change_button_state(DISABLED, self.btn_GESTAN02)
        self.change_button_state(DISABLED, self.btn_LEDATA02)
        self.change_button_state(DISABLED, self.btn_DEBPG100)
        self.change_button_state(DISABLED, self.btn_DEBPG200)
        self.change_button_state(DISABLED, self.btn_ALL)
        self.change_button_state(NORMAL, self.btn_reselect_seq)
        self.flag = "KEDATA02"
        self.seq.configure(text="Select sequence: [ {} ] ".format(self.flag), fg='dark green')
        tl_KEDATA02 = self.create_toplevel_window("KEDATA02 uplink time(s)")
        row = 0
        column = 0 
        if len(self.sDict["KEDATA02"]["uplink_times"]) > 1:
            self.create_button_in_toplevel_window(tl_KEDATA02, "all instances", row, column, 10, 5, NORMAL, self.get_all_uplink_times)
        for elem in self.sDict["KEDATA02"]["uplink_times"]:
            row += 1 
            self.create_button_in_toplevel_window(tl_KEDATA02, elem, row, column, 10, 5, NORMAL, lambda t=elem: self.get_uplink_time(t))

    
    def LEDATA02_uplink_time(self):
        self.change_button_state(DISABLED, self.btn_GESTAN02)
        self.change_button_state(DISABLED, self.btn_KEDATA02)
        self.change_button_state(DISABLED, self.btn_DEBPG100)
        self.change_button_state(DISABLED, self.btn_DEBPG200)
        self.change_button_state(DISABLED, self.btn_ALL)
        self.change_button_state(NORMAL, self.btn_reselect_seq)
        self.flag = "LEDATA02"
        self.seq.configure(text="Select sequence: [ {} ] ".format(self.flag), fg='dark green')
        tl_LEDATA02 = self.create_toplevel_window("LEDATA02 uplink time(s)")
        row = 0
        column = 0 
        if len(self.sDict["LEDATA02"]["uplink_times"]) > 1:
            self.create_button_in_toplevel_window(tl_LEDATA02, "all instances", row, column, 10, 5, NORMAL, self.get_all_uplink_times)
        for elem in self.sDict["LEDATA02"]["uplink_times"]:
            row += 1 
            self.create_button_in_toplevel_window(tl_LEDATA02, elem, row, column, 10, 5, NORMAL, lambda t=elem: self.get_uplink_time(t))


    def DEBPG100_uplink_time(self):
        self.change_button_state(DISABLED, self.btn_GESTAN02)
        self.change_button_state(DISABLED, self.btn_KEDATA02)
        self.change_button_state(DISABLED, self.btn_LEDATA02)
        self.change_button_state(DISABLED, self.btn_DEBPG200)
        self.change_button_state(DISABLED, self.btn_ALL)
        self.change_button_state(NORMAL, self.btn_reselect_seq)
        self.flag = "DEBPG100"
        self.seq.configure(text="Select sequence: [ {} ] ".format(self.flag), fg='dark green')
        tl_DEBPG100 = self.create_toplevel_window("DEBPG100 uplink time(s)")
        row = 0
        column = 0 
        if len(self.sDict["DEBPG100"]["uplink_times"]) > 1:
            self.create_button_in_toplevel_window(tl_DEBPG100, "all instances", row, column, 10, 5, NORMAL, self.get_all_uplink_times)
        for elem in self.sDict["DEBPG100"]["uplink_times"]:
            row += 1 
            self.create_button_in_toplevel_window(tl_DEBPG100, elem, row, column, 10, 5, NORMAL, lambda t=elem: self.get_uplink_time(t))

    
    def DEBPG200_uplink_time(self):
        self.change_button_state(DISABLED, self.btn_GESTAN02)
        self.change_button_state(DISABLED, self.btn_KEDATA02)
        self.change_button_state(DISABLED, self.btn_LEDATA02)
        self.change_button_state(DISABLED, self.btn_DEBPG100)
        self.change_button_state(DISABLED, self.btn_ALL)
        self.change_button_state(NORMAL, self.btn_reselect_seq)
        self.flag = "DEBPG200"
        self.seq.configure(text="Select sequence: [ {} ] ".format(self.flag), fg='dark green')
        tl_DEBPG200 = self.create_toplevel_window("DEBPG200 uplink time(s)")
        row = 0
        column = 0 
        if len(self.sDict["DEBPG200"]["uplink_times"]) > 1:
            self.create_button_in_toplevel_window(tl_DEBPG200, "all instances", row, column, 10, 5, NORMAL, self.get_all_uplink_times)
        for elem in self.sDict["DEBPG200"]["uplink_times"]:
            row += 1 
            self.create_button_in_toplevel_window(tl_DEBPG200, elem, row, column, 10, 5, NORMAL, lambda t=elem: self.get_uplink_time(t))


    def reactivate_buttons(self):
        self.change_button_state(NORMAL, self.btn_GESTAN02)
        self.change_button_state(NORMAL, self.btn_KEDATA02)
        self.change_button_state(NORMAL, self.btn_LEDATA02)
        self.change_button_state(NORMAL, self.btn_DEBPG100)
        self.change_button_state(NORMAL, self.btn_DEBPG200)
        self.change_button_state(NORMAL, self.btn_ALL)
        self.seq.configure(text="Select sequence: [ SEQUENCE NAME / ALL ]", fg='blue')
        self.time.configure(text = "Time of uplink: [ YYYY-MM-DDThh:mm:ssZ ]", fg='gray')
        self.change_button_state(DISABLED, self.btn_save_options)


    def get_uplink_time(self, t): 
        self.time.configure(text="Time of uplink: [ {} ]".format(t), fg="dark green")
        self.time_chosen = t
        self.change_button_state(NORMAL, self.btn_save_options)


    def get_all_uplink_times(self):
        self.time_chosen = self.sDict[self.flag]["uplink_times"]
        self.time.configure(text="Time of uplink: [ ALL ]", fg="dark green")
        self.change_button_state(NORMAL, self.btn_save_options)


    def save_options(self):
        # DISACTIVATE BUTTONS, ACTIVATE GEN TPF
        self.change_button_state(DISABLED, self.btn_rrrr_vv)
        self.change_button_state(DISABLED, self.btn_loading)
        self.change_button_state(DISABLED, self.btn_GESTAN02)
        self.change_button_state(DISABLED, self.btn_KEDATA02)
        self.change_button_state(DISABLED, self.btn_LEDATA02)
        self.change_button_state(DISABLED, self.btn_DEBPG100)
        self.change_button_state(DISABLED, self.btn_DEBPG200)
        self.change_button_state(DISABLED, self.btn_ALL)
        self.change_button_state(DISABLED, self.btn_reselect_seq)
        self.change_button_state(DISABLED, self.btn_save_options)
        self.change_button_state(NORMAL, self.button)


class FrameActions():
    def __init__(self, master, frame_args): 
        self.frame_arguments = frame_args
        self.labelframe3 = LabelFrame(text="Actions", font=('Helvetica', 12), fg='black')  
        self.labelframe3.grid(row=3, column=0, padx=(20, 20), pady=(5, 5), ipadx=0, ipady=5, sticky='EW')
        self.btn_main = self.create_button("Generate .TPF", 2, 1, 20, 5, DISABLED, None)
        self.loading_bar = self.create_progressbar(2, 2)
        self.saved_in1 = self.create_label("The .TPF(s) have been generated and saved here: ", 2, 3, "gray")
        self.saved_in2 = self.create_label(" ", 3, 3, "dark green")
        self.btn_quit = self.create_button("Exit", 3, 1, 20, 5, NORMAL, master.quit)
        self.epo_file = " "
        self.rrrr_vv = " "
        self.key = " "
        self.utimes = " " 
        self.last_valid_time = " "
        self.sDict = {}
        self.name = " "
        self.outputs = "outputs/"
	# C:\\Users\\Francesca Covella\\Documents\\Project_first\\APF2TPF_Local_Py3\\outputs\\


    def create_label(self, text, row, column, color):
        lb = Label(self.labelframe3, text=text, width=80, font=('Helvetica', 12), fg=color)
        lb.grid(row=row, column=column, sticky='WE')
        return lb


    def create_button(self, test, row, column, padx, pady, state, function):
        btn = Button(self.labelframe3, text=test, font=('Helvetica', 12), fg='black', padx=padx, state=state, command=function)
        btn.grid(row=row,column=column, padx=padx, pady=pady, sticky='E')
        return btn


    def create_progressbar(self, row, column):
        s = Style()
        s.theme_use('clam')
        s.configure("pink.Horizontal.TProgressbar", foreground='pink', background='pink')
        p = Progressbar(self.labelframe3, style="pink.Horizontal.TProgressbar", orient = HORIZONTAL, 
              length = 180, mode = 'determinate')
        p.grid(row=row, column=column, padx=(10, 10), sticky='E')
        return p


    def bar(self): 
        import time 
        self.loading_bar['value'] = 25
        self.labelframe3.update_idletasks() 
        time.sleep(0.5) 
        self.loading_bar['value'] = 50
        self.labelframe3.update_idletasks() 
        time.sleep(0.5) 
        self.loading_bar['value'] = 75
        self.labelframe3.update_idletasks() 
        time.sleep(0.5)
        self.loading_bar['value'] = 100
        self.labelframe3.update_idletasks() 
        time.sleep(0.5)


    def get_arguments(self):
        # important to pass args between frames
        self.epo_file = self.frame_arguments.epo_file
        self.rrrr_vv = self.frame_arguments.rrrr_vv
        self.key = self.frame_arguments.flag
        self.utimes = self.frame_arguments.time_chosen 
        self.sDict = self.frame_arguments.sDict
        return self.epo_file, self.rrrr_vv, self.key, self.utimes, self.sDict


    def write_files(self):
        self.get_arguments()
        self.btn_quit.configure(state=DISABLED)
        # all sequences and all times
        if len(list(self.key)) > 1 and self.utimes == "ALL":
            APF2TPF_3options.all_seq_all_time(self.epo_file, self.outputs, self.rrrr_vv, self.sDict)
        # generate all instances of one sequence
        if isinstance(self.key, list) == False and isinstance(self.utimes, list) == True:
            APF2TPF_3options.one_seq_all_time(self.epo_file, self.outputs, self.rrrr_vv, self.key, self.sDict)
        # generate only one tpf   
        if isinstance(self.key, list) == False and (isinstance(self.utimes, list) == False and self.utimes != "ALL"):
            APF2TPF_3options.one_seq_one_time(self.epo_file, self.outputs, self.rrrr_vv, self.key, self.utimes, self.sDict) 
        self.bar()
        

    def display_location(self, location):
        self.saved_in1.configure(fg="dark green") 
        self.saved_in2.configure(text="{}".format(location))
    
    
    def save_files(self):
        ''' 
        Giving the functionalities to the button:
            write the file and save the current file as a new file 
            '''
        print('start writing')
        self.write_files()
        self.display_location(self.outputs)
        print("finish writing!")
        self.btn_quit.configure(state=NORMAL)
        self.btn_main.configure(state=DISABLED) 
        


    def assign_function_to_button(self, button):
        button.configure(command=self.save_files)
