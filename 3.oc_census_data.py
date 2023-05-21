# -*- coding: utf-8 -*-
"""
Onondaga_development
 
@author: Yerouap
May 2023
"""
#       - Import modules - 
#

import requests      # to resuest data from Census server
import pandas as pd  # to manipulate and structure data
import numpy as np   # to work with numeric data

#%%
#       - Retrieve economic and demographic data from census -
#
# set keys to rename census variables
variables = {'B02001_001E':'pop_total',
             'B02001_002E':'pop_white',
             'B02001_003E':'pop_black',
             'B03001_003E':'pop_hispanic_latino',
             'B25003_001E':'housing_total',
             'B25003_002E':'housing_owned',
             'B25003_003E':'housing_rental',
             'B19013_001E':'med_hh_income',
             'B19001_001E':'tot_hh_income',
             'B17001_001E':'tot_pop_measured_poverty', 
             'B17001_002E':'tot_pop_below_poverty',
             'B17001_003E':'tot_pop >= poverty',
             'B25070_001E':'med_gross_rent',
             'B25071_001E':'med_owner_cost%',   # cost given as percentage of household income
             'B25077_001E':'med_value_owner-occupied_housing_units'
                                                                           }

# set keys as list
var_list = variables.keys()
#format keys for API request
var_string = ','.join(var_list)

#%%
#       - Create Census API request - 
#
# set endpoint: Census ACS5 - Detailed Tables 
api = 'https://api.census.gov/data/2021/acs/acs5'

# set payload: parameters for data retrieval 
#   specify variables 
get_clause = var_string
#   select geographic entity
for_clause = 'tract:*'
#   specify location within entity: New York State and Onondaga County
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
# send HTTP get request to collect response from API endpoint
response = requests.get(api, payload)

# test for successful request
if response.status_code == 200:
    print('\nsuccess')
else:
    print(response.status_code)
    print(response.text)
    assert False    

# return rows of data as list and convert to datatframe
row_list = response.json()
colnames = row_list[0]
datarows = row_list[1:]
pop = pd.DataFrame(columns=colnames, data=datarows)

#%%
#       - clean request -
#
# deal with missing data
pop = pop.replace('-666666666', np.nan)
pop = pop.replace('-666666666.0', np.nan)

# rename columns
pop = pop.rename(columns=variables)

#%%
#       - Create new variables -
#
# concatenate columns to create GEOIDs 
pop['GEOID'] = pop['state']+pop['county']+pop['tract']
# +pop['block group']

# set index
pop = pop.set_index('GEOID')
# drop individual columns used ot create GEOIDs
keep_cols = list(variables.values())
pop= pop[keep_cols]

#group traditionaly underrepresented communities
pop['pop_black'] = pop['pop_black'].fillna(0)
pop['pop_hispanic_latino'] = pop['pop_hispanic_latino'].fillna(0)
pop['pop_poc'] = pop['pop_black'].astype(int) + pop['pop_hispanic_latino'].astype(int)

#%%
#       - Save results -
#
# as csv
pop.to_csv('oc_pops.csv')



