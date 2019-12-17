#!/usr/bin/env python3
"""
@authors: climatebrad, anilca-lab

Usage:

> import data_cleaner as dc

load data from pickled dataframe; if the pickle doesn't exist, will generate from the raw year CSVs: 
> data = dc.load_full_sqf()

if you want to force a regeneration of the pickle (e.g. if you are editing data_cleaner):

> data = dc.load_full_sqf(force=True)

load a single year's data from the raw CSV:

> data17 = dc.load_sqf(2017)

2017 and 2018 CSVs are in a different format than the rest of the years. If you don't want them to be converted:

> data17 = dc.load_sqf(2017, convert=False)

"""
import re
import os.path
import pandas as pd
import numpy as np

from data_dicts import *
from clean_cat_values import CLEAN_CAT_VALUES


def sqf_excel_to_csv(infile, outfile, dirname='../data/stop_frisk'):
    """read in the sqf excel file and output csv file."""
    data = pd.read_excel(f'{dir}/{infile}', na_values='(null)')
    data.to_csv(f'{dirname}/{outfile}.csv', index=False)

def format_time(t_str):
    """make sure timestops have colon between hour and minute"""
    if t_str == t_str: # skip NaN
        t_str = t_str.strip().zfill(4)
        if t_str[2] != ':':
            return t_str[:2] + ':' + t_str[2:]
        if re.match('(\d{2}):(\d{2}):(\d{2})', t_str):
            m = re.match('(\d{2}:\d{2}):(\d{2})', t_str)
            t_str = m[1]
        return t_str
    return t_str

def format_date(date_str):
    """make sure datestops in monthdayyear format"""
    if date_str == date_str: # skip NaN
        date_str = date_str.strip().zfill(8)
        if re.match('(\d{4})-(\d{2})-(\d{2})', date_str):
            m = re.match('(\d{4})-(\d{2})-(\d{2})', date_str)
            date_str = f'{m[2]}{m[3]}{m[1]}'
    return date_str



def add_datetimestop(data):
    """Concatenate date and time fields into a datetime field. Edits dataframe in place"""
    data['datetimestop'] = pd.to_datetime(data.datestop.apply(format_date) \
                                          + data.timestop.apply(format_time),
                                          format='%m%d%Y%H:%M',
                                          errors='coerce')
#    data = data.drop(columns=['datestop', 'timestop'])
    return data

def add_datetimestops(data_dict):
    """update the dataframes in a data_dict with datetimestop field."""
    for year in data_dict:
        print(f'Processing {year}...')
        add_datetimestop(data_dict[year])
    print('Done.')

def add_height(data):
    """Convert ht_feet, ht_inch to height in inches"""
    data['height'] = data['ht_feet'] * 12 + data['ht_inch']
    return data


def y_n_to_1_0(col, yes_value='Y', set_na=True):
    """convert Y/N column to 1/0 column. set_na keeps blanks as NaN, if false sets to 0"""
    out_col = pd.Series(np.where(col.isin([yes_value, '1']), 1, 0), col.index).astype('int8')
    if set_na:
        out_col[col.isna()] = np.NaN
    return out_col

def y_n_to_1_0_cols(data, cols=Y_N_COLS, yes_value='Y', set_na=True):
    """convert Y/N columns to 1/0 columns. set_na keeps blanks as NaN, if false sets to 0"""
    for y_n_col in Y_N_COLS:
        if y_n_col in data:
            data[y_n_col] = y_n_to_1_0(data[y_n_col], yes_value, set_na)

def height_to_feet_inch(data, height_col):
    """Convert the height_col column to ht_feet, ht_inch
    'SUSPECT_HEIGHT' : '{ht_feet}.{ht_inch}'"""
    # note there are some spurious entries in the SUSPECT_HEIGHT column
    data[['ht_feet', 'ht_inch']] = data[height_col].str.split('.', 1, expand=True)
    # sometimes SUSPECT_HEIGHT is just '5' should go to '5', '0'
    data.loc[data.ht_inch.isna() & data.ht_feet.notna(), 'ht_inch'] = 0
    # convert to int
    data.ht_feet = data.ht_feet.apply(pd.to_numeric).astype('Int64')
    data.ht_inch = data.ht_inch.apply(pd.to_numeric).astype('Int64')
    # deal with junk entries
    data.loc[(data.ht_feet < 3) | (data.ht_feet > 7), ['ht_feet', 'ht_inch']] = np.nan
    data.loc[(data.ht_inch > 11), 'ht_inch'] = 0
    data = data.drop(columns=height_col)
    return data

