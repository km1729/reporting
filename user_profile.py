import os
from pathlib import Path
import pandas as pd

origin_data = "./data/total_dp9_gdata.csv"
user_group="./data/usergroup.txt"

# users in reports
csv_header_dp9 = ["date",'project','user','usage','gb','tb','size','count','d']
df_origin = pd.read_csv(origin_data, names=csv_header_dp9)
s = df_origin['user'].unique()
df_users_in_record=pd.DataFrame(s, columns=['user'])
# print('--- df_users_in_record ---')
# print(df_users_in_record)

'''
    df_users_in_record.columns
    ['user', 'name', 'sub_proj']
'''

# some users profile
user_df = pd.read_csv(user_group)
# print('--- user_group ---')
# print(user_df)
'''
    user_df.columns
    ['user']
'''
combine_user_df=pd.merge(df_users_in_record, user_df, left_on='user', right_on='user', how='left')
print(combine_user_df)
combine_user_df.to_csv(user_group)
# print(df_user)
# print(type(df_user))
# df_group = df[['user','name','sub_proj']]
# df_group.to_csv(user_group, index=False)
