import os
from pathlib import Path

orgin_path="./data/table.txt"
dest_path="./data/usergroup_temp.txt"

p = Path(orgin_path)

read_origin_file = open(orgin_path, 'r')
convert_to_list = read_origin_file.readlines()

for word in convert_to_list:
    f = open(dest_path,'a')
    f.write(" ".join(word.split()).replace(' ',','))
    f.write('\n')
    f.close()

    
# for i in a:
#     split_by_space = i.split(" ") # split by empty value
#     remove_none_value = list(filter(None,split_by_space)) # create a list with filtering None value
    
#     f = open(dest_path,'a')

#     for word in remove_none_value:        
#         f.write(word)
#         # f.write(",".join(word))      
#     f.write('\n')
#     f.close()