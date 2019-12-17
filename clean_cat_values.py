import numpy as np

CLEAN_CAT_VALUES = {
    'inout' : { 'S' : 'O' }, # inside or outside -> S = street (we assume)
    'eyecolor' : { 
        'P' : 'ZZ', # pink -> other
        'PK' : 'ZZ', # pink -> other
    },
}

CAT_FILL_NA_VALUES = {
    'trhsloc' :  'P', #transit, housing authority -> P = neither
    'typeofid' : 'O', # type of id from stopped person -> O = other
    'sector' : 'Z', # should be calculated from pct, fill with dummy value for now
}

MODEL_IGNORE_COLS = [
    'recstat', # don't know what this is
    'forceuse', # only used in some years, don't know what values mean
]