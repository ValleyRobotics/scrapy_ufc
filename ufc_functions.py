import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt

# change display settings
#pd.set_option('display.max_rows', None)
#pd.set_option('display.width', 4000)
#pd.set_option('display.max_columns', None)
#head_ = 12
# data to be used
# dict for fighter 1
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


def pretty_print(str="I'm too lazy to add comment", max=206):
    ''' Just a function to make the printed output stand out'''
    str_l = len(str)
    print('*' * (max + 1))
    l = int((max - str_l) / 2)
    print('*' * l, str, '*' * l)
    print('*' * (max + 1))
    return

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


# end functions