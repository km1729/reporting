# ######################################################################
# Combine dp9 daily reports into one File
# ###################################################################### 

import os
from pathlib import Path
import csv

origin_path = './report/dataset_small/small'
input_dir = Path(origin_path)
dest_path = './report/dataset_output/test2_format.csv'

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
copied_record = 0  

for report in os.scandir(input_dir):
   
    number_of_files = len(os.listdir(input_dir))

    if report.is_file():                
       
        if 'dp9_gdata_20' in report.name: 
            proj_data = read_a_report(report)

            
            for proj in proj_data:
                yy, mm, dd = get_date(report.name) 

                            
                if 'dp' in proj:         
                    count_dp9 +=1    

                    a = proj.split(' ')                    
                    b = [elem.strip() for elem in a]
                    b = list(filter(None,b))         
                    
                    # add date
                    b.insert(0,str(yy+'-'+mm+'-'+dd))
                                  
                    print(b)
                    print("length of list is: "+ str(len(b)))
                    # print("\n")
                    
                    if len(b) == 6:
                        copied_record +=1
                        b.insert(4,convert_data_value_GB(b[3]))                    
                        b.insert(5,convert_data_value_TB(b[3]))  
                        # write to combinded dataset file
                        f= open(dest_path,'a')
                        for word in b:              
                            f.write(word + ',')                        
                        f.write('\n')
                        f.close()
                      

print("# of files in dir: "+ str(number_of_files))
print("# of dp9 usage data in files: " + str(count_dp9))
print("# of record copied to output: " + str(copied_record))
                              