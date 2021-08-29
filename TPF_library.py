#  created by F Covella - Dec 2020 to Feb 2021
from os.path import join
import sys
import re
import datetime
import INTXMM_library 

class TPF:

    def __init__(self):
        ### Structure of the headers
        # Header 1 attributes
        self.header_h1 = " "
        self.task_name = " "                    # Column 0-7    (mandatory)
        self.spare_h1_08 = " "                  # Column 8      (spare)
        self.task_type = " "                    # Column 9      (mandatory: C = Command / S = Sequence)
        self.spare_h1_10 = " "                  # Column 10     (spare)
        self.parameter_set_name = "{0:8}".format(" ")           # Column 11-18  (optional)
        self.spare_h1_19 = " "                  # Column 19     (spare)
        self.parameter_value_set_name = "{0:8}".format(" ")     # Column 20-27  (optional)
        # Header 2 attributes
        self.header_h2 = ""
        self.spare_h2_00 = "{0:11}".format(" ")          # Column 0-10   (spare)
        self.destination = " "                           # Column 11     (mandatory: A = AutoStack / M = ManualStack)
        self.spare_h2_12 = " "                           # Column 12     (spare)
        self.source = " "                                # Column 13     (mandatory: F = FDS / S = SOC)
        self.spare_h2_14 = " "                           # Column 14     (spare)
        self.number_of_parameters = " "                  # Column 15-17  (mandatory: The number of data records supplied as part of the TPF body)
        # Header 3 attributes
        self.header_h3 = " "
        self.release_time = "{0:20}".format(" ")         # Column 00-19  (optional: YYYY-MM-DDThh:mm:ssZ)
        self.spare_h3_20 = " "                           # Column 20     (spare)
        self.earliest_time = "{0:20}".format(" ")        # Column 21-40  (optional: YYYY-MM-DDThh:mm:ssZ)
        self.spare_h3_41 = " "                           # Column 41     (spare)
        self.latest_time = "{0:20}".format(" ")          # Column 42-61  (optional: YYYY-MM-DDThh:mm:ssZ)
        # Header 4 attributes
        self.header_h4 = " "
        self.execution_time = "{0:20}".format(" ")          # Column 00-19   (optional: YYYY-MM-DDThh:mm:ssZ)
        self.spare_h4_20 = " "                              # Column 20     (spare)
        self.sub_schedule_ID = "{0:5}".format(" ")          # Column 21-25  (optional)
        # Header 5 attributes
        self.header_h5 = " "                                # Column 0-x    (optional: for information/printout only)
        self.lst_of_headers = []
        
        ### Structure of the body
        self.parameter = " "
        self.parameter_name = " "           # Column 0-7 (mandatory)
        self.spare_p_08 = " "               # Column 8     (spare)
        self.value_type = " "               # Column 9 (optional: R=raw -default-, E=engineering, C=command, S=sequence)
        self.spare_p_10 = " "               # Column 10     (spare)
        self.parameter_value = " "          # Column 11-30 (mandatory if value type is specified)
        self.spare_p_31 = " "               # Column 31     (spare)
        self.value_unit = ""                # Column 32-35 (optional)
        self.spare_p_36 = " "               # Column 36     (spare)
        self.value_radix = " "              # Column 37 (optional: D for Decimal, H for Hexadecimal, O for Octal)
        self.spare_p_38 = " "               # Column 38     (spare)
        #self.comment = "{0:42}".format(" ")# Column 39-80  (optional) Not used by SCOS-2000
        self.lst_of_parameters = []
        # Location where you want to save the file
        # self.path = ""                       # Asked to the user in the write_tpf method

    # ------------------- Header 1 methods ------------------- 
    def get_task_name(self):
        return self.task_name


    def set_task_name(self, input_name):
        """
        Sets the task name and checks its length and that it is not void (very unlikely)
        """
        # OPTION 1: check that the length it is exactly 8 chars
        # assert (len(input_name) == 8 and input_name != "        "), "TASK NAME is 8 characters long."
        # self.task_name = input_name
        # OPTION 2: pad the remaining chars with spaces
        self.task_name = INTXMM_library.pad_with_spaces_notVoid(input_name, 8)
        self.update_header1()


    def get_task_type(self):
        return self.task_type


    def set_task_type(self, input_type):
        """
        Sets the task type and checks that it is either C or S
        """
        assert (input_type == "C" or input_type == "S"), "TASK TYPE can be either C for Command or S for Sequence."
        self.task_type = input_type
        self.update_header1()


    def get_parameter_set_name(self):
        return self.parameter_set_name


    def set_parameter_set_name(self, input_parameter_set):
        # self.parameter_set_name = input_parameter_set
        self.parameter_set_name = INTXMM_library.pad_with_spaces(input_parameter_set, 8)
        self.update_header1()


    def get_parameter_value_set_name(self):
        return self.parameter_value_set_name


    def set_parameter_value_set_name(self, input_parameter_value_set):
        # self.parameter_value_set_name = input_parameter_value_set
        self.parameter_value_set_name = INTXMM_library.pad_with_spaces(input_parameter_value_set, 8)
        self.update_header1()


    def set_header1(self, input_name, input_type, input_parameter_set="{0:8}".format(" "), input_parameter_value_set="{0:8}".format(" ")):
        self.set_task_name(input_name)
        self.set_task_type(input_type)                           
        self.set_parameter_set_name(input_parameter_set)
        self.set_parameter_value_set_name(input_parameter_value_set)
        self.update_header1()


    def get_header1(self):
        return self.header_h1


    def update_header1(self):    
        self.header_h1 = self.get_task_name()+self.spare_h1_08+self.get_task_type()+self.spare_h1_10+self.get_parameter_set_name()+self.spare_h1_19+self.get_parameter_value_set_name()


    # ------------------- Header 2 methods ------------------- 
    def get_destination(self):
        return self.destination


    def set_destination(self, input_destination):
        """
        Sets the destination and checks it's A or M
        """
        assert (input_destination == "A" or input_destination == "M"), "DESTINATION can be either A for AutoStack or M for ManualStack."
        self.destination = input_destination
        self.update_header2()


    def get_source(self):
        return self.source


    def set_source(self, input_source):
        """
        Sets the source and checks it's F or S
        """
        assert (input_source == "F" or input_source == "S"), "SOURCE can be either F for FDS or S for SOC."
        self.source = input_source
        self.update_header2()


    def get_number_of_parameters(self):
        return self.number_of_parameters


    def set_number_of_parameters(self, input_number_of_parameters):
        """
        Sets the number of parameters
        """
        self.number_of_parameters = INTXMM_library.pad_with_leading_zero_notVoid_notZero(input_number_of_parameters, 3)
        # assert (len(input__number_of_parameters) == 3 and input__number_of_parameters.isdecimal()), "No. OF PARAMETERS is 3 characters long and shall contain only numbers."
        # self.number_of_parameters = input_number_of_parameters
        self.update_header2()


    def set_header2(self, input_destination, input_source, input_number_of_parameters):
        self.set_destination(input_destination)
        self.set_source(input_source)                           
        self.set_number_of_parameters(input_number_of_parameters)
        self.update_header2()


    def get_header2(self):
        return self.header_h2


    def update_header2(self):    
        self.header_h2 = self.spare_h2_00+self.get_destination()+self.spare_h2_12 + self.get_source()+self.spare_h2_14 + self.get_number_of_parameters()


    # ------------------- Header 3 methods ------------------- 
    def get_release_time(self):
        return self.release_time


    def set_release_time(self, input_release_time):
        """
        Sets the release time and checks its format, if given
        """
        self.release_time = input_release_time
        if self.release_time != "{0:20}".format(" ") :
            INTXMM_library.check_time_format(self.release_time)
        else:
            pass
        self.update_header3()


    def get_earliest_time(self):
        return self.earliest_time


    def set_earliest_time(self, input_earliest_time):
        """
        Sets the earliest time and checks its format, if given
        """
        self.earliest_time = input_earliest_time
        if self.earliest_time != "{0:20}".format(" ") :
            INTXMM_library.check_time_format(self.earliest_time)
        else:
            pass
        self.update_header3()


    def get_latest_time(self):
        return self.latest_time


    def set_latest_time(self, input_latest_time):
        """
        Sets the latest time and checks its format, if given
        """
        self.latest_time = input_latest_time
        if self.latest_time != "{0:20}".format(" ") :
            INTXMM_library.check_time_format(self.latest_time)
        else:
            pass
        self.update_header3()


    def set_header3(self, input_release_time="{0:20}".format(" "), input_earliest_time="{0:20}".format(" "), input_latest_time="{0:20}".format(" ")):
        self.set_release_time(input_release_time)
        self.set_earliest_time(input_earliest_time)                           
        self.set_latest_time(input_latest_time)
        self.update_header3()


    def get_header3(self):
        return self.header_h3


    def update_header3(self):    
        self.header_h3 = self.get_release_time()+self.spare_h3_20+self.get_earliest_time()+self.spare_h3_41+self.get_latest_time()


    # ------------------- Header 4 methods ------------------- 
    def get_execution_time(self):
        return self.execution_time


    def set_execution_time(self, input_execution_time):
        """
        Sets the execution time and checks its format, if given
        """
        self.execution_time = input_execution_time
        if self.execution_time != "{0:20}".format(" ") :
            INTXMM_library.check_time_format(self.execution_time)
        else:
            pass
        self.update_header4()


    def get_sub_schedule_ID(self):
        return self.sub_schedule_ID
   

    def set_sub_schedule_ID(self, input_sub_schedule_ID):
        """
        Sets the Sub Scheduled id and checks it's 5 chars long
        """
        self.sub_schedule_ID = input_sub_schedule_ID
        assert (len(self.sub_schedule_ID) == 5), "SUB SCHEDULED ID is 5 characters long."
        self.update_header4()
        

    def set_header4(self, input_execution_time="{0:20}".format(" "), input_sub_schedule_ID="{0:5}".format(" ")):
        self.set_execution_time(input_execution_time)
        self.set_sub_schedule_ID(input_sub_schedule_ID)                           
        self.update_header4()


    def get_header4(self):
        return self.header_h4


    def update_header4(self):    
        self.header_h4 = self.get_execution_time()+self.spare_h4_20+self.get_sub_schedule_ID()


