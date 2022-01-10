# ######################################################################
# Combine dp9 daily reports into one File
# ###################################################################### 

import os
from pathlib import Path
import csv

origin_path = './report'
input_dir = Path(origin_path)
dest_path = './report/dataset_output/total_dp9_gdata.csv'

# target_reports = ['dp9_20','dp9_gdata_20','dp9_scratch_20']
# project = ['dp9','dx2']

def get_date(fname):
    year = fname[-12:-8]
    month = fname[-8:-6]
    date = fname[-6:-4]
    return year, month, date

def read_a_report(report):
    
    f = open(origin_path+'/'+report.name,'r') 
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
    if unit == "kB":  
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
    if unit == "kB":
        value /= 1000000.0
    return str(value)

count_dp9 = 0
number_of_gdata = 0  

for report in os.scandir(input_dir):
   
    number_of_files = len(os.listdir(input_dir))

    if report.is_file():                
        
        # determine a report name has a target report name
        if 'dp9_gdata_20' in report.name:
            number_of_gdata +=1 
            proj_data = read_a_report(report)

            # read the daily report and determine if there is a project name  'dp9' in a line of the report
            for proj in proj_data:
                yy, mm, dd = get_date(report.name) 

                if 'dp' in proj:   
                    a = proj.split(' ')                    
                    b = [elem.strip() for elem in a]
                    b = list(filter(None,b))                    
                                        
                    b.insert(0,str(yy+'-'+mm+'-'+dd))              
                    
                    if len(b) == 6:
                        count_dp9 +=1 
                        b.insert(4,convert_data_value_GB(b[3]))                    
                        b.insert(5,convert_data_value_TB(b[3]))    
                        
                        f= open(dest_path,'a')
                        for word in b:              
                            f.write(word + ',')                        
                        f.write('\n')
                        f.close()                    
                              

print(str(number_of_files)+" of files found in this directory")
print(str(number_of_gdata) + " of dp9_gdata file found")
print(str(count_dp9) + " of records copied ")
