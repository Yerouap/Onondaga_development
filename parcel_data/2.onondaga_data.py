# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 22:51:37 2023

@author: Yerouap
"""


import requests
import pandas as pd
import numpy as np

#ADD new vars?!
#set keys to rename census data
variables = {'B02001_001E':'pop_total',
             'B02001_002E':'pop_white',
             'B25003_001E':'housing_total',
             'B25003_002E':'housing_owned',
             'B25003_003E':'housing_rental',
             'B19013_001E': 'Median household income',
             'B19001_001E': 'Total household income'}

var_list = variables.keys()
var_string = ','.join(var_list)



#                       [RETRIEVE CENSUS VARIABLE]
#
api = 'https://api.census.gov/data/2021/acs/acs5'
#
get_clause = var_string
for_clause = 'block group:*'
in_clause = 'state:36 county:067'
#personal API key
key_value =  '2f01ed011472c0feb42831c7f77f0cef4035a942'
#Parameters for data retrieval 
payload = {'get': var_string,
           'for': for_clause,
           'in': in_clause,
           'key': key_value}
#HTTPS query string to collect response from API endpoint
response = requests.get(api, payload)
#Test Request
if response.status_code == 200:
    print('\nzero=0=good')
else:
    print(response.status_code)
    print(response.text)
    assert False    
#return rows as list --> dataframe
row_list = response.json()
colnames = row_list[0]
datarows = row_list[1:]
pop = pd.DataFrame(columns=colnames, data=datarows)


#deal with missing data
pop = pop.replace('-666666666', np.nan)

#rename columns
pop = pop.rename(columns=variables)


#concatenate columns
pop['GEOID'] = pop['state']+pop['county']+pop['tract']+pop['block group']



#set index
pop = pop.set_index('GEOID')
#list??
keep_cols = list(variables.values())
#trim pop!!
pop= pop[keep_cols]

##write pop to csv
pop.to_csv('ocpop_by_bg.csv')



