# ------------------- Header 5 methods -------------------  
    def get_header5(self):
        return self.header_h5
        
    
    def set_header5(self, input_info=" "):
        self.info = input_info
        self.update_header5()


    def update_header5(self):    
        self.header_h5 = self.info


    def create_headers_sublist(self):
        self.lst_of_headers.append(self.get_header1())
        self.lst_of_headers.append(self.get_header2()) 
        self.lst_of_headers.append(self.get_header3())
        self.lst_of_headers.append(self.get_header4())
        self.lst_of_headers.append(self.get_header5())
        return self.lst_of_headers


# ------------------- Parameters methods ------------------- 
    def set_parameter(self, input_parameter_name, input_value_type, input_parameter_value, input_value_unit="", input_value_radix=""):
        self.parameter_name = input_parameter_name
        self.value_type = input_value_type
        self.parameter_value = input_parameter_value
        self.value_unit = input_value_unit
        self.value_radix = input_value_radix
        self.update_parameter()


    def get_parameter(self):
        return self.parameter
    

    def update_parameter(self):
        self.parameter = self.parameter_name+self.spare_p_08+self.value_type+self.spare_p_10+self.parameter_value+self.spare_p_31+self.value_unit+self.spare_p_36+self.value_radix+self.spare_p_38

    
    def create_parameters_sublist(self):
        self.lst_of_parameters.append(self.get_parameter())


    def assign_param(self, lst_p):
        self.lst_of_parameters = lst_p


    def print_hello(self):
        print("hello hello")
    

# ------------------- Writing the TPF file ------------------- 

    def write_tpf(self, file_name):
        with open(file_name, "w+") as tpf:
            for l in self.lst_of_headers:
                tpf.write("%s \n" %l)
            for item in self.lst_of_parameters:
                if item.endswith("\n") == True: 
                    tpf.writelines(item) 
                else:     
                    tpf.write("%s \n" %item)
            tpf.close()    
            print('Something worked well!')
