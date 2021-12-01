# ######################################################################
# Combine dp9 daily reports into one File
# ###################################################################### 

import os
from pathlib import Path
import csv

report_dir = './report/temp'
p = Path(report_dir)
combined_report1_path = './report/total_dp9_gdata.csv'

# target_reports = ['dp9_20','dp9_gdata_20','dp9_scratch_20']
# project = ['dp9','dx2']

def get_date(fname):
    year = fname[-12:-8]
    month = fname[-8:-6]
    date = fname[-6:-4]
    return year, month, date

def read_a_report(report):
    
    f = open(report_dir+'/'+report.name,'r') 
    a = f.readlines()
    return a

def convert_data_value_TB(usage):
    value = float(usage [:-2])
    unit = usage[-2:]

    # Convert units to TB
    if unit == "GB":
        value /= 1000.0
    if unit == "MB":
        value /= 1000000.0
    if unit == "KB":
        value /= 1000000000.0
    return str(value)

def convert_data_value_GB(usage):
    value = float(usage [:-2])
    unit = usage[-2:]

    # Convert units to GB
    if unit == "TB":
        value *= 0.001
    if unit == "MB":
        value /= 1000.0
    if unit == "KB":
        value /= 1000000.0
    return str(value)

for report in os.scandir(p):

    if report.is_file():

        # determine a report name has a target report name
        # get the date of the report
        if 'dp9_gdata_20' in report.name: 
            data_in_report = read_a_report(report)

            # read the project name and determine if there is a project name is 'dp9' in a line of the report
            # dp_2021xxxx.rpt file doesn't have a project name in a daily report - different format
            for proj_usage in data_in_report:
                yy, mm, dd = get_date(report.name) 
                              
                if 'dp' in proj_usage:                    
                    a = proj_usage.split(' ')
                    b = [elem.strip() for elem in a]
                    b = list(filter(None,b))                    
                    
                    # add date
                    b.insert(0,str(yy+'-'+mm+'-'+dd))
                    print(b[3])
                    b.insert(4,convert_data_value_GB(b[3]))
                    b.insert(5,convert_data_value_TB(b[3]))
                    print(b)
                    

                    # write to combinded dataset file
                    f= open(combined_report1_path,'a')
                    for word in b:              
                        f.write(word + ',')                        
                    f.write('\n')
                    f.close()          
