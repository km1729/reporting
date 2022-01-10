# ######################################################################
# Combine dp9 daily reports into one File
# ###################################################################### 

import os
from pathlib import Path
import csv

origin_path = './report/dataset_small/small'
input_dir = Path(origin_path)
dest_path = './report/dataset_output/test3.csv'

def get_date(fname):
    year = fname[-12:-8]
    month = fname[-8:-6]
    date = fname[-6:-4]
    return year, month, date

def read_a_report(report):
    f = open(origin_path+'/'+report.name,'r') 
    a = f.readlines()
    return a

count_dp9 = 0  

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
                    # print("\n")
                    

                    # write to combinded dataset file
                    f= open(dest_path,'a')
                    for word in b:              
                        f.write(word + ',')                        
                    f.write('\n')
                    f.close()
                      

print("# of files: "+ str(number_of_files))
print("dp9 usage data: " + str(count_dp9))
                              
