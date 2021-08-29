# created by F Covella 08 Feb 21
import INTXMM_library
from TPF_library import TPF


def name_file(location, rev_v, seq, time):
    # convert the time string into a format which the function "open" accepts, i.e. without column
    time = INTXMM_library.time_conversion_to_mois(time)
    name = location + rev_v + "_" + seq + "_" + time + ".TPF"
    return name


def all_seq_all_time(epo_file, outputs, rev_v, dictionary):   
    last_valid_time = INTXMM_library.latest_time_in_rev(epo_file)

    for k in list(dictionary.keys()) :
        utimes = dictionary[k]["uplink_times"]
        for t in utimes:
            idx = dictionary[k]["uplink_times"].index(t)
            num_param = dictionary[k]["#_param"][idx]
            TPF_obj = TPF()
            TPF_obj.set_header1(k, "S")
            TPF_obj.set_header2("M", "S", num_param)
            if t != utimes[-1]:
                TPF_obj.set_header3("{0:20}".format(" "), t, dictionary[k]["uplink_times"][idx+1])
            elif t == utimes[-1]:
                TPF_obj.set_header3("{0:20}".format(" "), t, last_valid_time)
            TPF_obj.set_header4()
            TPF_obj.set_header5()
            file = name_file(outputs, rev_v, k, t)
            TPF_obj.create_headers_sublist()
            lst_param = dictionary[k]["lst_of_param"][idx]
            TPF_obj.assign_param(lst_param)
            TPF_obj.write_tpf(file)


def one_seq_all_time(epo_file, outputs, rev_v, input_key, dictionary):
    last_valid_time = INTXMM_library.latest_time_in_rev(epo_file)
    utimes = dictionary[input_key]["uplink_times"]
    for t in utimes:
        idx = dictionary[input_key]["uplink_times"].index(t)
        num_param =dictionary[input_key]["#_param"][idx]
        TPF_obj = TPF()
        TPF_obj.set_header1(input_key, "S")
        TPF_obj.set_header2("M", "S", num_param)
        if t != utimes[-1]:
            TPF_obj.set_header3("{0:20}".format(" "), t, dictionary[input_key]["uplink_times"][idx+1])
        elif t == utimes[-1]:
            TPF_obj.set_header3("{0:20}".format(" "), t, last_valid_time)
        TPF_obj.set_header4()
        TPF_obj.set_header5()
        file = name_file(outputs, rev_v, input_key, t)
        TPF_obj.create_headers_sublist()
        lst_param = dictionary[input_key]["lst_of_param"][idx]
        TPF_obj.assign_param(lst_param)
        TPF_obj.write_tpf(file)


def one_seq_one_time(epo_file, outputs, rev_v, input_key, utimes, dictionary):
    last_valid_time = INTXMM_library.latest_time_in_rev(epo_file)
    idx = dictionary[input_key]["uplink_times"].index(utimes)
    num_param = dictionary[input_key]["#_param"][idx]
    
    TPF_obj = TPF()
    TPF_obj.set_header1(input_key, "S")
    TPF_obj.set_header2("M", "S", num_param)
    if utimes != dictionary[input_key]["uplink_times"][-1]:
        TPF_obj.set_header3("{0:20}".format(" "), utimes, dictionary[input_key]["uplink_times"][idx+1])
    elif utimes == dictionary[input_key]["uplink_times"][-1]:
        TPF_obj.set_header3("{0:20}".format(" "), utimes, last_valid_time)
    TPF_obj.set_header4()
    TPF_obj.set_header5()
    file = name_file(outputs, rev_v, input_key, utimes)
    TPF_obj.create_headers_sublist()
    lst_param = dictionary[input_key]["lst_of_param"][idx]
    TPF_obj.assign_param(lst_param)
    TPF_obj.write_tpf(file)