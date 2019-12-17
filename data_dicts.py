"""
author : @climatebrad
"""

import numpy as np

NA_VALUES = (' ', '12311900', '*', '**', '(nul' ,'(n', '(', '(nu')

Y_N_COLS = ('arstmade', 'pistol', 'machgun', 'asltweap',
            'riflshot', 'knifcuti', 'othrweap', 'wepfound',
            'cs_lkout', 'cs_objcs', 'cs_casng', 'cs_cloth', 'cs_descr',
            'cs_drgtr', 'cs_furtv', 'cs_vcrim', 'cs_bulge', 'cs_other',
            'sb_outln', 'sb_other', 'sb_hdobj', 'sb_admis',
            'ac_time', 'ac_rept', 'ac_stsnd', 'ac_proxm',
            'ac_assoc', 'ac_evasv', 'ac_incid', 'ac_cgdir', 'ac_inves', 'ac_other',
            'rf_furt', 'rf_bulg', 'rf_vcrim', 'rf_vcact', 'rf_verbl', 'rf_othsw', 'rf_attir', 'rf_knowl',
            'pf_hands', 'pf_wall', 'pf_grnd', 'pf_drwep', 'pf_ptwep', 'pf_baton', 'pf_hcuff',
            'pf_pepsp', 'pf_other', 'radio', 'rf_rfcmp','officrid', 'offshld', 'offverb',
            'othpers', 'explnstp', 'offunif', 'frisked', 'searched', 'contrabn', 'adtlrept',
            'sumissue', )

REPLACE_VALUES = {
    'pct' : { 999: np.nan, 208760: np.nan },
    'offverb' : {'V' : 'Y', '0' : 'N' }, # verbal statement provided by officer (if not in uniform)
    'offshld' : {'S' : 'Y', '0' : 'N' }, # shield provided by officer (if not in uniform)  
    'city' : {'STATEN IS' : 'STATEN ISLAND'},
    'eyecolor' : {'Z' : 'ZZ', # other
                  'UN' : 'XX', # unknown
                  'MC' : 'DF', # multicolor -> different
                 },
    'haircolr' : {'ZZZ' : 'ZZ'} # other
}

CAT_COLS =  ('city', # aka boro
             'sector',
             'post',      # ignorable column
             'dettypcm',  
             'officrid',
             'rescode',
             'offverb',
             'offshld',
             'forceuse',
             'sex',
             'race',
             'haircolr',
             'eyecolor',
             'build',
             'typeofid',
             'recstat',
             'inout',
             'trhsloc',
             'addrtyp',
             'month',
             'day',
             'pct_sector')

IGNORE_COLS = ('detail1_', 
               'linecm', 
               'post', 
               'comppct', # never used
               'compyear', # never used
               'state', # always NY
               'rescode',
              )

UNMATCHED_2017_COLS = ('ISSUING_OFFICER_RANK',
 'SUPERVISING_OFFICER_RANK',
 'JURISDICTION_DESCRIPTION',
 'OFFICER_NOT_EXPLAINED_STOP_DESCRIPTION',
 'SUPERVISING_ACTION_CORRESPONDING_ACTIVITY_LOG_ENTRY_REVIEWED',
 'PHYSICAL_FORCE_CEW_FLAG',
 'PHYSICAL_FORCE_VERBAL_INSTRUCTION_FLAG',
 'SEARCH_BASIS_CONSENT_FLAG',
 'DEMEANOR_OF_PERSON_STOPPED',
 'STOP_LOCATION_PATROL_BORO_NAME',
 'BACKROUND_CIRCUMSTANCES_SUSPECT_KNOWN_TO_CARRY_WEAPON_FLAG',
 'SUSPECTS_ACTIONS_CONCEALED_POSSESSION_WEAPON_FLAG',
 'SUSPECTS_ACTIONS_IDENTIFY_CRIME_PATTERN_FLAG',
 'SEARCH_BASIS_INCIDENTAL_TO_ARREST_FLAG',
 'FIREARM_FLAG',
 'PHYSICAL_FORCE_DRAW_POINT_FIREARM_FLAG',
 'PHYSICAL_FORCE_RESTRAINT_USED_FLAG',
 'STOP_LOCATION_FULL_ADDRESS')

