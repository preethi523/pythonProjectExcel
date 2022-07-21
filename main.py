# This is a sample Python script.
import os

import numpy as np
import pandas as pd
import string
import json
import re

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from pandas import DataFrame


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True


def altering_json(path_json, path_excel):
    # Opening JSON file
    json_input = open(path_json)
    data = json.load(json_input)
    final_cpt_codes = data["cpt"]["surgery"]["codes"]
    list_of_codes = final_cpt_codes.split(",")
    model_probability = data["cpt"]["surgery"]["codeProbabilities"]
    list_of_tuples = []
    for i in range(len(model_probability)):
        if model_probability[i]["code"] in list_of_codes:
            dict_values = tuple(model_probability[i].values())
            list_of_tuples.append(dict_values)
    count = 0
    df = pd.read_excel(path_excel)
    for i in range(len(list_of_tuples)):
        df['cpt_code'] = df['cpt_code'].astype(str)
        df_filtered = df[(df['cpt_code'] == list_of_tuples[i][0])]  # Filtering dataframe
        if not df_filtered.empty:
            matched_threshold = df_filtered[df_filtered["Threshold"] <= list_of_tuples[i][1]]
            if matched_threshold.empty:
                data["cpt"]["surgery"]["codes"] = data["cpt"]["surgery"]["codes"].replace(list_of_tuples[i][0], "")
                data["cpt"]["surgery"]["candidateCodes"]=data["cpt"]["surgery"]["candidateCodes"].replace(list_of_tuples[i][0], "")
                count=count+1
            else:
                data["cpt"]["surgery"]["codes"] = data["cpt"]["surgery"]["codes"].replace(list_of_tuples[i][0],
                                                                                          list_of_tuples[i][0])
                data["cpt"]["surgery"]["candidateCodes"] = data["cpt"]["surgery"]["candidateCodes"].replace(list_of_tuples[i][0],
                                                                                          list_of_tuples[i][0])
        else:
            data["cpt"]["surgery"]["codes"] = data["cpt"]["surgery"]["codes"]
            data["cpt"]["surgery"]["candidateCodes"] = data["cpt"]["surgery"]["candidateCodes"]
    data["cpt"]["surgery"]["codes"] = data["cpt"]["surgery"]["codes"].replace(",,", ",")
    data["cpt"]["surgery"]["codes"] = data["cpt"]["surgery"]["codes"].strip(',')
    data["cpt"]["surgery"]["candidateCodes"] = data["cpt"]["surgery"]["candidateCodes"].strip(',')
    data["cpt"]["surgery"]["candidateCodes"] = data["cpt"]["surgery"]["candidateCodes"].replace(",,", ",")


    print(data)

    #to write in a file
    # path = '/home/preethia/Documents/07202022_Gopi'
    # output_path= f"{path}/{file_name}"
    # output_file = open(output_path, "w")
    # json.dump(data, output_file)
    # print(data)
    # print(output_file)
    #
    # output_file.close()
    json_input.close()
    print(count)
    return count


def read_multiple_files_from_directory():
        path = '/home/preethia/Documents/07182022'
        os.chdir(path)
        count_total = 0
        filect = 0
        for file in os.listdir():
            # Check whether file is in json format or not
            if file.endswith(".json"):
                file_path = f"{path}/{file}"
                count = altering_json(file_path,
                                     '/home/preethia/PycharmProjects/pythonProjectExcel/Threshold_dict-Ephron.xlsx',
                                     file)
                filect = filect + 1
                count_total = count + count_total
        print("final count", count_total)

    # Closing file



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    read_multiple_files_from_directory
    altering_json("data.json",'/home/preethia/PycharmProjects/pythonProjectExcel/Threshold_dict-Ephron.xlsx')








# See PyCharm help at https://www.jetbrains.com/help/pycharm/
