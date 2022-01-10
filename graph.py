import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns

# 
file_path='./report/dataset_output/total_dp9_gdata.csv'

colnames = ['date', 'project', 'user', 'GB','TB']
columns_selected = [0,1,2,4,5]

df = pd.read_csv(file_path, names=colnames, usecols=columns_selected)
df.drop_duplicates()

the_last_day = [
                '2020-04-30','2020-05-30', '2020-06-30',
               '2021-01-31', '2021-02-28', '2021-03-31', '2021-04-30', '2021-07-31', '2021-08-31', 
               '2021-09-30','2021-10-31'
               ]

# Project cumulative and actuall usage dataframe
df_prj_mth = df.loc[df['date'].isin(the_last_day),:]
df_prj_mth_s = df_prj_mth.groupby(['date','project']).TB.sum().reset_index()
df_prj_mth_s['diff'] = df_prj_mth_s['TB'].diff().fillna(0)

# individual's cumulative and actuall usage dataframe
df_inv = df_prj_mth.groupby(['date','user']).TB.sum().reset_index()
df_inv['diff'] = df_inv['TB'].diff().fillna(0)
df_inv_p1=df_inv.pivot(index='date',columns='user', values='diff')

fig, axes = plt.subplots(3, 1, figsize=(12, 10))

fig.suptitle('dp9 gdata usage')

sns.lineplot(ax=axes[0], data=df_prj_mth_s, x='date', y='TB')
sns.lineplot(ax=axes[1], data=df_prj_mth_s, x='date', y='diff')
# df_inv_p1.plot(ax=axes[2], kind='bar')

plt.show()
fig.savefig('Subplot_ex3.png')
