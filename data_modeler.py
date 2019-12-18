"""
@author: climatebrad, StevenDye
"""

import os.path
from statsmodels.formula.api import ols
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE

PRE_STOP_OBSERVABLES = {'month', 'day', 'pct_sector', 'inout',
                        'trhsloc', 'perobs', 'crimsusp', 'offunif', 'cs_objcs', 
                        'cs_descr', 'cs_casng', 'cs_lkout', 'cs_cloth', 'cs_drgtr',
                        'cs_furtv', 'cs_vcrim', 'cs_bulge', 'cs_other', 'ac_incid',
                        'ac_time', 'ac_stsnd', 'ac_other', 'age',
                        'sex', 'race', 'height', 'weight', 'haircolr', 'eyecolor', 
                        'build', 'addrtyp', 
                        'premname',}

DURING_STOP_OBSERVABLES = {'recstat', 'perstop', 'typeofid', 'explnstp', 'othpers',
                         'officrid', 'frisked', 'searched', 'contrabn', 'adtlrept',
                         'pistol', 'riflshot', 'asltweap', 'knifcuti', 'machgun',
                         'othrweap', 'pf_hands', 'pf_wall', 'pf_grnd', 'pf_drwep',
                         'pf_ptwep', 'pf_baton', 'pf_hcuff', 'pf_pepsp', 'pf_other',
                         'radio', 'ac_rept', 'ac_inves', 'rf_vcrim', 'rf_othsw',
                         'ac_proxm', 'rf_attir', 'rf_vcact', 'ac_evasv', 'ac_assoc',
                         'rf_rfcmp', 'ac_cgdir', 'rf_verbl', 'rf_knowl', 'sb_hdobj',
                         'sb_outln', 'sb_admis', 'rf_furt', 'rf_bulg', 'offverb', 
                         'offshld', 'forceuse', 'dob', 'dettypCM', 'lineCM', 
                         'detailCM'}



TARGETS = {'arstmade', 'arstoffn', 'sumissue', 'sumoffen'}

def load_split(X, y, **kwargs):
    """basic wrapper for train_test_split"""
    X_train, X_test, y_train, y_test = train_test_split(X, y, **kwargs)
    return {'X_train' : X_train, 'X_test' : X_test, 'y_train' : y_train, 'y_test' : y_test }

def run_logit(split, **kwargs):
    """run logistic regression 
good defaults: solver='saga', penalty='l1', max_iter=4000"""
    smote = SMOTE()
    X_train_resampled, y_train_resampled = smote.fit_sample(split['X_train'], split['y_train']) 
    logit = LogisticRegression(**kwargs)
    logit.fit(X_train_resampled, y_train_resampled)
    return logit
    
def print_residuals(split, logit):
    """print residutals from logit run"""
    y_hat_train = logit.predict(split['X_train'])
    residuals = np.abs(split['y_train'] - y_hat_train)
    print("Train\n", pd.Series(residuals).value_counts())
    print(pd.Series(residuals).value_counts(normalize=True))
    y_hat_test = logit.predict(split['X_test'])
    residuals = np.abs(split['y_test'] - y_hat_test)
    print("Test\n", pd.Series(residuals).value_counts())
    print(pd.Series(residuals).value_counts(normalize=True))
    
def split_and_logit(X, y, **kwargs):
    """do a split then run logit """
    split = load_split(X, y, **kwargs)
    logit = run_logit(split, solver='saga', penalty='l1', max_iter=4000)
    print_residuals(split, logit)
    return split, logit


def fill_NaNs(X):
    """Fill all missing values in a dataframe with 'NoVal' entry"""
    category_list = X.columns.to_list()
    X_nona = pd.DataFrame()
    for category in category_list:
        X_nona[category] = X[category].cat.add_categories('NoVal').fillna('NoVal')
    return X_nona


def categorical_encoder(X, handle_unknown='ignore', **kwargs):
    """One hot encodes categorical data in a dataframe.
Default value handle_unkown='ignore', since possible categories in 
test will not be in train"""
    encoder = OneHotEncoder(handle_unknown=handle_unknown, **kwargs)
    encoder.fit(X)
    return encoder


def run_rf(X_train, y_train, max_depth=2, **kwargs):
    """run random forest: good defaults: max_depth=2"""
    smote = SMOTE()
    X_train_resampled, y_train_resampled = smote.fit_sample(X_train, y_train) 
    rf = RandomForestClassifier(max_depth=max_depth, **kwargs)
    rf.fit(X_train_resampled, y_train_resampled)
    return rf

def run_all(data):
    X_category = data.select_dtypes(include='category')
    X_noncat = data.select_dtypes(exclude='category')
    y = data.arstmade
    X = fill_NaNs(X_category)
    X = categorical_encoder(X)
    split = load_split(X, y, stratify=y)
    clf = run_rf(split, max_depth=2)
    print(clf.feature_importances_)
    print(balanced_accuracy_score(split['y_test'], clf.predict['X_test']))
    return split, clf

def encode_X_cat(X_train, **kwargs):
    """"one-hot-encode categorical variables in X_train, return merged dataframe"""
    X_cat = X_train.select_dtypes(include='category')
    X_noncat = X_train.select_dtypes(exclude='category')
    X_cat = fill_NaNs(X_cat)
    cat_encoder = categorical_encoder(X_cat, **kwargs)
    X_cat_ohe = cat_encoder.transform(X_cat)
    X_ohe_df = pd.DataFrame(X_cat_ohe.toarray(), 
                            columns=cat_encoder.get_feature_names(X_cat_ohe.columns),
                            index=X_cat.index)
    X_result = X_noncat.join(X_ohe_df)
    return X_result
     
