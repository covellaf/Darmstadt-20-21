# =============================================================================
# Created By  : Francesca Covella
# Created Date: March - May 2021
# =============================================================================

import re
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import os
import shutil
from configuration import Constant

###################### creating and delating output folder ######################

def make_output_folder(path_output_folder):
    """
    This method creates an output folder in SLW_PLOTS/ if the folder does not yet exists

    """
    if not os.path.isdir(path_output_folder):
        os.mkdir(path_output_folder)


def delete_output_folder(path_output_folder, flag):
    """
    This method deletes the output folder as it is empty or not complete due to the occurrence of an Exception

    """
    if flag == 0:
        pass
    elif flag == 1 :
        if os.path.isdir(path_output_folder):
            shutil.rmtree(path_output_folder, ignore_errors=True)


###################### data reading from TMPtint and formatting ######################

def processing_pcf(pcf_file):
    """
    it takes as input the pcf file and it processes it to have 
    the correct format for the excel dataframe

    NOTE
    if a "name"(a telemetry value in the pcf) has no unit associated to 
    it, then I convert the NaN value in - so that it is more convenient for 
    plotting the data, as in the litterature for an adimensional number or a number
    with no unit associated to it, [-] is more common than [NaN], [nan], [no unit]. 
    DataFrame.fillna(value=None, method=None, axis=None, inplace=False, limit=None, downcast=None)[source]
    """
    headers = ["NAME", "DESCRIPTION", "info3", "UNIT", 
            "info5", "info6", "info7", 
            "info8", "info9", "info10", 
            "info11", "info12", "info13", 
            "info14", "info15", "info16", 
            "info17", "info18", "info19"]
    pcf_table = pd.read_table(pcf_file, header=None, names=headers, skip_blank_lines=True)
    pcf_sub = pcf_table[["NAME", "DESCRIPTION", "UNIT"]]
    pcf_sub["UNIT"] = pcf_sub["UNIT"].fillna(value ="n/a")
    
    return pcf_sub


def negative_lookahead_assertion(s):
    """
    Matches - if a number doesn’t match next. This is a negative lookahead assertion. 
    For example, - (?!number) will match ' ' only if it’s not followed by a number.
    takes a string as input and substitutes all hypans with spaces unless the
    hypan is followed by a number, in which case the hypan is a minus sign.
    """
    s = re.sub(r'-(?![0-9])', ' ', s)
    return s


def from_original_to_processed1(original_file, new_file, words_to_skip):
    """
    inputs:
    file path of original file from TM print
    path of new file
    list of words to skip
    the function deletes the empty lines, replaces hypan with spaces
    to account for header names and empty values
    replaces e+space by e to avoid probles with elevation to a power
    and lastly eliminates useless strings for the data processing
    """
    with open(original_file) as f, open(new_file, 'w') as n:
        for line in f:
            if line.strip():
                line = negative_lookahead_assertion(line)
                line = line.replace("e ", "e")
                if not any(word in line for word in words_to_skip):
                    n.write(line)


def from_processed1_to_processed2(p1, p2):
    """ 
    writes a new .txt for the later operation with panda dataframe 
    skip the headers after the first line
    """
    with open(p1, 'r') as f, open(p2, 'w') as n:
        first_line = f.readline()
        n.write(first_line)
        second_to_end = f.readlines()[1:]
        for line in second_to_end:
            if line != first_line:
                n.write(line)


def pre_processing(original_file, processed1, words_skipped, processed2):
    """
    function which from the original file produced by TM PRINT
    writes a txt file useful for the post-processing with pandas
    """
    from_original_to_processed1(original_file, processed1, words_skipped)
    from_processed1_to_processed2(processed1, processed2)


def parse_stream(df):
    """
    makes sure that only the rows in which the stream is 65535 is saved
    and then it deletes the column of stram values - for instance **** -
    input: dataframe
    actions: convert the stream values from type numpy.int64 to str
    dump rows which do not have 65535 under STREAM, delete stream column
    output: new dataframe
    NOTE
    reset_index()
    drop bool, default False
    Do not try to insert index into dataframe columns. This resets the index to the default integer index.
    inplace bool, default False
    Modify the DataFrame in place (do not create a new object).
    """
    df["STREAM"] = df["STREAM"].map(str)
    df = df[df.STREAM.str.contains('65535')]
    df = drop_column_named(df, 'STREAM')
    df = df.reset_index(drop=True, inplace=False)
    return df


