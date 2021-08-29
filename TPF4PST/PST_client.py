import tkinter as tk 
from TPF_library import TPF 
from PST_generator import PST
from PST_generator_GUI import FrameZero, FrameOne, FrameTwo, FrameThree, FrameFour

def main():
# ---- create the GUI object ---- 
    master = tk.Tk()
    master.title("TPF generation tool for PST bandwidth re-allocation")
    frame0 = FrameZero(master)
    frame1 = FrameOne(master)
    frame2 = FrameTwo(master)
    frame1.change_line1_buttons_callback(frame2.sld_5)
    frame1.change_line2_buttons_callback(frame2.sld_3)
    frame1.change_line3_buttons_callback(frame2.sld_4)

# ---- create the PST object (for the command sequence) ---- 
    DEPST256 = PST()

# ---- create the object headers ----    
    DEPST256.set_header1("DEPST256", "S")
    DEPST256.set_header2("M", "S", "150")
    DEPST256.set_header3()
    DEPST256.set_header4()
    DEPST256.set_header5()
    DEPST256.create_headers_sublist()
    

# ---- link the code functionalities with the GUI functionalities ----
    frame3 = FrameThree(master, frame2, DEPST256)
    frame2.button = frame3.btn_main
    frame3.assign_function_to_button(frame3.btn_main)
    frame4 = FrameFour(master, frame2)
    frame2.lb_ibis = frame4.mk_lb_ibis
    frame2.lb_spi = frame4.mk_lb_spi
    frame2.lb_jemx1 = frame4.mk_lb_jemx1
    frame2.lb_jemx2 = frame4.mk_lb_jemx2
    frame2.lb_omc = frame4.mk_lb_omc
    frame2.lb_padu = frame4.mk_lb_padu

    master.resizable(0, 0) 
    master.mainloop()


if __name__ == "__main__":
    main()
