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

# drop unknown owner data OR say that -999 is unknown owner 
print(raw_parcel_data['OWNER_TYPE'].value_counts())
raw_parcel_data['OWNER_TYPE'] = raw_parcel_data['OWNER_TYPE'].replace('-999', np.nan)
print(raw_parcel_data['OWNER_TYPE'].value_counts())

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
    

#%%
#-
#
# city_tracts = gpd.read_file('NYS-Tax-Parcels.gpkg', layer = 'Syracuse_City_Tracts', dtype=fips, index=False)
# city_vacant = int_city_tracts.sjoin(vacant,how='left',predicate='intersects')

#%%
#       - Create geopackage to file results -
#
#set parcel geopackage
# out_file = 'prop_class.gpkg'

# #set projection
# utm18n = 26918
# .to_crs(epsg=utm18n)

# # check if file exists and remove if does
# if os.path.exists(out_file):
#     os.remove(out_file)


# #       - Save results -
# # as layers in geopackage
# .to_file(out_file, layer='vacant', index=False)
# .to_file(out_file, layer='residential', index=False)


#%%


















