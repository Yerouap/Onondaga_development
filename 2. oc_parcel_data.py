# -*- coding: utf-8 -*-
"""
Onondaga_development 

Clean, identify, and join Onondaga County parcels data onto geometry...

shoutout - Professor Wilcixen --> for loop
"""


#%%
#       - Import modules -
#
# module 
import geopandas as gpd
# module
import numpy as np
#
import os

#%%
#       - Load Onondaga County parcel data -
#
# set dictionary to define variable type
fips = {
        'STATEFP': str,     
        'COUNTYFP': str,    
        'TRACTCE': str,     
        'GEOID': str,       
       }
       
# read parcel data
raw_parcel_data = gpd.read_file('Onondaga_2021_Tax_Parcels_SHP_2203.zip', dtype=fips, index=False)

# change variable type to ...
raw_parcel_data['PROP_CLASS'] = raw_parcel_data['PROP_CLASS'].astype(float)

# # drop unknown owner data OR say that -999 is unknown owner 
# print(raw_parcel_data['OWNER_TYPE'].value_counts())
# raw_parcel_data['OWNER_TYPE'] = raw_parcel_data['OWNER_TYPE'].replace('-999', np.nan)
# print(raw_parcel_data['OWNER_TYPE'].value_counts())

#%%
#       - Clean raw data - 
#
keep_cols = [
             'COUNTY',      #
             'MUNI_NAME',   #
             'SWIS',        #
             'LAND_AV',     #
             'TOTAL_AV',    #
             'FULL_MV',     #
             'YR_BLT',      #
             "PROP_CLASS",  #
             'MUNI_PCLID',  #
             'geometry',    #
             'OWNER_TYPE',  #
             ]  

#
parcels = raw_parcel_data[keep_cols]

#%%
#       - Identify parcel type -
#
#list of NYS property type classification codes
prop_info = [
             ('aggriculture', 100,199),
             ('residential', 200,299),
             ('vacant', 300,399),
             ('commercial', 400,499),
             ('recreation', 500,599),
             ('community_services', 600,699),
             ('industrial', 700,799),
             ('public_services', 800,899),
             ('parks', 900,999)
            ]

# loop through data to identify parcel type
# assign true/false values + range
parcels_type = parcels.copy()
for info in prop_info:
    (name, start, end) = info 
    parcels_type[name] = parcels_type['PROP_CLASS'].between(start,end)
    
#%%
#       - Identify publicly owned parcels - 
#
# types of public owners
owner_info = [
              ('Federal', 1),
              ('State', 2),
              ('County', 3),
              ('City', 4),
              ('Town', 5),
              ('Village', 6),
              ('Mixed govt', 7)
             ]

# 
# 
owner_type = parcels.copy()
for info in owner_info:
    (owner, typ) = info 
    owner_type[owner] = owner_type['OWNER_TYPE'].isin([str(typ)])
    

print(owner_type.columns)
#
owner_type_tf = owner_type.drop(columns= [
                                          'COUNTY', 'MUNI_NAME', 
                                          'SWIS', 'LAND_AV', 
                                          'TOTAL_AV', 'FULL_MV',
                                          'YR_BLT', 'PROP_CLASS', 
                                          'MUNI_PCLID'
                                         ])
    
#%%
#       - Create geopackage to file results -
#
# set parcel geopackage
out_file = 'oc_parcels.gpkg'

#set projection
utm18n = 26918

#
parcels_type.to_crs(epsg=utm18n)
owner_type.to_crs(parcels_type.crs)

# check if file exists and remove if does
if os.path.exists(out_file):
    os.remove(out_file)

#%%
#       - Save results -
#
# as layers in geopackage

parcels_type.to_file(out_file, layer='parcels_type', index=False)
owner_type_tf.to_file(out_file, layer='owner_type', index=False)

#%%
#
# as csv file
parcels.to_csv('oc_parcels.csv', index=False)














