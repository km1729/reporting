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
                    b.insert(0,yy+mm+dd)
                    print(b)
                    # print(type(a))
                    # write
                    f= open(combined_report1_path,'a')
                    for word in b:              
                        f.write(word + ',')                        
                    f.write('\n')
                    f.close()          
