# -*- coding: utf-8 -*-
"""
Onondaga_develpoment

Retrieve demographic data from American Community Survey 5-year data (2021) 
to identify populations in Onondaga County, particularly communities that are 
traditionaly underrepresented in tech. 

@author: Yerouap
"""

#import modules
import requests
#module
import pandas as pd
#module
import numpy as np

#%%
#       Retrieve demographic data 
#
# set keys to rename census variables
variables = {'B02001_001E':'pop_total',
             'B02001_002E':'pop_white',
             'B02001_003E':'pop_black',
             'B03001_003E':'pop_hispanic_latino',
             'B25003_001E':'housing_total',
             'B25003_002E':'housing_owned',
             'B25003_003E':'housing_rental',
             'B19013_001E': 'Median household income',
             'B19001_001E': 'Total household income',
        'B17001_001E':'tot pop poverty determined', 
            'B17001_002E': 'tot pop below pov',
            'B17001_003E': 'tot pop at or above pov',
            'B25070_001E': 'Median gross rent',
           'B25071_001E': 'Median owner cost as a percentage of household income',
           'B25077_001E': 'Median value of owner-occupied housing units'
                                                                           }

# set keys as list
var_list = variables.keys()
var_string = ','.join(var_list)

#%%
#
# endpoint for API retrieval - Detailed Tables 
api = 'https://api.census.gov/data/2021/acs/acs5'

# set payload : parameters for data retrieval 
get_clause = var_string
for_clause = 'tract:*'
in_clause = 'state:36 county:067'

# personal API key
key_value =  '2f01ed011472c0feb42831c7f77f0cef4035a942'

# group parameters for data retrieval 
payload = {'get': get_clause,
           'for': for_clause,
           'in': in_clause,
           'key': key_value}

#%%
#
# ???HTTPS query string to collect response from API endpoint
response = requests.get(api, payload)

# test request
if response.status_code == 200:
    print('\nzero=0=good')
else:
    print(response.status_code)
    print(response.text)
    assert False    

# return rows as list and convert to datatframe
row_list = response.json()
colnames = row_list[0]
datarows = row_list[1:]
pop = pd.DataFrame(columns=colnames, data=datarows)

#%%
#
# deal with missing data
pop = pop.replace('-666666666', np.nan)
pop = pop.replace('-666666666.0', np.nan)

# rename columns
pop = pop.rename(columns=variables)

# concatenate columns
pop['GEOID'] = pop['state']+pop['county']+pop['tract']
# +pop['block group']

# set index
pop = pop.set_index('GEOID')

# ???list
keep_cols = list(variables.values())

# trim pop!!
pop= pop[keep_cols]

#%%
#
#group traditionaly underrepresented communities
pop['pop_black'] = pop['pop_black'].fillna(0)
pop['pop_hispanic_latino'] = pop['pop_hispanic_latino'].fillna(0)
pop['pop_poc'] = pop['pop_black'].astype(int) + pop['pop_hispanic_latino'].astype(int)

#%%
#
##write pop to csv
pop.to_csv('oc_pops.csv')

#%%













