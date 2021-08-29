# F Covella 08 Feb 21
from TPF_library import TPF 


class PST(TPF):
    def __init__(self):    
        super().__init__()
        self.lst_of_slots_repetition = []
    
    def parameters_for_PST(self, val_type, values_from_sliders):
        """
        creates the specific parameter structure for the PST programmable slots
        and returns the list of parameters for the PST table to be written
        """
        # for pst the val_type is a list of 150 (n elements) E
        self.value_type = val_type  
        # save input values
        self.lst_of_slots_repetition = values_from_sliders
        lst_of_slots_values = ["PST2 IBIS1", "PST2 SPI1", "PST2 JEM X1", "PST TM PK JEM X2", "PST2 OMC", "PST2 LO DU", "PST2 NOTRANS"]
        # create param list
        param_value = [item for item, count in zip(lst_of_slots_values, self.lst_of_slots_repetition) for i in range(count)]
        idx = [i for i in range(1, 151)] 
        index = [str(i).zfill(3) for i in idx]
        param_name = ["TMS" + j + "  " for j in index]
        self.lst_of_parameters = [param_name[i] + " " + val_type[i] + " " + param_value[i] for i in range(len(param_name))]
        # print(self.lst_of_parameters)
        return self.lst_of_parameters
        
        

# F Covella 08 Jan 21
# --- in the database --- predefined indeces
        # idxs = [146, 23, 147, 31, 39, 47,55, 63, 69, 134, 82, 80, 127, 75, 84, 120, 87, 24, 90, 89, 
        #         32, 40, 48, 56, 64, 133, 126, 119, 70, 76, 113, 107, 11, 145, 22, 6, 
        #         140, 17, 77, 25, 132, 33, 41, 49, 125, 118, 112, 106, 101, 10, 144, 21, 5, 139, 
        #         16, 57, 2, 136, 13, 26, 34, 42, 50, 58, 65, 131, 124, 117, 111, 105, 100, 71, 78,
        #         85, 9, 143, 20, 27, 130, 35, 43, 51, 123, 116, 110, 104, 99, 8, 142, 19, 4, 138, 
        #         15, 59, 66, 72, 28, 129, 36, 44, 54, 122, 115, 109, 60, 67, 103, 7, 141, 18, 3, 
        #         137, 14, 73, 1, 135, 12, 29, 128, 37, 45, 53, 121, 114, 108, 102, 98, 97, 96, 61, 
        #         95, 30, 38, 46, 52, 62, 68, 74, 79, 81, 83, 86, 88, 92, 148, 149, 91, 94, 93, 150]
        # idxs_py = [k - 1 for k in idxs]
        # reshuffle 
        # param_value = [param[i] for i in idxs_py]
        # # string part to add to TMS when writing the file
        # index = [str(i).zfill(3) for i in idxs]
        # # add TMS to the index and two spaces to have 0-7 chars allocated to the name
        # param_name = ["TMS" + j + "  " for j in index]
        # for n, t, v in zip(param_name, val_type, param_value):
        #     self.set_parameter(n, t, v)
        #     self.create_parameters_sublist()
        
        #     print(self.set_parameter(n, t, v))
        # return self.create_parameters_sublist()