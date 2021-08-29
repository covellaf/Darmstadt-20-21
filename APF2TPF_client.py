# created by F Covella - Jan, Feb 2021

import sys
# difference from python3
import Tkinter as tk 
from APF2TPF_GUI import FrameLogo, FrameInstructions, FrameSelectArgs, FrameActions
import INTXMM_library
import APF2TPF_3options
from TPF_library import TPF


def main(argv):

    # AUTOMATIC MODE
    if argv[1] == "-a": 
        inputs = "inputs/"
	# "C:\\Users\\Francesca Covella\\Documents\\Project_first\\APF2TPF_Local_Py3\\inputs\\" 
        outputs = "outputs/"
        rrrr_vv = argv[2]
        apf_file = inputs + rrrr_vv + "/" + rrrr_vv + ".APF"
        epo_file = inputs + rrrr_vv + "/" + rrrr_vv + ".EPO"
        lst_of_sequences = ['GESTAN02', 'KEDATA02', 'LEDATA02', 'DEBPG100', 'DEBPG200']
        myDict = INTXMM_library.create_dictionary_from_apf(apf_file, lst_of_sequences)
        if len(argv) == 3 :
            # generate all files
            APF2TPF_3options.all_seq_all_time(epo_file, outputs, rrrr_vv, myDict)
        if len(argv) == 4 :
            # generate all instances of one sequence
	        if argv[3] in lst_of_sequences:	
                seq = argv[3]
	        else: 
	            sys.exit( "The sequence name is not recognised" )
            APF2TPF_3options.one_seq_all_time(epo_file, outputs, rrrr_vv, seq, myDict)
        if len(argv) == 5 :
            # generate only one tpf
            if argv[3] in lst_of_sequences:	
                seq = argv[3]
	        else: 
	            sys.exit( "The sequence name is not recognised" )
            time = argv[4]
            APF2TPF_3options.one_seq_one_time(epo_file, outputs, rrrr_vv, seq, time, myDict) 


    # INTERACTIVE MODE
    elif argv[1] == "-i" :
        # ---- create the GUI object ---- 
        master = tk.Tk()
        master.title("APF to TPF file converter and generating tool")
        frame0 = FrameLogo(master)
        frame1 = FrameInstructions(master)
        frame2 = FrameSelectArgs(master)
        frame3 = FrameActions(master, frame2)
        frame2.button = frame3.btn_main
        frame3.assign_function_to_button(frame3.btn_main)
        master.resizable(0, 0) 
        master.mainloop()


if __name__ == "__main__":
    main(sys.argv)
