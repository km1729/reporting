import os
from pathlib import Path
import pandas as pd

origin_data = "./data/total_dp9_gdata.csv"
group_data = "./data/usergroup_temp.txt"
dest_data = "./data/total_dp9_gdata_group.csv"
user_group="./data/usergroup.txt"

csv_header_dp9 = ["date",'project','user','usage','gb','tb','size','count','d']
csv_header_group = ['user','a','b','c','d','name','sub_proj']
df_origin = pd.read_csv(origin_data, names=csv_header_dp9)
df = pd.read_csv(group_data, names=csv_header_group)

s = df_origin['user'].unique()
df_user=pd.DataFrame(s, columns=['user'])
df_group = df[['user','name','sub_proj']]
# df_group.to_csv(user_group, index=False)

df_origin['proj'] = df_origin[['user']].merge(df_group, how='left').sub_proj
print(df_origin.shape)

df_origin.to_csv(dest_data, index=False, sep=',')