def convert_17_18_data(data):
    """Convert the 2017-2018 data into the 2003-2016 standard
we can convert these:
'STOP_WAS_INITIATED' : { 'Based on Radio Run' :'radio', 'Based on C/W on Scene' : 'ac_rept'}
'JURISDICTION_CODE' : (if 'A' : NaN else 'trhsloc'),

these we'd have to consider adding to the other years as combined columns:
'FIREARM_FLAG' : 'pistol' | 'riflshot' | 'asltweap' | 'machgun',
'PHYSICAL_FORCE_DRAW_POINT_FIREARM_FLAG' : 'pf_ptwep' | 'pf_drwep',
'PHYSICAL_FORCE_RESTRAINT_USED_FLAG' : 'pf_hands' | 'pf_wall' | 'pf_grnd',
'STOP_LOCATION_FULL_ADDRESS' : 'addrnum' + 'stname' + 'stinter' + 'crossst'
    """
    data = data.copy().rename(columns=COL_RENAME)
    
    # convert STOP_WAS_INITIATED
    data['radio'] = data.STOP_WAS_INITIATED.map(lambda x: 'Y' if x=='Based on Radio Run' else 'N')
    data['ac_rept'] = data.STOP_WAS_INITIATED.map(lambda x: 'Y' if x=='Based on C/W on Scene' else 'N')
    data = data.drop(columns='STOP_WAS_INITIATED')
    
    # convert JURISDICTION CODE
    data.trhsloc = data.trhsloc.map(lambda x: np.NaN if x=='A' else x)
    
    data = height_to_feet_inch(data, 'SUSPECT_HEIGHT')
    
    data = data.replace(REPLACE_DICT)
    data = data.drop(columns=list(UNMATCHED_2017_COLS))
    
    # fix column datatypes
    dtypes = get_dtypes()
    dtypes = {key : dtypes.get(key) for key in data.columns if dtypes.get(key)}
    data = data.astype(dtypes, errors='ignore')
    
    return data

def clean_categories(data):
    """get data categories ready for one-hot-encoding"""
    data = data.replace(CLEAN_CAT_VALUES)
    data = data.dropna(subset=CLEAN_CAT_VALUES.keys()).astype('object').astype('category')
    return data


def get_dtypes(on_input=True):
    """Return full dict of dtypes, for on_input or output."""
    dtypes = {'repcmd' : str,
              'revcmd' : str,
              'stname' : str,
              'datestop' : str,
              'timestop' : str,
              'sumoffen' : str,
              'addrnum' : str,
              'othfeatr' : str,
              'recstat' : str,
              'pct' : 'Int64',
              'ht_feet' : 'Int64',
              'ht_inch' : 'Int64',
              'beat' : 'Int64',
              'addrpct' : 'Int64',
              'year' : 'Int64'
              }
    for col in Y_N_COLS:
        if on_input:
            dtypes.update({col : 'category'})
        else:
            dtypes.update({col : 'int8'})
    for col in CAT_COLS:
        dtypes.update({col : 'category'})
    if not on_input:
        for key in IGNORE_COLS + ('datestop', 'timestop'):
            if key in dtypes:
                dtypes.pop(key)
                
    return dtypes
        
