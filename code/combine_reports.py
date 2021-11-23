# ######################################################################
# Combine dp9 records in the existing reports into one File
# ###################################################################### 

import os
from pathlib import Path

report_dir = '/BOM/report/q3'
p = Path(report_dir)
combined_report1_path = '/BOM/report/q3/combined_report.txt'
target_reports = ['dp9_20','dp9_gdata_20','dp9_scratch_20']

project = ['dp9','du7']

def get_fname(report):
    a = report[11:]
    b = a[:-2]
    return b

def get_date(fname):
    year = fname[-12:-8]
    month = fname[-8:-6]
    date = fname[-6:-4]
    return year, month, date

def read_a_report(report):
    f = open(report,'r')
    Lines = f.readlines()
    # Lines.strip()
    return Lines

reports = []
for report in os.scandir(p):

    if report.is_file():

        if target_reports[0] in report.name:
            line = read_a_report(report)            

            if target_reports[0] in line: #'dp' in line
                f= open(combined_report1_path,'w')
                f.writelines(line)
                f.close()

            # reports.append(get_fname(str(report))) 
            
           

# print(reports)
# print(len(reports))
# print(type(reports[0]))

# count = 0
# for fname in reports:
#     if project[0] in fname:
#         count += 1
#         print(fname)
        # file = open(combined_report[0], 'a')
        # file.writelines(line)
        # file.close()

    

