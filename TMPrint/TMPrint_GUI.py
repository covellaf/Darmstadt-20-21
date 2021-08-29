# =============================================================================
# Created By  : Francesca Covella
# Created Date: March - May 2021
# ============================================================================= 

from tkinter import Frame, Label, Entry, LabelFrame, StringVar, Button, IntVar, HORIZONTAL, VERTICAL, NORMAL, DISABLED
from tkinter.filedialog import asksaveasfilename, askdirectory, askopenfile
import tkinter as tk 
from PIL import Image, ImageTk
import os
import subprocess
import shlex
from TMPrint_client import plot_tool
from configuration import Constant
from watch_folder import Api


class FrameLogo:
    """
    This class creates the logo frame
    """
    def __init__(self, master):
        self.labelframe0 = LabelFrame(master, text="Mission", font=('Helvetica', 12), fg='black')  
        self.labelframe0.grid(row=1, column=0, padx=(620, 20), pady=5, sticky='W')        
        self.pic_location = Constant.LOGO_PATH 
        self.picture = self.create_logo(self.pic_location, 1, 1, 60) 
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
    """
    This class sets the instructions
    """
    def __init__(self, master):
        self.labelframe1 = LabelFrame(master, text="Instructions", font=('Helvetica', 12), fg='black')  
        self.labelframe1.grid(row=1, column=0, padx=(100, 200), pady=5, sticky='W') 
        self.line1 = self.create_instruction("Welcome to the Automatic TM Print Plotting Tool ! ", 1, 0)
        # self.line2 = self.create_instruction("This tool is useful to carry out ACC patch", 2, 0)
        self.line3 = self.create_instruction("Please follow the following steps:", 3, 0)
        self.line4 = self.create_instruction("1. Press 'Select Slew directory' and choose the slew of interest.", 4, 0)
        self.line5 = self.create_instruction("2. Press 'Generate plots' to generate and save the plots.", 5, 0)
        self.line6 = self.create_instruction("3. Press 'Open viewer' if you want to see the plots or press 'Exit'.", 6, 0)
        self.line7 = self.create_instruction("4. If in 3. you selected 'Open viewer', then select 'Image' >>> 'Open' ", 8, 0)
        self.line8 = self.create_instruction("    to choose the folder of interest in the SLW_PLOTS directory ", 9, 0)
        self.line9 = self.create_instruction("Thanks for using this application and have a lovely day.", 10, 0)
        self.line10 = self.create_instruction("Arrivederci e grazie!", 11, 0)


    def create_instruction(self, text, row, column):
        instruction = Label(self.labelframe1, text=text, width=60, anchor='nw', font=('Helvetica', 11), fg='black')
        instruction.grid(row=row, column=column, sticky='E')
        return instruction


class FrameActions():
    """
    This class implements the PLOT GENERATION functionality and the OPEN VIEWER 
    """
    def __init__(self, master): 
       
        self.labelframe2 = LabelFrame(text="Actions", font=('Helvetica', 12), fg='black')  
        self.labelframe2.grid(row=2, column=0, padx=(20, 20), pady=(5, 5), sticky='EW') 
        self.inputs = Constant.WHERE_FROM    # "/home/imcsuser/TMPrint/SLW_DATA"        
        self.outputs = Constant.WHERE_TO     # "/home/imcsuser/TMPrint/SLW_PLOTS"
        self.inputs_fslash = self.inputs + "/" 
        self.btn_select_directory = self.create_button("Select Slew directory", 2, 1, 20, 5, NORMAL, lambda: self.select_slew_dir(self.inputs_fslash))
        self.lb_dir = self.create_label("Selected directory: {}".format(""), 2, 2, 'grey')
        self.btn_main = self.create_button("Generate plots", 3, 1, 20, 5, DISABLED, None)
        self.saved_in1 = self.create_label("Plots generated and saved in: {}".format(""), 3, 2, "gray")
        self.saved_in2 = self.create_label(" ", 4, 2, "dark green")
        self.btn_viwer = self.create_button("Open viwer", 5, 1, 20, 5, DISABLED, self.open_viewer)
        self.btn_quit = self.create_button("Exit", 5, 2, 20, 5, NORMAL, master.quit)
        self.directory_name = " "
        self.directory = " "


    def create_label(self, text, row, column, color):
        lb = Label(self.labelframe2, text=text, width=60, font=('Helvetica', 12), fg=color)
        lb.grid(row=row, column=column, sticky='WE')
        return lb


    def create_button(self, test, row, column, padx, pady, state, function):
        btn = Button(self.labelframe2, text=test, font=('Helvetica', 12), fg='black', padx=padx, state=state, command=function)
        btn.grid(row=row,column=column, padx=padx, pady=pady, sticky='E')
        return btn


    def change_button_state(self, state, button):
        button.configure(state=state)


    def select_slew_dir(self, folder):
        ''' give the user the option to select the folder from SLW_DATA 
        (previsouly copied from imcd)
        '''
        self.directory = askdirectory(initialdir=folder) #(**mustexist)
        if len(self.directory) > 0:
            self.change_button_state(NORMAL, self.btn_main)
        self.directory_name = self.directory.split("/", -1)[-1]
        self.lb_dir.configure(text="Selected directory: {}".format(self.directory_name), fg='dark green')
        return self.directory_name


    def display_location(self, location):
        self.saved_in1.configure(fg="dark green") 
        self.saved_in2.configure(text="{}".format(location))
    

    def save_files(self):
        ''' 
        Giving the functionalities to the button via the cronjob which calls the plot_tool function
        # example: Api.api("/home/imcsuser/TMPrint/SLW_DATA", "SLW_573802")
        # originally: plot_tool(self.directory_name, self.inputs, self.outputs)
        '''
        self.change_button_state(DISABLED, self.btn_select_directory)
        Api.api(self.inputs, self.directory_name)
        self.display_location(self.outputs)
        self.change_button_state(NORMAL, self.btn_viwer)
        self.btn_quit.configure(state=NORMAL)
        self.btn_main.configure(state=DISABLED) 


    def assign_function_to_button(self, button):
        button.configure(command=self.save_files)


    def open_viewer(self):
        command = "eog"
        shlex.quote(command)
        subprocess.run(command, shell=True)
        self.change_button_state(DISABLED, self.btn_viwer)

# end