def drop_column_named(df, column_regex):
    """
    This method eliminates certain columns of the dataframe based on the regex inserted 

    """
    df = df[df.columns.drop(list(df.filter(regex=column_regex)))]
    return df


def drop_rows_with_missing_value(df):
    """
    input: dataframe
    actions: makes sure that only the rows in which the number of headers matches the number
    of entries is saved, avoiding that if one missing value is present the whole row
    is not saved, as the data is considered incomplete
    output: new dataframe
    NOTE
    dropna()
    DataFrame.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
    axis{0 or ‘index’, 1 or ‘columns’}, default 0
    Determine if rows or columns which contain missing values are removed.
    0, or ‘index’ : Drop rows which contain missing values.
    1, or ‘columns’ : Drop columns which contain missing value.
    """
    df = df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
    df = df.reset_index(drop=True, inplace=False)
    return df


def get_start_and_end_of_slew(df_HK):
    """
    input: hausekeeping dataframe
    epoch is defined as the beginning of slew manoeuvre
    corresponding to the value of RGA that turns from 5 (stable pointing)
    to 15 (slew configuration)
    NOTE
    if slew array is void at this point it means that there is no
    slew in the chosen timeframe, hence the epoch is defined as the
    start of TM collection and the end of the data of interest is defined
    as the end of the TM collection timeframe.
    """
    slew = []
    abort = []
    for index in range(len(df_HK['A5243'])):
        if df_HK['A5243'][index] == 15:
            slew.append(index)
        if df_HK['A5242'][index] == 6:
            abort.append(index)

    if len(slew) == 0:
        time_epoch = to_seconds(df_HK["TIME"][0])
        if Constant.verbose == 1:
            print('WARNING: there is no slew occurring in the selected time range ')
        abort_slew = 0
        delta_slew = 0 
    elif len(slew) != 0 :
        start_slew_idx = slew[0]
        end_slew_idx = slew[-1]        
        start_slew_time = df_HK['TIME'][start_slew_idx]
        end_slew_time = df_HK['TIME'][end_slew_idx]              
        time_epoch = to_seconds(start_slew_time)
        end_slew_0margin = to_seconds(end_slew_time)
        delta_slew = end_slew_0margin - time_epoch      
        if len(abort) == 0:
            abort_slew = 0           
        elif len(abort) != 0 :
            abort_idx = abort[0]
            abort_slew_time = df_HK['TIME'][abort_idx]
            abort_slew = to_seconds(abort_slew_time) - time_epoch       
    return time_epoch, delta_slew, abort_slew


def create_column_timeSeconds_from_epoch(df, df_HK):
    """
    function that outputs an updated dataframe with a new column containing
    the time in seconds starting from an epoch corresponsing with the beginning
    of the slew, that is second 0.
    NOTE
    A5243 == RGA, find all indeces when A5243 is equal to 15
    """
    epoch, end_slew, abort = get_start_and_end_of_slew(df_HK)
    time_in_sec = []
    for count in range(len(df["TIME"])):
        result = to_seconds(df["TIME"][count])
        time_in_sec.append(result - epoch)
    df["TIME (s)"] = time_in_sec
    return df, end_slew, abort



def mid(text, start_char, num_chars):
    """ 
    MID returns a specific number of characters 
    from a text string, starting at the position you specify, 
    based on the number of characters you specify.
    """
    string = text[start_char : start_char+num_chars]
    return int(string)


def to_seconds(time):
    """ 
    returns the number of seconds from a text string of time
    specified in the format YYYY.JJJ.hh.mm.ss.ffff
    """
    seconds = mid(time, 9, 2) * 3600 + mid(time, 12, 2) * 60 + mid(time, 15, 2) 
    #+ mid(time, 18, 3) * 0.001
    return seconds


