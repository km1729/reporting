import os
from pathlib import Path
import shutil


origin_path = './report/dataset_small'
dest_path=''

p = Path(origin_path)
shutil.copytree(origin_path, dest_path)

num_of_files = len(os.listdir(origin_path))

# print(os.curdir)
print(num_of_files)

the_last_day = [
               '2021-01-31', '2021-02-28', '2021-03-31', '2021-04-30', '2021-07-31', '2021-08-31',
               '2021-09-30', '2021-10-31'
               ]

# for file in os.scandir(p) :
#     print(file)