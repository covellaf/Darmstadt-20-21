#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

# =============================================================================
# Created By  : Francesca Covella
# Created Date: April - May 2021
# ============================================================================= 

import os
import pandas as pd 
import tkinter as tk 
from TMPrint_GUI import FrameLogo, FrameInstructions, FrameActions
import TMPrint_library as TM


def main():
    """
    This method creates the GUI object and opens the GUI
    """
    master = tk.Tk()
    master.title("TMPrint: Automatic Plots Generation Tool")
    frame0 = FrameLogo(master)
    frame1 = FrameInstructions(master)
    frame2 = FrameActions(master)
    frame2.assign_function_to_button(frame2.btn_main)
    master.resizable(0, 0) 
    master.mainloop()


if __name__ == "__main__":
    main()
