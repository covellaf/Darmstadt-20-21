# F Covella 25 Jan 21
from tkinter import Label, LabelFrame, Radiobutton, Scale, Button, IntVar, HORIZONTAL, VERTICAL, NORMAL, DISABLED
from tkinter.filedialog import asksaveasfilename
import tkinter as tk 
from PIL import Image, ImageTk
from TPF_library import TPF 
from PST_generator import PST


class FrameZero:
    def __init__(self, master):
        self.labelframe0 = LabelFrame(master, text="Mission", font=('Helvetica', 12), fg='black')  
        self.labelframe0.grid(row=1, column=0, padx=200, pady=5, sticky='E') 
        self.picture = self.create_logo("C:\\Users\\Francesca Covella\\Documents\\Project_second\\GUI in python\\Integral_logo.png", 1, 1, 60) #("Integral_logo.png", 1, 1, 60)
        # absolute path of picture
        self.signature = self.create_signature("Author: Francesca Covella", 2, 1)

    def create_signature(self, author, row, column):
        signature = Label(self.labelframe0, text=author, font=('Helvetica', 12), fg='#00bfff') #or bfff
        signature.grid(row=row, column=column, padx=0, sticky='WE')
        # W = right, E = left, WE = centre
        return signature


    def create_logo(self, image_name, row, column, padx):
        pic = Image.open(image_name)
        resized_pic = pic.resize((150, 150), Image.ANTIALIAS)
        pic = ImageTk.PhotoImage(resized_pic)
        pic_label = Label(self.labelframe0, image=pic)
        pic_label.image = pic
        pic_label.grid(row=row, column=column, padx=padx, sticky='E')
        return pic_label


class FrameOne:
    def __init__(self, master):
        # FRAME 1 (Radio buttons to select preferences)
        self.labelframe1 = LabelFrame(master, text="Target configuration", font=('Helvetica', 12), fg='black')   
        self.labelframe1.grid(row=1, column=0, padx=100, pady=0, ipadx=10, ipady=5, sticky='W') 
        self.R1 = IntVar()
        self.R2 = IntVar()
        self.R3 = IntVar()
        self.btn1_line1, self.btn2_line1 = self.create_line("OMC flat field calibration", 2, 1, 'yes', 'no', self.R1)
        self.btn1_line2, self.btn2_line2 = self.create_line("JEMX-1", 3, 1, 'on', 'off', self.R2)
        self.btn1_line3, self.btn2_line3 = self.create_line("JEMX-2", 4, 1, 'on', 'off', self.R3)
    

    def create_line(self, text, row, column, test1, test2, var):
        tk.Label(self.labelframe1, text=text, font=('Helvetica', 12), fg='blue').grid(row=row, sticky='E')
        btn1 = self.create_radio_button(test1, 1, row, column, var)
        btn2 = self.create_radio_button(test2, 0, row, column+1, var)
        return btn1, btn2
    

    def create_radio_button(self, test, value, row, column, var):
        btn = Radiobutton(self.labelframe1, text=test, font=('Helvetica', 12), fg='black', padx=20, variable=var, value=value)
        btn.grid(row=row, column=column)
        return btn


    # def change_slider_to(self, slider, new_value):
    #     slider.configure(to=new_value)
    

    # def change_slider_from(self, slider, new_value):
    #     slider.configure(from_=new_value)
    

    # def change_slider_state(self, slider, state):
    #     slider.configure(state=state)


    def change_slider_range(self, slider, from_val, to_val):
        slider.configure(from_=from_val, to=to_val)


    def change_line1_buttons_callback(self, slider):
        # self.btn1_line1.configure(command=lambda: self.change_slider_to(slider, 64))
        self.btn1_line1.configure(command=lambda: self.change_slider_range(slider, 0, 64))
        # self.btn2_line1.configure(command=lambda: self.change_slider_to(slider, 127))
        self.btn2_line1.configure(command=lambda: self.change_slider_range(slider, 0, 127))


    def change_line2_buttons_callback(self, slider):
        self.btn1_line2.configure(command=lambda: self.change_slider_range(slider, 1, 127))
        self.btn2_line2.configure(command=lambda: self.change_slider_range(slider, 0, 0))


    def change_line3_buttons_callback(self, slider):
        self.btn1_line3.configure(command=lambda: self.change_slider_range(slider, 1, 127))
        self.btn2_line3.configure(command=lambda: self.change_slider_range(slider, 0, 0))


