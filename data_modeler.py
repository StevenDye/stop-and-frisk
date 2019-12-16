"""
@author: climatebrad
"""

import os.path
from statsmodels.formula.api import ols
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

def load_split(X, y, **kwargs):
    """basic wrapper for train_test_split"""
    X_train, X_test, y_train, y_test = train_test_split(X, y, **kwargs)
    return {'X_train' : X_train, 'X_test' : X_test, 'y_train' : y_train, 'y_test' : y_test }