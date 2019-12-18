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

USE_OTHER_VALUES = {
    'premname' : [
        'LOBBY', 'PARK', 'HALLWAY', 
        'WALKWAY', 'PARKING LOT',
        'SUBWAY', 'NYCHA', 'CAR', 'PLAYGROUND'
    ],
    'crimsusp' : [
        'GRAND LARCENY', 'PETIT LARCENY', 'LOITERING',
        'CRIMINAL MISCHIEF', 'HOMICIDE', 'RAPE',
        'SEXUAL ABUSE', 'GAMBLING', 'KIDNAPPING',
    ]
}

REPLACE_REVERSE_DICT = {
    'premname' : {
        'STREET' : [
            'ST',
            'PUBLIC STREET',
            'STREET CORNER'
        ],
        'MEZZ' : ['MEZZANINE'],
        'SIDEWALK' : ['PUBLIC SIDEWALK'],
        'RESIDENTIAL' : [
            'APT BUILDING',
            'APARTMENT',
            'APT',
            'RES',
            'APT. BUILDING',
            'HOUSE',
            'PRIVATE HOUSE',
            'RESIDENCE',
            'APARTMENT BUILDING'
        ],
        'BUILDING' : ['BLDG'],
        'STAIRWELL' : ['STAIRCASE'],
        'COMMERCIAL' : [
            'COMM', 
            'STORE'
        ]
    },
    'crimsusp' : {
        'FELONY' : [
            'FEL',
            'F'
        ],
        'ASSAULT' : [
            'ASSAULT 3',
            'ASSAULT 2',
            'ASSAULT 1',
        ],
        'MISDEMEANOR' : [
            'M',
            'MISD',
            'MIS/CPW',
        ],
        'CRIMINAL POSSESSION WEAPON' : [
            'CPW',
            'CPW 3',
            'CPW 4',
            'C.P.W.',
            'CRIMINAL POSSESSION OF WEAPON',
            'C.P.W',
            'CPW GUN',
            'CPW FIREARM',
            'FELONY CPW',
            'CPW FELONY',
        ],
        'CRIMINAL TRESPASS' : [
            'CRIMINAL TRESSPASS',
            'CRIM TRES',
            'CRIM TRESS',
            'TRESPASSING',
            'CRIMINAL  TRESSPASS',
            'CRIM. TRESP.',
            'CRIMINAL TRES',
            'CRIM TRESSPASS',
            'MIS/CRIM TRES',
        ],
        'BURGLARY' : [
            'BURG',
            'BURG.'
        ],
        'ROBBERY' : [
            'ROB',
            'ROBBERY PATTERN',
            'ROBBERY/CPW',
            'CPW/ROBBERY',
            'ROBB',
            'ROBBERY 1',
            'FELONY/ROBBERY',
        ],
        'GRAND LARCENY AUTO' : [
            'GLA',
            'GLA - GRAND LARCENY AUTO',
            'G.L.A.',
            'G.L.A',
            'GRAND LARCENY FROM AUTO',
            'GLA/CPW',
            'LARCENY FROM AUTO',
            'AUTO STRIPPING',
        ],
        'CRIMINAL POSSESSION CONTROLLED SUBSTANCE' : [
            'CRIMINAL POSSESSION OF CONTROL',
            'CPCS',
            'CRIMINAL POSSESION OF CONTROLL',
            'CPCS 7',
            'CPCS - CRIMINAL POSSESSION OF',
            'DRUGS' 
        ],
        'CRIMINAL POSSESSION MARIJUANA' : [
            'CRIMINAL POSSESSION OF MARIHUA',
            'CPM',
            'CPM - CRIMINAL POSSESSION OF M',
            'CPM 5',
        ],
        'CRIMINAL SALE CONTROLLED SUBSTANCE' : [
            'CRIMINAL SALE OF CONTROLLED SU', 
            'DRUG SALES', 
            'CSCS', 
            'CSCS - CRIMINAL SALE OF CONTRO', 
            'C.S.C.S.',
            'NARCOTIC SALES',
            'DRUG/SALES',
        ],
        'CRIMINAL SALE MARIJUANA' : [
             'CRIMINAL SALE OF MARIHUANA',   
             'CRIMINAL SALE OF MARIJUANA',
        ],
        'GRAFFITI' : [
            'MAKING GRAFFITI'
        ],
        'PROSTITUTION' : [
            'LOITERING FOR PROSTITUTION'
        ],
        'CRIMINAL POSSESSION STOLEN PROPERTY' : [
            'CRIMINAL POSSESSION STOLEN PRO',
            'CPSP',
            'C.P.S.P.',
        ]
    }
}