class FrameTwo:
    def __init__(self, master):
        # FRAME 2 (Sliders)
        self.labelframe2 = LabelFrame(master, text="Number of programmable slots assigned to", font=('Helvetica', 12), fg='black')  
        # self.labelframe2.grid(row=2, column=0, padx=20, pady=10, ipadx=10, ipady=0, sticky='EW')
        self.labelframe2.grid(row=2, column=0, padx=20, pady=10, ipadx=10, ipady=0, sticky='W')

        self.lb_1, self.sld_1 = self.create_slider("IBIS", 2, 1, 0, 90)
        self.lb_2, self.sld_2 = self.create_slider("SPI", 3, 1, 0, 127)
        self.lb_3, self.sld_3 = self.create_slider("JEMX-1", 4, 1, 0, 0)#127) 
        self.lb_4, self.sld_4 = self.create_slider("JEMX-2", 5, 1, 0, 0)#127) 
        self.lb_5, self.sld_5 = self.create_slider("OMC", 6, 1, 0, 127)
        self.lb_6, self.sld_6 = self.create_slider("LOAD AND DUMP", 7, 1, 0,  150)
        self.sliders_sum = 0
        self.lb_7 = Label(self.labelframe2, text="You can still assign 150 slots", font=('Helvetica', 12), fg='dark green')     
        self.lb_7.grid(row=18, column=2, sticky='E')
        self.lb_8 = Label(self.labelframe2, text=" ", font=('Helvetica', 12), fg='dark green')     
        self.lb_8.grid(row=9, column=2, sticky='E')
        self.values = []
        self.remaining_slots = 0
        # fixed slots
        self.f1 = 90
        self.f2 = 8
        self.f3 = 0
        self.f4 = 1


    def create_slider(self, test, row, column, init_value, end_value):
        lb = Label(self.labelframe2, text=test, font=('Helvetica', 12), fg='blue')
        lb.grid(row=row,column=column, sticky='E')
        sld = Scale(self.labelframe2, from_=init_value, to=end_value,  length=600, orient=HORIZONTAL, font=('Helvetica', 12), fg='black', command=self.slider_callback)
        sld.grid(row=row, column=column+1)
        return lb, sld


    def sum_all_slider_value(self, s1, s2, s3, s4, s5, s6):
        self.sliders_sum = s1 + s2 + s3 + s4 + s5 + s6
        return self.sliders_sum
    

    def slider_callback(self, sld_val):
        v1 = self.sld_1.get()
        v2 = self.sld_2.get()
        v3 = self.sld_3.get()
        v4 = self.sld_4.get()
        v5 = self.sld_5.get()
        v6 = self.sld_6.get()
        # Modify the label message based on self.sliders_sum
        self.sum_all_slider_value(v1, v2, v3, v4, v5, v6)
        if self.sliders_sum <= 150 : 
            # update the message every time to avoid overlapping when the order of magnitude of the sum changes :) 
            self.lb_7.configure(text=" ")
            # Modify the label message saying how many left
            self.lb_7 = Label(self.labelframe2, text=f"You can still assign {150-self.sliders_sum} slots", font=('Helvetica', 12), fg='dark green')     
            self.lb_7.grid(row=18,column=2, sticky='E') 
            self.lb_8.configure(text="The remining slots will be assigned to NO TRANSACTION")  
            if self.sliders_sum == 150:
                self.lb_8.configure(text=" ")     
            self.change_button_state(NORMAL, self.button) 
            self.remaining_slots = 150-self.sliders_sum
            self.pass_values_to_botton(self.button, self.remaining_slots)  

            self.lb_ibis.configure(text="{} + {} = {}".format(v1, self.f1, v1+self.f1))
            self.lb_spi.configure(text="{} + {} = {}".format(v2, self.f2, v2+self.f2))
            self.lb_jemx1.configure(text="{} + {} = {}".format(v3, self.f3, v3+self.f3))
            self.lb_jemx2.configure(text="{} + {} = {}".format(v4, self.f3, v4+self.f3))

            self.lb_omc.configure(text="{} + {} = {}".format(v5, self.f4, v5+self.f4))
            self.lb_padu.configure(text="{} + {} = {}".format(v6, self.f3, v6+self.f3))

        else:
            self.lb_8.configure(text=" ")
            self.lb_7.configure(text=" ")
            # Modify label message in red saying how many in excess
            self.lb_7 = Label(self.labelframe2, text=f"You have assigned {self.sliders_sum-150} too many slots", font=('Helvetica', 12), fg='red')
            self.lb_7.grid(row=18,column=2, sticky='E')        
            self.change_button_state(DISABLED, self.button)   

            self.lb_ibis.configure(text="{}".format(self.f1))
            self.lb_spi.configure(text="{}".format(self.f2))
            self.lb_jemx1.configure(text="{}".format(self.f3))
            self.lb_jemx2.configure(text="{}".format(self.f3))
            self.lb_omc.configure(text="{}".format(self.f4))
            self.lb_padu.configure(text="{}".format(self.f3))


    def change_button_state(self, state, button):
        button.configure(state=state)

    
    def pass_values_to_botton(self, button, remaining_slots):
        self.values = [self.sld_1.get(),
        self.sld_2.get(),
        self.sld_3.get(),
        self.sld_4.get(),
        self.sld_5.get(),
        self.sld_6.get(), self.remaining_slots]


