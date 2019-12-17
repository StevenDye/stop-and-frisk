import numpy as np

CLEAN_CAT_VALUES = {
    'inout' : { 'S' : np.NaN }, # inside or outside
}

CAT_FILL_NA_VALUES = {
    'trhsloc' :  'P', #transit, housing authority -> P = neither
    'typeofid' : 'O', # type of id from stopped person -> O = other
    'sector' : 'Z', # should be calculated from pct, fill with dummy value for now
}
