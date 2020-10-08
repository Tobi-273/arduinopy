"""Functions for saving arduino data by using the serial bus"""

import serial
import pandas as pd
from datetime import datetime


def save_current_timestamp(function_list):
    """Appends current time to given list and returns it"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    function_list.append(current_time)
    return function_list


def save_value(data, function_list):
    """Appends given value to given list and returns it"""
    data = data.replace("\r\n", "")
    function_list.append(data)
    return function_list


def create_dataframe(list_1, list_2, name_1='Column_1', name_2='Column_2'):
    """Creates a pandas dataframe from two given lists and returns it.
    Expects two lists (and according names as kwargs)"""
    df = pd.DataFrame(list(zip(list_1, list_2)), columns=[name_1, name_2])
    return df


def csvname_creator(basename, name_addition):
    """Creates a name for the output file and returns it.
    Expects two strings; a basename that does not (have to) change and a name_addition that changes (e.g. timestamp),
    in order to prevent overwriting files that have been created by previous function calls and/or program runs"""
    csvname = basename + name_addition
    csvname = csvname.replace(':', '-')
    csvname = csvname.replace('.', '--')
    csvname = csvname + '.csv'
    return csvname


def time_and_datalog(file_basename='DataLog', com='COM3', encoding='ascii', baudrate=9600, timeout=1,
                     x_name='Timestamp', y_name='Value'):
    """Creates a .csv file with timestamps and arduino values until interrupted"""
    start_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-7])
    filename = csvname_creator(file_basename, start_time)

    try:
        current_connection = serial.Serial(com, baudrate=baudrate, timeout=timeout)
    except serial.serialutil.SerialException:
        print("Arduino is not connected")
        exit()
    arduino_data = current_connection.readline().decode(encoding) # This first value is garbage, assignment IS needed

    time_list = ['start']
    values_list = ['start']

    while True:
        if time_list[-1] != datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]:
            arduino_data = current_connection.readline().decode(encoding)
            time_list = save_current_timestamp(time_list)
            values_list = save_value(arduino_data, values_list)
            print(arduino_data)

            arduino_frame = create_dataframe(time_list, values_list, name_1=x_name, name_2=y_name)
            arduino_frame.to_csv(filename)
