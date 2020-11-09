import pandas as pd
from datetime import date


field_dict_f1 = {'event_name': 'count', 'kd_1': 'sum',
                 'round': 'sum', 'Wins_f1': 'sum',
                 'Losses_f1': 'sum', 'NC_f1': 'sum',
                 'Draw_f1': 'sum',
                 'sig_str_f1': 'sum',
                 'sig_str_att_f1': 'sum',
                 'time_min': 'sum'
                 }
# dict for fighter 2
field_dict_f2 = {'method': 'count', 'kd_2': 'sum',
                 'round': 'sum', 'Wins_f2': 'sum',
                 'Losses_f2': 'sum',
                 'NC_f2': 'sum',
                 'Draw_f2': 'sum',
                 'sig_str_f2': 'sum',
                 'sig_str_att_f2': 'sum',
                 'time_min': 'sum'
                 }
# fighter 1 field list which will be appended to
f1_list = ['fighter_name_1', 'Wins_f1',
           'Losses_f1', 'NC_f1', 'Draw_f1',
           'event_name', 'kd_1', 'round',
           'time_min']
# fighter 2 field list which will be appended to
f2_list = ['fighter_name_2', 'Wins_f2', 'Losses_f2', 'NC_f2',
           'Draw_f2', 'method', 'kd_2', 'round',
           'time_min']

# the fields to be added ####
the_fields_to_add = [
    'sig_str_1',
    'sig_str_2',
    'tot_str_1',
    'tot_str_2',
    'TD_1',
    'TD_2',
    'r1_sig_str_1',
    'r1_sig_str_2',
    'r1_tot_str_1',
    'r1_tot_str_2',
    'r1_TD_1',
    'r1_TD_2',
    'tot_head_1',
    'tot_head_2',
    'tot_body_1',
    'tot_body_2',
    'tot_leg_1',
    'tot_leg_2',
    'tot_dist_1',
    'tot_dist_2',
    'tot_clinch_1',
    'tot_clinch_2',
    'tot_ground_1',
    'tot_ground_2']
#
other_fields_no_att = [
    'sub_att_1',
    'sub_att_2',
    'rev_1',
    'rev_2',
    'r1_sub_att_1',
    'r1_sub_att_2',
    'r1_rev_1',
    'r1_rev_2',
    'r1_ctrl_1',
    'r1_ctrl_2',
    'ctrl_1',
    'ctrl_2']
# functions
def split_it(lst):
    ''' split_it takes in string and splits to a list and returns first and last item'''
    ret = lst.split(' ')
    return [ret[0], ret[-1]]


def new_fields(df_, field_lst, yes_att=True, f1=field_dict_f1, f2=field_dict_f2):
    ''' splits field names based on fighter 1 or two
     sets up the dict for field names based on fighter one or two - adds _f1 or _f2
     if field has attempts it adds att_f to it
     appends to dictionary with 'sum' so that they can be aggregated also adds field to field list to
     be included in different tables.  '''
    for field_ in field_lst:
        field_use = (field_[:-1] + 'f' + field_[-1])
        if yes_att:
            df_[field_use] = [int(val.split(",")[0]) for val in df_[field_]]
        else:
            if field_[-6:-2]=='ctrl':
                # control field meaning time in control time sep by : ex = 3:22
                df_[field_use] = [0 if val == '--' else ((int(val.split(":")[0])*60) + (int(val.split(":")[1])))/60
                                  for val in df_[field_]]
            else:
                # not a control field
                df_[field_use] = [int(val) for val in df_[field_]]
        if field_use[-1] == '1':
            f1[field_use] = 'sum'
            f1_list.append(field_use)
        else:
            f2[field_use] = 'sum'
            f2_list.append(field_use)
        if yes_att:
            field_use = (field_[:-1] + 'att_f' + field_[-1])
            df_[field_use] = [int(val.split(",")[1]) for val in df_[field_]]
            if field_use[-1] == '1':
                f1[field_use] = 'sum'
                f1_list.append(field_use)
            else:
                f2[field_use] = 'sum'
                f2_list.append(field_use)
    return df_, f1, f2

def judge_break_out(df_):
    for judge_ in ['judge_1', 'judge_2', 'judge_3']:
        name_ = []
        scr1_ = []
        scr2_ = []
        for item in df_[judge_]:
            if pd.isna(item):
                name_.append('NA')
                scr1_.append('NA')
                scr2_.append('NA')
            else:
                item = item.split('-')
                if len(item[0]) < 3:
                    item[0] = 'Missing Data'
                if len(item) > 3:
                    item[0] = item[0] + "-" + item[1]
                    item[1] = item[2]
                    item[2] = item[3]
                name_.append(item[0])
                scr1_.append(item[1])
                scr2_.append(item[2])
        df_[judge_ + '_name'] = [x for x in name_]
        df_[judge_ + '_scr_1'] = [x for x in scr1_]
        df_[judge_ + '_scr_2'] = [x for x in scr2_]
    return (df_)



# end functions
# load data from spider download
df = pd.read_csv(r"data/ufc.csv")
# make event_date a date field and create a year fiels
df['event_date'] = pd.to_datetime(df['event_date'])
df['year'] = df['event_date'].dt.strftime('%Y')
# create a grouped dataframe to be used for agg and for fighter info
grouped_df = df.sort_values('event_date').groupby(['year'])
df_group_count = grouped_df['fighter_name_1'].count().reset_index(name='fights').sort_values(['year'], ascending=False)

# time ####
df['time_sec'] = [int(val.split(":")[0]) * 60 + (int(val.split(':')[1])) for val in df['time']]
df['time_min'] = [((val - 1)) * 5 + (df.iloc[i]['time_sec'] / 60) for i, val in enumerate(df['round'])]