class FrameThree():
    # FRAME 3 (Buttons generate TPF and quit application)
    def __init__(self, master, frame_Two, pst_obj): 
        self.frame2 = frame_Two
        self.pst_obj = pst_obj
        #self.tpf_obj = tpf_obj
        self.labelframe3 = LabelFrame(text="Actions", font=('Helvetica', 12), fg='black')  
        self.labelframe3.grid(row=3, column=0, padx=400, pady=5, ipadx=0, ipady=5, sticky='NW') 
        self.inputs1 = []
        self.inputs2 = []
        self.btn_main = self.create_button("Generate .TPF", 2, 1, 20, 5, None)
        self.btn_quit = self.create_button("Exit", 2, 2, 15, 5, master.quit)
        self.filepath = " "


    def create_button(self, test, row, column, padx, pady, function):
        btn = Button(self.labelframe3, text=test, font=('Helvetica', 12), fg='black', padx=padx, command=function)
        btn.grid(row=row,column=column, padx=padx, pady=pady, sticky='E')
        return btn


    def get_slots_name_and_path(self):
        ''' Giving all the functionalities to the button:
        1. passing the slider values to the PstSequence
        2. write the file
        3. save the current file as a new file '''
        self.inputs1 = ["E"]*150
        self.inputs2 = self.frame2.values
        self.pst_obj.parameters_for_PST(self.inputs1, self.inputs2)

        self.filepath = asksaveasfilename(defaultextension="txt",
            filetypes=[("Text Files", "*.TPF"), ("All Files", "*.*")],)
        self.pst_obj.write_tpf(self.filepath)


    def assign_function_to_button(self, button):
        button.configure(command=self.get_slots_name_and_path)


class FrameFour():
    # FRAME 4 (Shows the current fixed allocation of the PST and an updated sum of the total slots)
    def __init__(self, master, frame_two):
        self.frame2 = frame_two 
        self.labelframe4 = LabelFrame(master, text="Total number of slots", font=('Helvetica', 12), fg='black')  
        self.labelframe4.grid(row=2, column=0, padx=50, pady=5, ipadx=0, ipady=0, sticky='E')
        self.explaining = Label(self.labelframe4, text="(Programmable + Fixed) = Total", font=('Helvetica', 12), fg='black')
        self.explaining.grid(row=3, column=0, sticky='E')

        self.mk_lb_ibis = Label(self.labelframe4, text="{}".format(90), font=('Helvetica', 12), width=18, fg='blue')   
        self.mk_lb_ibis.grid(row=4,column=0, ipadx=10, sticky='WE') 
        self.mk_lb_spi = Label(self.labelframe4, text="{}".format(8), font=('Helvetica', 12), width=18, fg='blue')   
        self.mk_lb_spi.grid(row=5,column=0, ipadx=10, sticky='WE') 
        self.mk_lb_jemx1 = Label(self.labelframe4, text="{}".format(0), font=('Helvetica', 12), width=18, fg='blue')   
        self.mk_lb_jemx1.grid(row=6,column=0, ipadx=10, sticky='WE') 
        self.mk_lb_jemx2 = Label(self.labelframe4, text="{}".format(0), font=('Helvetica', 12), width=18, fg='blue')   
        self.mk_lb_jemx2.grid(row=7,column=0, ipadx=10, sticky='WE') 
        self.mk_lb_omc = Label(self.labelframe4, text="{}".format(1), font=('Helvetica', 12), width=18, fg='blue')   
        self.mk_lb_omc.grid(row=8,column=0, ipadx=10, sticky='WE') 

        self.mk_lb_padu = Label(self.labelframe4, text="{}".format(0), font=('Helvetica', 12), width=18, fg='blue')   
        self.mk_lb_padu.grid(row=9,column=0, ipadx=10, sticky='WE') 
        