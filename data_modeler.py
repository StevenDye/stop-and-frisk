"""
@author: climatebrad
"""

import os.path
from statsmodels.formula.api import ols
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

PRE_STOP_OBSERVABLES = ['year', 'pct', 'ser_num', 'datestop', 'timestop', 'inout',
                        'trhsloc', 'perobs', 'crimsusp', 'offunif', 'cs_objcs', 
                        'cs_descr', 'cs_casng', 'cs_lkout', 'cs_cloth', 'cs_drgtr',
                        'cs_furtv', 'cs_vcrim', 'cs_bulge', 'cs_other', 'ac_incid',
                        'ac_time', 'ac_stsnd', 'ac_other', 'repcmd', 'revcmd', 'age',
                        'sex', 'race', 'height', 'weight', 'haircolr', 'eyecolor', 
                        'build', 'othfeatr', 'addrtyp', 'rescode', 'premtype',
                        'premname', 'addrnum', 'sector', 'beat', 'post', 'xcoord', 
                        'ycoord', ]

DURING_STOP_OBSERVABLES = ['recstat', 'perstop', 'typeofid', 'explnstp', 'othpers',
                         'officrid', 'frisked', 'searched', 'contrabn', 'adtlrept',
                         'pistol', 'riflshot', 'asltweap', 'knifcuti', 'machgun',
                         'othrweap', 'pf_hands', 'pf_wall', 'pf_grnd', 'pf_drwep',
                         'pf_ptwep', 'pf_baton', 'pf_hcuff', 'pf_pepsp', 'pf_other',
                         'radio', 'ac_rept', 'ac_inves', 'rf_vcrim', 'rf_othsw',
                         'ac_proxm', 'rf_attir', 'rf_vcact', 'ac_evasv', 'ac_assoc',
                         'rf_rfcmp', 'ac_cgdir', 'rf_verbl', 'rf_knowl', 'sb_hdobj',
                         'sb_outln', 'sb_admis', 'rf_furt', 'rf_bulg', 'offverb', 
                         'offshld', 'forceuse', 'dob', 'dettypCM', 'lineCM', 
                         'detailCM']

TARGETS = ['arstmade', 'arstoffn', 'sumissue', 'sumoffen', 'compyear', 'comppct']

def load_split(X, y, **kwargs):
    """basic wrapper for train_test_split"""
    X_train, X_test, y_train, y_test = train_test_split(X, y, **kwargs)
    return {'X_train' : X_train, 'X_test' : X_test, 'y_train' : y_train, 'y_test' : y_test }