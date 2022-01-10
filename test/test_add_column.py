import pytest
import os
from pathlib import Path
import pandas as pd

data1 = {
    'user' : ['dl9118','km0642','lm4758','bd1225','dl9118','km0642','lm4758','ac1225'],
    'team' :['russia', 'saudiarabia','egypt','uruguay','','','',''],
    'against': ['saudiarabia', 'russia', 'uruguay', 'egypt','','','','',],
    'fifa_rank': [65, 63, 31, 21,0,0,0,0]
    }
columns = ['user','team', 'against', 'fifa_rank']
data2 = {
    'user' :['dl9118','km0642','lm4758'],
    'proj':['577','123','']
}
df1 = pd.DataFrame(data1, columns = columns)
df2 = pd.DataFrame(data2, columns=['user','proj'])
df3 = df1.copy()
print(df1)
print(df2)
print(df3)
print(type(df3))

# df1['proj'] = df1[['user']].merge(df2, how='left').proj
# print(df1)

df3 = pd.DataFrame.merge(df1,df2,left_on='user',right_on='user', how='left')
print(df3)


# df1['sub_prj']= pd.merge(df1, df2, left_on="user", right_on="user",how='left')
# df1

# df1['sub_proj'] = df1[['user']].merge(df2,how='left').sub_proj
# print(df1)

def add_group(user):
    projs = user
    return projs