def load_sqf(year, dirname='../data/stop_frisk', convert=True):
    """Load and clean sqf csv file by year. 
    convert=True if 2017, 2018 should be converted to pre-2017 format."""
    print(f'Loading {year}...')
    # '*' is a na_value for the beat variable
    # '12311900' is a na_value for DOB
    
    if year in (2017, 2018):
        data = pd.read_csv(f'{dirname}/{year}.csv',
                           encoding='cp437',
                           dtype = {'SUSPECT_HEIGHT' : str,
                                    'PHYSICAL_FORCE_OC_SPRAY_USED_FLAG' : 'str',
                                    'PHYSICAL_FORCE_WEAPON_IMPACT_FLAG' : 'str'},
                           na_values=NA_VALUES,
                           usecols = lambda x : x not in IGNORE_COLS
                          )
        if convert:
            data = convert_17_18_data(data)
    else:      
        data = pd.read_csv(f'{dirname}/{year}.csv',
                           encoding='cp437',
                           na_values=NA_VALUES,
                           dtype=get_dtypes())
        # fix 2006 column names
        data = data.rename(columns={'adrnum' : 'addrnum',
                                    'adrpct': 'addrpct',
                                    'dettyp_c' : 'dettypcm',
                                    'rescod' : 'rescode',
                                    'premtyp' : 'premtype',
                                    'prenam' : 'premname',
                                    'strintr' : 'stinter',
                                    'strname' : 'stname',
                                    'details_' : 'detailcm'})
    if convert or year < 2017: 
        data = add_datetimestop(data)
        # 999 is a na_value for the precinct variable
        data.pct = data.pct.replace({999: np.nan, 208760: np.nan})
        data.columns = data.columns.str.lower()
        data = data.dropna(subset=['pct'])
        # convert ht_feet, ht_inch to height 
        data = add_height(data)
        # convert yes-no columns to 1-0
        y_n_to_1_0_cols(data)
        
    return data

def load_sqfs(start=2003, end=2018, dirname='../data/stop_frisk'):
    """Loads sqf data in format dir/<year>.csv into dict of dataframes
    Currently works for years in 2003 to 2016"""
    stop_frisks = {}
    for year in range(start, end + 1):
        stop_frisks[year] = load_sqf(year, dirname)
    print("Done.")
    return stop_frisks


def load_filespecs(start=2003, end=2017, dirname='../data/stop_frisk/filespecs'):
    """Loads filespecs from files named '<year> SQF File Spec.xlsx'
    for years in 2003 to 2017 (inclusive)"""
    return {year : pd.read_excel(f'{dirname}/{year} SQF File Spec.xlsx',
                                 header=3) for year in range(start, end + 1)}

def add_all_columns(data):
    """Make sure dataframe data has all the possible columns with the correct datatypes."""
    dtypes = get_dtypes(on_input=False)
    newcols = { col : dtype for col, dtype in dtypes.items() if col not in data}
    newcols = { col : np.NaN for col in newcols}
    data = data.assign(**newcols)
    data = data.fillna({col : 0 for col in Y_N_COLS})
    data = data.astype(dtypes)
    return data
    
def concat_dict_of_dfs(df_dict):
    """when we want to concatenate the years"""
    # we should probably be using merge instead of concat, which is better at handling categorical columns
    df_dict = {year : add_all_columns(data) for year, data in df_dict.items()}
    data = pd.concat(df_dict.values(), sort=False, ignore_index=True)
    dtypes = get_dtypes(on_input=False)
    data = data.astype(dtypes)
    return data


def clean_and_save_full_sqfs(indirname='../data/stop_frisk', outdirname='../data'):
    """Create and save full stop-and-frisks data from raw files"""
    data = concat_dict_of_dfs(load_sqfs(dirname=indirname))
    data.to_pickle(f'{outdirname}/full_stop_frisks_df.pkl')
    return data


def load_full_sqf(dirname='../data/', create=True, force=False):
    """Load the cleaned 2003-2018 dataframe. 
create=True will generate the dataframe pickle if it doesn't exist. 
force=True generates the dataframe pickle, overwriting if previously exists"""
    if force or (create and (not os.path.exists(f'{dirname}/full_stop_frisks_df.pkl'))):
        data = clean_and_save_full_sqfs(indirname=f'{dirname}/stop_frisk', outdirname=dirname)
        return data
    return pd.read_pickle(f'{dirname}/full_stop_frisks_df.pkl')

