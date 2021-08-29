# =============================================================================
# Created By  : Francesca Covella
# Created Date: March - May 2021
# =============================================================================
import os
import re
import pandas as pd 
import TMPrint_library as TM
import SIM_LOG_client as Sim
from TMPrint_DICT import *
from configuration import Constant


####################################### data reading and formatting #######################################


def plot_tool(Dir, PATH_FROM=None, WHERE_TO=None):
    """
    This method creates the outputs (excel sheets and plots)
    """
    if PATH_FROM is None:
	    PATH_FROM = Constant.WHERE_FROM
    if WHERE_TO is None:
        WHERE_TO = Constant.WHERE_TO

    # create output directory
    path_output_folder = WHERE_TO + "/" + Dir + "/"
    TM.make_output_folder(path_output_folder)

    log_filename = ""
    path = PATH_FROM + "/" + Dir + "/"
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:  
            if '.txt' in file:
                files.append(os.path.join(r, file))
            if 'SimLog' in file:
                log_filename = os.path.join(r, file) 


    if len(files) == 0:
        Constant.error = 1
        TM.delete_output_folder(path_output_folder, Constant.error)
        raise Exception("There are no .txt files in the chosen input folder")  
             

    sheets_excel = []
    for f in files:
        if (Dir+"/"+Dir in f):
            f = (f.split(Dir+"_", -1)[-1])
            f = re.split("_[0-9]+", f)[0]
            sheets_excel.append(f)

    if len(sheets_excel) == 0:
        Constant.error = 1
        TM.delete_output_folder(path_output_folder, Constant.error)
        raise Exception("There are no valid .txt files in the selected folder")  
    
    # take a HK as a reference for the start and end of slew
    hk_files = []
    for f in files:
        if "HK" in f:
            hk_files.append(f)
    hk = hk_files[0]

    words_to_skip = ['FULL PRINTOUT FOR SATELLITE: INTEGRAL', 'STREAMS:  65535']

    # create intermediate file list
    lst_processed1 = []
    lst_processed2 = []

    for n in range(len(sheets_excel)):
        lst_processed1.append(path+"processed1_"+str(n+1))
        lst_processed2.append(path+"processed2_"+str(n+1))

    # create the dataframe for the PCF SHEET
    database = Constant.PCF_DAT # PATH_FROM + "/" + "pcf.dat"
    p = TM.processing_pcf(database)

    ####################################### preprocessing #######################################
    hk1 = path + "processed1_" + "hk"
    hk2 = path + "processed2_" + "hk"
    TM.pre_processing(hk, hk1, words_to_skip, hk2)
    
    for f, p1, p2 in zip(files, lst_processed1, lst_processed2):
        TM.pre_processing(f, p1, words_to_skip, p2)

    ####################################### postprocessing #######################################
    df_list_preprocessed = []
    for p2 in lst_processed2:
        df = pd.read_csv(p2, skip_blank_lines = True, delim_whitespace = True)
        df_list_preprocessed.append(df)

    # create reference for the housekeeping data to track start of slew
    df_hk = pd.read_csv(hk2, skip_blank_lines = True, delim_whitespace = True)
    df_hk = TM.parse_stream(df_hk)
    df_hk = TM.drop_rows_with_missing_value(df_hk)
    df_hk = TM.drop_column_named(df_hk, 'QUALITY')

    df_list_postprocessed = []
    for df in df_list_preprocessed:
        df = TM.parse_stream(df)
        df = TM.drop_rows_with_missing_value(df)
        df = TM.drop_column_named(df, 'QUALITY')
        # time column addition
        df, end_slew_time, abort_slew_time = TM.create_column_timeSeconds_from_epoch(df, df_hk)
        df_list_postprocessed.append(df)


    #################### call function which analyses the input from the logger file from simulator
    if log_filename != "" :
        log_xls_name = WHERE_TO + "/" + Dir + "/" + Dir + "_SIM_LOGGER.xlsx"
        log_plot     = WHERE_TO + "/" + Dir + "/"
        Sim.create_euler_and_rates_outputs(log_filename, log_xls_name, log_plot, end_slew_time) 
    else :
        Constant.error = 1
        TM.delete_output_folder(path_output_folder, Constant.error)
        raise Exception("No sim logger file present in current slew folder")  

    df_updateHeaders = TM.update_columns_name(df_list_postprocessed, p)
    path_excel = WHERE_TO + "/" + Dir + "/" + Dir + ".xlsx" 
    TM.save_xls(path_excel, df_updateHeaders, sheets_excel, p)

    myDict = {}
    for sheet in sheets_excel:
        df = pd.read_excel(path_excel, sheet_name=sheet)
        start_idx = df.loc[df["TIME (s)"] >= 0, "TIME (s)"].idxmin()
        if start_idx-10 > 0 :
            start_idx = start_idx-10
        else :
            start_idx = 0
        df = df.iloc[start_idx: -1]
        df = df.reset_index(drop=True, inplace=False)
        myDict[sheet] = df

    ####################################### generate plots ######################################
    file_id = ["HK_FSS", 
                "HK_IMUZ", 
                "HK_CTRL", 
                "HK_STR", 
                "ATT_IMU_RW", 
                "RTU2_IMU", 
                "CTL_FSS",
                "CTL_IMUZ", 
                "CTL_CTRL",
                "CTL_STR",
                "CTL_DEBUG_FLOAT",
                "CTL_DEBUG_RAW",
                "CTL_ROLL_XY",
                "CTL_ROLL_ITM",
                "CTL_PITCH_XY",
                "CTL_PITCH_ITM",
                "CTL_YAW_XY", 
                "CTL_YAW_ITM",
                "ATT_TRQ_YPS"] 

    for key, value in myDict.items():
        lst_headers = value.columns.values.tolist()
        indep_var = value["TIME (s)"]

        for f_id in file_id :
            if f_id in key :
                plots_info = file_plots[f_id]

                if end_slew_time == 0:
                    t_list = None
                    t_list_style = None 
                    t_list_label = None

                elif end_slew_time != 0 and abort_slew_time != 0 :
                    t_list = [0, abort_slew_time, end_slew_time]        
                    t_list_style = ["dashdot", "dashed", "dotted"]
                    t_list_label = ['slew start', 'slew abort', 'slew end']
                    
                elif end_slew_time != 0 and abort_slew_time == 0 :
                    t_list = [0, end_slew_time]
                    t_list_style = ["dashdot", "dotted"]
                    t_list_label = ['slew start', 'slew end']
                  
                for plot in plots_info:
                    ys = [value[lst_headers[col_num]] for col_num in plot['ys']]
                    labels = [lst_headers[col_num] for col_num in plot['ys']]

                    if Constant.verbose == 1:
                        print('Generated: ', plot['title'])
                    #else:
                        #pass

                    TM.plot_create(indep_var, 
                                ys, 
                                plot['line_styles'], 
                                plot['line_widths'], 
                                plot['line_colors'], 
                                labels, 
                                plot['style'], 
                                plot['markers'],
                                WHERE_TO + "/" + Dir + "/" + plot['title'] + ".png", 
                                lst_headers[-1], 
                                plot['v_label'],
                                t_list,
                                t_list_style, 
                                t_list_label, 
                                plot['title'])                            
    # END
