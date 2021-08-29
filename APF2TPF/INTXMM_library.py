# created by F Covella - 08 Jan 21
import datetime
import time

# this is a library of general functions
# this can be greately expanded with general functions, well documented 

def check_time_format(string_time):
    """
    Checks that the format of the time string is YYYY-MM-DDThh:mm:ssZ, otherwise it returns an error message
    """
    try:
        datetime.datetime.strptime(string_time, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        raise ValueError("Incorrect time format, should be YYYY-MM-DDThh:mm:ssZ")


def pad_with_spaces_notVoid(string_var, string_tot_length):
    """
    It pads with spaces on the right a string, given its total length
    and checks that the string is not empty and with the right length
    """
    if len(string_var) < string_tot_length:
        string_var = string_var.ljust(string_tot_length, " ")
    if len(string_var) > string_tot_length:
        raise Exception('The length of the input exceed its maximum length. The input was: {}'.format(string_var))
    if string_var == (" " * string_tot_length):
        raise Exception('The input consists of an empty string')
    else:
        pass
    return string_var


def pad_with_spaces(string_var, string_tot_length):
    """
    It pads with spaces on the right a string, given its total length
    """
    if len(string_var) < string_tot_length:
        string_var = string_var.ljust(string_tot_length, " ")
    if len(string_var) > string_tot_length:
        raise Exception('The length of the input exceed its maximum length. The input was: {}'.format(string_var))
    else:
        pass
    return string_var


def pad_with_leading_zero_notVoid_notZero(number_var, number_tot_length):
    """
    It pads with zero(s) on the left a given number, given its total length
    input type: int, double
    output type: string type
    """
    number_var = str(number_var)
    if len(number_var) < number_tot_length:
        number_var = number_var.zfill(number_tot_length)
        print(number_var)
    if len(number_var) > number_tot_length:
        raise Exception('The length of the input exceed its maximum length. The input was: {}'.format(number_var))
    if number_var == (" " * number_tot_length):
        raise Exception('The input consists of an empty string')
    if int(number_var) == 0:
        raise Exception('The input was the number 0 or was left empty')
    else:
        pass
    return number_var


#  created by F Covella - 06 Feb 21
def latest_time_in_rev(epo_file):
    """
    checks if the string PSF_STOP exists in the indicated EPO file and takes the last
    valid time of the revolution.
    """
    flag = False
    with open(epo_file, "r") as e:
        lines = e.readlines()
        for idx, content in enumerate(lines):
            if "PSF_STOP" in content:
                last_valid_time = lines[idx][:20]
                flag = True
        if flag == False:
            raise Exception('Check the .EPO file path: {}, no PST_STOP found'.format(epo_file))
        e.close()
    return last_valid_time


def time_conversion_to_mois(timestamp):
    # change the name of this function (also in th GUI)
    '''
    From %Y-%m-%dT%H:%M:%SZ to '%Y.%j.%H.%M.%S' format
    conversion from ASCII TIME CODE A [YYYY:DD:MMThh:mm:ssZ] 
    to  
    '''
    if timestamp == " ": 
        raise Exception("Please enter a time to be converted")
    else:
        step1 = time.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        step2 = time.strftime('%Y.%j.%H.%M.%S', step1) #"%m/%d/%Y", step1)
    return step2


def create_dictionary_from_apf(apf_file, list_of_s):
    """
    create a dictionary of a certain list of sequences found in a chosen apf file (note that
    you need the path leading to the file) containing for each sequence the uplink time, the
    number of parameters and a list of the parameters of each of its occurrence in the apf.
    """
    sDict = {}
    for elem in list_of_s:
        sDict[elem] = {"uplink_times": [], "#_param": [], "lst_of_param": []}
    with open(apf_file, 'r') as f:
        lines = f.readlines()
        for idx, content in enumerate(lines):
            for elem in list_of_s:
                if elem in content:
                    sDict[elem]["uplink_times"].append( lines[idx+2][:len(lines[idx+2]) -1] )
                    sDict[elem]["#_param"].append( lines[idx+1][ (len(lines[idx+1])-4):len(lines[idx+1])-1] )
                    P = int(sDict.get(elem, {}).get("#_param")[0])
                    sDict[elem]["lst_of_param"].append( lines[idx+5:idx+5+P])
        f.close()
    return sDict
