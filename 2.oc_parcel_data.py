# -*- coding: utf-8 -*-
"""
Onondaga_development
 
colaborators: Pete Wilcoxen
@author: Yerouap
May 2023
"""
#       - Import modules -
#
# to work with geospatial data 
import geopandas as gpd
# to work with numeric data
import numpy as np
# to clear file path for geopackage 
import os

#%%
#       - Load Onondaga County tax parcel data -
#
# set dictionary to define variable type
fips = {
        'STATEFP': str,     
        'COUNTYFP': str,    
        'TRACTCE': str,     
        'GEOID': str,       
       }
       
# read tax parcel data
raw_parcel_data = gpd.read_file('Onondaga_2021_Tax_Parcels_SHP_2203.zip', dtype=fips, index=False)

#%%
#       - Clean raw data -
#
# change variable type to sort by numeric classification code
raw_parcel_data['PROP_CLASS'] = raw_parcel_data['PROP_CLASS'].astype(float)

# identify parcels with unknown owner 
#original parcel count 
print(raw_parcel_data['OWNER_TYPE'].value_counts())
print(raw_parcel_data['OWNER_TYPE'].value_counts().sum())
# replace unknown values 
raw_parcel_data['OWNER_TYPE'] = raw_parcel_data['OWNER_TYPE'].replace('-999', np.nan)
# parcel count after
print(raw_parcel_data['OWNER_TYPE'].value_counts())
print(raw_parcel_data['OWNER_TYPE'].value_counts().sum())

#%%
#        
# set list of select tax parcel variables
keep_cols = [
             'COUNTY',      #
             'MUNI_NAME',   # variables needed to evaluate the economic and
             'SWIS',        # demographic characteristics of Onondaga County 
             'LAND_AV',     # in script 4.figures_and_statistics. 
             'TOTAL_AV',    #
             'FULL_MV',     # Columns excluded from list do not contain data that 
             'YR_BLT',      # pertinant data to inform economic development.
             "PROP_CLASS",  #
             'MUNI_PCLID',  #
             'geometry',    #
             'OWNER_TYPE',  #
             ]  

# create DataFrame of selected variables 
parcels = raw_parcel_data[keep_cols]

#%%
#       - Identify parcel type -
#
# list of NYS property type classification codes
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

# loop through parcels to identify parcel type
#   assign true/false values for each classification range
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

# loop through parcels to identify owner type
#   assign true/false values for each type of owner
owner_type = parcels.copy()
for info in owner_info:
    (owner, typ) = info 
    owner_type[owner] = owner_type['OWNER_TYPE'].isin([str(typ)])
#
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

# set projected coordinate system to NYS standard projection
utm18n = 26918
# convert projection 
parcels_type.to_crs(epsg=utm18n)
# match projection to parcels
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

# as csv file
parcels.to_csv('oc_parcels.csv', index=False)