# creating fields for fighter info Win Loss NC Draw ####
df['Wins_f1'] = df.apply(lambda x: True if x['f1_res'] == 'W' else False, axis=1)
df['Wins_f2'] = df.apply(lambda x: True if x['f2_res'] == 'W' else False, axis=1)
df['Losses_f1'] = df.apply(lambda x: True if x['f1_res'] == 'L' else False, axis=1)
df['Losses_f2'] = df.apply(lambda x: True if x['f2_res'] == 'L' else False, axis=1)
df['NC_f1'] = df.apply(lambda x: True if x['f1_res'] == 'N' else False, axis=1)
df['NC_f2'] = df.apply(lambda x: True if x['f2_res'] == 'N' else False, axis=1)
df['Draw_f1'] = df.apply(lambda x: True if x['f1_res'] == 'D' else False, axis=1)
df['Draw_f2'] = df.apply(lambda x: True if x['f2_res'] == 'D' else False, axis=1)

# the new improved automated way of adding fields! Calls new_field function and feeds in list of fields
# adds the field names to dictionary for and to field list for later adding different views
df, field_dict_f1, field_dict_f2 = new_fields(df, the_fields_to_add)
df, field_dict_f1, field_dict_f2 = new_fields(df, other_fields_no_att, yes_att=False)

# break out judge info here
df = judge_break_out(df)
# finished judge info

# end of splitsville ####
# using the dict to agg the fields
df_fighter_1 = df.groupby(['fighter_name_1']).agg(field_dict_f1).reset_index(drop=False)
df_fighter_2 = df.groupby(['fighter_name_2']).agg(field_dict_f2).reset_index(drop=False)
# using the list to select the fields to include
df_fighter_1 = df_fighter_1.loc[:, f1_list]
df_fighter_2 = df_fighter_2.loc[:, f2_list]
# merging fighter 1 and 2 to aid the viewing pleasure of the report writer
df_fighter = pd.merge(df_fighter_1, df_fighter_2, left_on='fighter_name_1', right_on='fighter_name_2', how='outer')
df_fighter.fighter_name_1.fillna(df_fighter.fighter_name_2, inplace=True)
# this is the next area to automate
df_fighter = df_fighter.loc[:,
                  ['fighter_name_1', 'event_name', 'method', 'kd_1', 'round_x', 'kd_2', 'round_y',
                   'Wins_f1', 'Wins_f2', 'Losses_f1', 'Losses_f2', 'NC_f1', 'NC_f2',
                   'Draw_f1', 'Draw_f2', 'sig_str_f1', 'sig_str_att_f1', 'sig_str_f2',
                   'sig_str_att_f2', 'time_min_x', 'time_min_y', 'ctrl_f1', 'ctrl_f2']]
#df_fighter.fillna(0, inplace=True)
# next area to automate - will add some of the f1 and f2 fields to make the data more usable
df_fighter.fillna(0, inplace=True)
df_fighter.rename(columns={'fighter_name_1': 'name', 'event_name': 'wins', 'method': 'losses'}, inplace=True)
df_fighter['total'] = df_fighter['wins'] + df_fighter['losses']
df_fighter['rounds'] = df_fighter['round_x'] + df_fighter['round_y']
df_fighter['kd'] = df_fighter['kd_1'] + df_fighter['kd_2']
df_fighter['kd_round'] = (df_fighter['kd']) / (df_fighter['rounds'])
df_fighter['t_wins'] = df_fighter['Wins_f1'] + df_fighter['Wins_f2']
df_fighter['t_losses'] = df_fighter['Losses_f1'] + df_fighter['Losses_f2']
df_fighter['t_nc'] = df_fighter['NC_f1'] + df_fighter['NC_f2']
df_fighter['t_draws'] = df_fighter['Draw_f1'] + df_fighter['Draw_f2']
df_fighter['win_p'] = df_fighter['t_wins'] / df_fighter['total']
df_fighter['sig_strikes'] = df_fighter['sig_str_f1'] + df_fighter['sig_str_f2']
df_fighter['sig_strikes_att'] = df_fighter['sig_str_att_f1'] + df_fighter['sig_str_att_f2']
df_fighter['rounds_per_fight'] = df_fighter['rounds'] / df_fighter['total']
df_fighter['time_min'] = df_fighter['time_min_x'] + df_fighter['time_min_y']
df_fighter['time_per_fight'] = df_fighter['time_min'] / df_fighter['total']
df_fighter['sig_str_per_min'] = df_fighter['sig_strikes'] / df_fighter['time_min']
df_fighter['ground_control'] = df_fighter['ctrl_f1'] + df_fighter['ctrl_f2']
# trim fighter dataframe to select columns
df_fighter = df_fighter.loc[:, ['name', 't_wins', 't_losses', 't_nc', 't_draws', 'total',
                                          'rounds', 'kd', 'kd_round', 'win_p', 'sig_strikes', 'sig_strikes_att',
                                          'rounds_per_fight', 'time_min', 'time_per_fight',
                                          'sig_str_per_min', 'ground_control']]
# save data as csv for future use
by_date = False
if by_date:
    current_date = date.today()
    date_out =  '_' + str(current_date.year) + '_' + str(current_date.month) + '_' + str(current_date.day)
else:
    date_out = ''

df.to_csv(r'data/ufc_data' + date_out + '.csv')
df_fighter.to_csv(r'data/ufc_fighter' + date_out + '.csv')
df_group_count.to_csv(r'data/ufc_group_count' + date_out + '.csv')