def save_xls(xls_path, list_dfs, list_sheets_name, pcf_df):
    """
    output: excel file with visualisation of each panda dataframe in each of the sheet
    it writes the dataframes into an excel file and it adds a sheet
    with the PCF parameters descriptions and unit
    NOTE
    engine: Write engine to use, ‘openpyxl’ or ‘xlsxwriter’. 
    """
    from pandas import ExcelWriter
    writer = pd.ExcelWriter(xls_path, engine = 'xlsxwriter')
    for df, name in zip(list_dfs, list_sheets_name):
        df.to_excel(writer, sheet_name = name, header=True, index=False) 
        if Constant.verbose == 1 :
            print('excel file written: ', name)
    writer.save()
    # writer.close()
    from openpyxl import load_workbook
    book = load_workbook(xls_path)
    writer = pd.ExcelWriter(xls_path, engine = 'openpyxl')
    writer.book = book
    pcf_df.to_excel(writer, sheet_name="PCF", header=True, index=False)
    if Constant.verbose == 1 :
        print("PCF", "written")
    writer.save()
    
    # ALT+H then O then I :to expand the excel spreadsheet

####################################### generate plots from TMPrint #######################################
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import pylab


def update_columns_name(lst_of_dfPostprocessed, dfPCF):
    """
    actions: to read the description and unit of each header parameters and update the dataframes
    output: a list of updated dataframes for plotting purposes with an updated header
    NOTE
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    df.rename(columns={"A": "a", "B": "c"})
    """
    lst_of_dfForPlotting = []
    for df in lst_of_dfPostprocessed: 
        for header in df.columns.tolist()[1:-1]:
            header_idx = dfPCF.index[dfPCF["NAME"] == header].tolist()[0]
            new_header = header + ": " + str(dfPCF.loc[header_idx]["DESCRIPTION"]) + " " + "[" + str(dfPCF.loc[header_idx]["UNIT"]) + "]"
            # new_header = header + ": " + str(dfPCF.iloc[header_idx]["DESCRIPTION"]) + " " + "[" + str(dfPCF.iloc[header_idx]["UNIT"]) + "]"
            df = df.rename(columns={header: new_header})
        lst_of_dfForPlotting.append(df)
    return lst_of_dfForPlotting


def plot_create(x, ys, line_styles, line_widths, line_colors, labels, style, markers, name_fig, h_label, v_label, t_list, t_list_style, t_list_label, title=''):
    """
    NOTE: the available plotting styles are
    'Solarize_Light2', '_classic_test_patch', 'bmh', 'classic', 'dark_background', 
    'fast', 'fivethirtyeight', 'ggplot' (has a gray background), 'grayscale', 'seaborn', 'seaborn-bright', 
    'seaborn-colorblind', 'seaborn-dark', 'seaborn-dark-palette', 'seaborn-darkgrid', 
    'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel', 
    'seaborn-poster','seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'tableau-colorblind10'
    """
    plt.figure()
    plt.style.use(style)

    for idx in range(len(ys)):
        plt.plot(x, 
                ys[idx], 
                linestyle = line_styles[idx], 
                linewidth = line_widths[idx], 
                marker = markers[idx],
                color = line_colors[idx], 
                label = labels[idx])
    if t_list:
        v_lines(t_list, t_list_style, t_list_label) 
    plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
                                    mode="expand", fancybox=True)
    plt.grid(True)
    plt.xlabel(h_label)
    plt.ylabel(v_label)
    plt.savefig(name_fig, bbox_inches="tight")


def v_lines(xposition, xstyle, xlabels):
    """
    This method creates vertical lines at some remarkable position, specifying a style and a legend

    """
    [plt.axvline(xp, linewidth=1, linestyle=xs, color='purple', label=xl) for xp, xs, xl in zip(xposition, xstyle, xlabels)]


def v_spans(xmin, xmax, xstyle, xlabels, xcolor):
    """
    This method divides the plot in regions delimited by vertical lines (each region can be highlighted of a different color)
    it is not used but it could be used, the vertical lines were considered a cleaner option --> see v_lines method

    """
    [plt.axvspan(xmi, xma, linewidth=1, linestyle=xs, color=xc, alpha=0.5, label=xl) for xmi, xma, xs, xl, xc in zip(xmin, xmax, xstyle, xlabels, xcolor)]