COL_RENAME = {'STOP_FRISK_ID' : 'ser_num',
 'STOP_FRISK_DATE' : 'datestop',
 'STOP_FRISK_TIME' : 'timestop',
 'Stop Frisk Time' : 'timestop',
 'YEAR2' : 'year',
 'MONTH2' : 'month',
 'DAY2' : 'day',
 'RECORD_STATUS_CODE' : 'recstat',
 'ISSUING_OFFICER_COMMAND_CODE' : 'repcmd',
 'SUPERVISING_OFFICER_COMMAND_CODE' : 'revcmd',
 'LOCATION_IN_OUT_CODE' : 'inout',
 'OBSERVED_DURATION_MINUTES' : 'perobs',
 'SUSPECTED_CRIME_DESCRIPTION' : 'crimsusp',
 'STOP_DURATION_MINUTES' : 'perstop',
 'OFFICER_EXPLAINED_STOP_FLAG' : 'explnstp',
 'OTHER_PERSON_STOPPED_FLAG' : 'othpers',
 'SUSPECT_ARRESTED_FLAG' : 'arstmade',
 'SUSPECT_ARREST_OFFENSE' : 'arstoffn',
 'SUMMONS_ISSUED_FLAG' : 'sumissue',
 'SUMMONS_OFFENSE_DESCRIPTION' : 'sumoffen',
 'OFFICER_IN_UNIFORM_FLAG' : 'offunif',
 'ID_CARD_IDENTIFIES_OFFICER_FLAG' : 'officrid',
 'SHIELD_IDENTIFIES_OFFICER_FLAG' : 'offshld',
 'VERBAL_IDENTIFIES_OFFICER_FLAG' : 'offverb',
 'FRISKED_FLAG' : 'frisked',
 'SEARCHED_FLAG' : 'searched',
 'OTHER_CONTRABAND_FLAG' : 'contrabn',
 'KNIFE_CUTTER_FLAG' : 'knifcuti',
 'OTHER_WEAPON_FLAG' : 'othrweap',
 'WEAPON_FOUND_FLAG' : 'wepfound',
 'PHYSICAL_FORCE_HANDCUFF_SUSPECT_FLAG' : 'pf_hcuff',
 'PHYSICAL_FORCE_OC_SPRAY_USED_FLAG' : 'pf_pepsp',
 'PHYSICAL_FORCE_OTHER_FLAG' : 'pf_other',
 'PHYSICAL_FORCE_WEAPON_IMPACT_FLAG' : 'pf_baton',
 'BACKROUND_CIRCUMSTANCES_VIOLENT_CRIME_FLAG' : 'cs_vcrim',
 'SUSPECTS_ACTIONS_CASING_FLAG' : 'cs_casng',
 'SUSPECTS_ACTIONS_DECRIPTION_FLAG' : 'cs_descr',
 'SUSPECTS_ACTIONS_DRUG_TRANSACTIONS_FLAG' : 'cs_drgtr',
 'SUSPECTS_ACTIONS_LOOKOUT_FLAG' : 'cs_lkout',
 'SUSPECTS_ACTIONS_OTHER_FLAG' : 'cs_other',
 'SUSPECTS_ACTIONS_PROXIMITY_TO_SCENE_FLAG' : 'ac_proxm',
 'SEARCH_BASIS_ADMISSION_FLAG' : 'sb_admis',
 'SEARCH_BASIS_HARD_OBJECT_FLAG' : 'sb_hdobj',
 'SEARCH_BASIS_OTHER_FLAG' : 'sb_other',
 'SEARCH_BASIS_OUTLINE_FLAG' : 'sb_outln',
 'DEMEANOR_CODE' : 'dettypcm',
 'SUSPECT_REPORTED_AGE' : 'age',
 'SUSPECT_SEX' : 'sex',
 'SUSPECT_RACE_DESCRIPTION' : 'race',
 'SUSPECT_WEIGHT' : 'weight',
 'SUSPECT_BODY_BUILD_TYPE' : 'build',
 'SUSPECT_EYE_COLOR' : 'eyecolor',
 'SUSPECT_HAIR_COLOR' : 'haircolr',
 'SUSPECT_OTHER_DESCRIPTION' : 'othfeatr',
 'STOP_LOCATION_PRECINCT' : 'pct',
 'STOP_LOCATION_SECTOR_CODE' : 'sector',
 'STOP_LOCATION_APARTMENT' : 'aptnum',
 'STOP_LOCATION_PREMISES_NAME' : 'premname',
 'STOP_LOCATION_STREET_NAME' : 'stname',
 'STOP_LOCATION_X' : 'xcoord',
 'STOP_LOCATION_Y' : 'ycoord',
 'STOP_LOCATION_ZIP_CODE' : 'zip',
 'STOP_LOCATION_BORO_NAME' : 'city',
 'JURISDICTION_CODE' : 'trhsloc'}

