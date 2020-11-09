import numpy as np
import matplotlib.pyplot as plt
# from ufc_functions import *
import matplotlib

# change display settings
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 4000)
pd.set_option('display.max_columns', None)
head_ = 12

def pretty_print(str="I'm too lazy to add comment", max=206):
    ''' Just a function to make the printed output stand out'''
    str_l = len(str)
    print('*' * (max + 1))
    l = int((max - str_l) / 2)
    print('*' * l, str, '*' * l)
    print('*' * (max + 1))
    return

def meth_split(meth_):
    ''' Aggregate the methods of fight finishing'''
    if meth_ in ['Decision - Majority', 'Decision - Split', "Decision - Unanimous" ]:
        return('Decision')
    elif meth_ in ["TKO - Doctor's Stoppage", 'KO/TKO']:
        return('TKO')
    elif meth_ == 'Submission':
        return ('Submission')
    else:
        return ('Other')


#read data
df = pd.read_csv(r"data/ufc_data.csv")
df_group_count = pd.read_csv(r'data/ufc_group_count.csv')
df_fighter = pd.read_csv(r'data/ufc_fighter.csv')


pretty_print('Basic Stats on the Data')
print('Sum: ', df_group_count.sum(numeric_only=True))
print('Mean Per Year: ', df_group_count.mean(numeric_only=True))
print('Median Per Year: ', df_group_count.median(numeric_only=True))
print('SD Per Year: ', df_group_count.std())
pretty_print('Number of Fights Per Year')
print(df_group_count)

# count by year and fight end type
df_yr_method = df.groupby(['year', 'method']).agg(np.count_nonzero).sort_values('year', ascending=False).reset_index(drop=False)
df_yr_method['method_agg'] = [meth_split(val) for val in df_yr_method['method']]
df_yr_method = df_yr_method.groupby(['year', 'method_agg']).agg(sum).sort_values(['year', 'event_name'], ascending=False).reset_index(drop=False)
df_yr_method.drop(df_yr_method.columns.difference(['year', 'method_agg', 'event_name']), 1, inplace=True)
# plot by year and type of finish
fig = plt.figure(figsize=(16,8) )
ax = plt.axes()

for i, type_dec in enumerate(pd.unique(df_yr_method.method_agg)):
    type_dec_ = df_yr_method[df_yr_method.method_agg.isin([type_dec])]
    plt.plot(type_dec_['year'], type_dec_['event_name'], label = type_dec)
plt.legend()
ax.set_title('UFC Method of Fight Completion by Year', fontsize=20)
plt.show()

print(df_yr_method)
pretty_print('Method of Fight Ending')
# count how fights are finished
df_method = df.groupby('method').agg(np.count_nonzero).sort_values('event_name', ascending=False).reset_index(drop=False)
df_method.drop(df_method.columns.difference(['method', 'event_name']), 1, inplace=True)
print(df_method)

# condense the way a fight is stopped and group
df_method['method_agg'] = [meth_split(val) for val in df_method['method']]
df_method = df_method.groupby('method_agg').agg(sum).sort_values('event_name', ascending=False).reset_index(drop=False)

pretty_print('by Method')
#df_method.drop(df_method.columns.difference(['method_agg', 'event_name']), 1, inplace=True)
print(df_method)
# pie chart of how fights finish
fig1, ax1 = plt.subplots(figsize=(16, 8), subplot_kw=dict(aspect="equal"))
cmap = plt.get_cmap('twilight')
colors = [cmap(i) for i in np.linspace(0,1,5)]
font = {'family' : 'sans-serif',
        'sans-serif' : "Comic Sans MS",
        'weight' : 'bold',
        'size'   : 18}
matplotlib.rc('font', **font)

#df_sel_method = df_method
sizes = df_method['event_name']
percent_ = 100 * df_method['event_name']/sum(df_method['event_name'])

labels = ['{0} - {1} - {2:1.2f} %'.format(i, j, k) for i, j, k in zip (df_method['method_agg'], df_method['event_name'], percent_)]
ax1.pie(sizes,
        colors = colors,
        labels=df_method['method_agg'],
        rotatelabels=True,
        #autopct = '% 1.1f %%',
        shadow=True, startangle =55)

ax1.legend(labels, loc='lower left', bbox_to_anchor=(1, 0, 0.5, 1)) #, fontsize=12)
ax1.set_title('UFC Method of Fight Completion', fontsize=30)
plt.show()

pretty_print('Ref count of fights')
print(df.groupby(['referee'])['event_name'].count()
      .reset_index(name='count')
      .sort_values(['count'], ascending=False)
      .head(head_))
pretty_print('Describe Data')
print(df.describe())

pretty_print('Describe df_fighter')
print(df_fighter.describe())
pretty_print('Total Fights')
print(df_fighter.sort_values(by=['total'], ascending=False).head(head_))
pretty_print('Total Wins')
print(df_fighter.sort_values(by=['t_wins'], ascending=False).head(head_))
pretty_print('Rounds')
print(df_fighter.sort_values(by=['rounds'], ascending=False).head(head_))
pretty_print('Knock Downs')
print(df_fighter.sort_values(by=['kd'], ascending=False).head(head_))
pretty_print('Knock Down percent per round')
print(df_fighter.loc[df_fighter['total'] > 5].sort_values(by=['kd_round'], ascending=False).head(head_))
pretty_print('Win Percent')
print(df_fighter.loc[df_fighter['total'] > 8].sort_values(by=['win_p'], ascending=False).head(head_))
pretty_print('Total Significant Strikes')
print(df_fighter.loc[df_fighter['sig_strikes'] > 8].sort_values(by=['sig_strikes'], ascending=False).head(head_))
pretty_print('Total Significant Strikes Attempted')
print(df_fighter.loc[df_fighter['sig_strikes_att'] > 8].sort_values(by=['sig_strikes_att'],
                                                                              ascending=False).head(head_))
pretty_print('Total Rounds per Fight')
print(df_fighter.loc[df_fighter['total'] > 5].sort_values(by=['rounds_per_fight'], ascending=False).head(head_))
pretty_print('Total Time per Fight')
print(df_fighter.loc[df_fighter['total'] > 5].sort_values(by=['time_per_fight'], ascending=False).head(head_))
pretty_print('Total Sig Strikes per Min')
print(df_fighter.loc[df_fighter['total'] > 5].sort_values(by=['sig_str_per_min'], ascending=False).head(head_))
pretty_print('Ground Control Time')
print(df_fighter.loc[df_fighter['total'] > 5].sort_values(by=['ground_control'], ascending=False).head(head_))
pretty_print('Dataframe df')
print(df.head(head_))
pretty_print('Dataframe Fighter')
print(df_fighter.head(head_))