# mapping of build, haircolr, eyecolor for 2017 -> 2016 earlier
REPLACE_2017_DICT = {
    'city' : {'STATEN IS' : 'STATEN ISLAND'},
    'build' : {'THN' : 'T', # thin
               'MED' : 'M', # medium
               'HEA' : 'H', # heavy
               'XXX' : 'Z', # unknown
              },
    'haircolr' : {'BLK' : 'BK', # black
                  'BRO' : 'BR', # brown
                  'BLD' : 'BA', # bald
                  'BLN' : 'BL', # blond
                  'XXX' : 'XX', # unknown
                  'GRY' : 'GY', # gray
                  'WHI' : 'WH', # white
                  'SDY' : 'SN', # sandy
                  'RED' : 'RD', # red
                  'PNK' : 'DY', # pink -> dyed
                  'PLE' : 'DY', # purple -> dyed
                  'GRN' : 'DY', # green -> dyed
                  'ORG' : 'DY', # orange -> dyed 
                 },
    'eyecolor' : {'BRO' : 'BR', # brown
                'BLK' : 'BK', # black
                'ZZZ' : 'XX', # unknown
                'BLU' : 'BL', # blue
                'HAZ' : 'HA', # hazel 
                'GRN' : 'GR', # green
                'GRY' : 'GY', # gray
                'MAR' : 'MA', # marbled?
                'MUL' : 'DF', # mul -> two different
                'OTH' : 'Z',  # other
                 },
    'sex' : {'MALE' : 'M',  # male
             'FEMALE' : 'F' # female
            },
    'race' : {'BLACK' : 'B',
              'WHITE HISPANIC' : 'Q',
              'WHITE' : 'W',
              'BLACK HISPANIC' : 'P',
              'ASIAN/PAC.ISL' : 'A',
              'ASIAN / PACIFIC ISLANDER' : 'A',
              'AMER IND' : 'I',
              'AMERICAN INDIAN/ALASKAN NATIVE' : 'I'},
}



# cleaning the crimsusp entries.
CRIMSUSP_REPLACE_DICT = {
    'CRIMINAL POSSESSION WEAPON' : [
        'CPW',
        'CPW 3',
        'CPW 4',
        'C.P.W.',
        'CRIMINAL POSSESSION OF WEAPON',
        'C.P.W',
        'CPW GUN',
        'CPW FIREARM',
        'FELONY CPW'
    ],
    'CRIMINAL TRESPASS' : [
        'CRIMINAL TRESSPASS',
        'CRIM TRES',
        'CRIM TRESS',
        'TRESPASSING',
        'CRIMINAL  TRESSPASS',
        'CRIM. TRESP.',
        'CRIMINAL TRES',
        'CRIM TRESSPASS'
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
        'ROBBERY 1'
    ],
    'GRAND LARCENY AUTO' : [
        'GLA',
        'GLA - GRAND LARCENY AUTO',
        'G.L.A.',
        'G.L.A',
        'GRAND LARCENY FROM AUTO',
        'GLA/CPW'
    ],
    'CRIMINAL POSSESSION CONTROLLED SUBSTANCE' : [
        'CRIMINAL POSSESSION OF CONTROL',
        'CPCS',
        'CRIMINAL POSSESION OF CONTROLL',
        'CPCS 7'
        'CPCS - CRIMINAL POSSESSION OF'
        'DRUGS' 
    ],
    'CRIMINAL POSSESSION MARIJUANA' : [
        'CRIMINAL POSSESSION OF MARIHUA'
        'CPM'
        'CPM - CRIMINAL POSSESSION OF M'
    ],
    'CRIMINAL SALE CONTROLLED SUBSTANCE' : [
        'CRIMINAL SALE OF CONTROLLED SU', 
        'DRUG SALES', 
        'CSCS', 
        'CSCS - CRIMINAL SALE OF CONTRO', 
        'C.S.C.S.',
        'NARCOTIC SALES',
    ],
    'CRIMINAL SALE MARIJUANA' : [
         'CRIMINAL SALE OF MARIHUANA',   
         'CRIMINAL SALE OF MARIJUANA',
    ]
}
