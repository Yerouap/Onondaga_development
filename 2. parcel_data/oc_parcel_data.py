# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 12:41:56 2023

@author: Yerouap
shoutout - Professor Wilcixen --> for loop
"""


#samp_parcels = parcels.sample(5000)
#samp_parcels_byzip = 


import geopandas as gpd
import pandas as pd
import os
import numpy as np

out_file = 'prop_class.gpkg'
out_file2 = 'prop_class2.gpkg'



fips = {
        'STATEFP': str,     #
        'COUNTYFP': str,    #
        'TRACTCE': str,     #
        'GEOID': str,       #
        }
#use_type = {'PROP_CLASS': str}



#                       Load parcel data
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
             'YR_BLT',      #
             'OWNER_TYPE']  #

parcel_data = gpd.read_file('Onondaga_2021_Tax_Parcels_SHP_2203.zip', dtype=fips, index=False)
#parcels_data = parcel_data.sample(10)
parcel_data['PROP_CLASS'] = parcel_data['PROP_CLASS'].astype(float)

parcels = parcel_data[keep_cols]



parcels ['pub_own'] = parcels['OWNER_TYPE'].astype(float)
parcels['pub_own'] = parcels ['pub_own'].where(parcels['pub_own']<=8, np.nan)

parcels['pub_own'] = parcels['pub_own'].replace('-999', np.nan)
#samp_parcels = parcels.sample(5000)

#print(samp_parcels.columns)
#samp_parcels['OWNER_TYPE'] = samp_parcels['OWNER_TYPE'].astype(float)

#samp_parcels_pubown = samp_parcels['OWNER_TYPE'].where(samp_parcels['OWNER_TYPE']<=7, np.nan)

city_tracts = gpd.read_file('NYS-Tax-Parcels.gpkg', layer = 'Syracuse_City_Tracts', dtype=fips, index=False)


# property_class = pd.DataFrame()

# def byclass(parcels):
#     property_class = pd.DataFrame()
#     for type_ in parcels:
#         type_ = type_.between()
#         property_class.append( int(type_) )
#     return property_class


prop_info = [
             ('residential', 200,299),
             ('vacant', 300,399),
             ]
parcels = parcels.copy()
for info in prop_info:
    (name, start, end) = info 
    parcels[name] = parcels['PROP_CLASS'].between(start,end)
    

#                       Property type to geopackage

# #prop_layers = prop_info[parcels]
# prop_layers = parcels[prop_info]
# for key in prop_layers:
#     ( )
#     prop_layers = prop_layers.astype(int)
#     name.to_file(out_file2, layer ='name', index=False)
    


#sub-types*
is_res = parcels['PROP_CLASS'].between(200,299)
res = parcels[is_res]
res = res.drop(columns='YR_BLT')
#sub-types*
is_vacant = parcels['PROP_CLASS'].between(300,399)
vacant = parcels[is_vacant]
vacant = vacant.drop(columns='YR_BLT')

#sub-types*
is_commercial = parcels['PROP_CLASS'].between(400,499)
commercial = parcels[is_res]

is_parksnrec = parcels['PROP_CLASS'].between(500,599)
parksnrec = parcels[is_parksnrec]

is_community_svcs = parcels['PROP_CLASS'].between(600,699)
community_svcs = parcels[is_community_svcs]

is_industrial = parcels['PROP_CLASS'].between(700,799)
industrial = parcels[is_industrial]

is_pub_svcs = parcels['PROP_CLASS'].between(800,899)
pub_svcs = parcels[is_pub_svcs]

is_pub_pks = parcels['PROP_CLASS'].between(900,999)
pub_pks = parcels[is_pub_pks]




#
#check if OUTPUT file exists and remove if does
if os.path.exists(out_file):
    os.remove(out_file)


vacant.to_file(out_file, layer='vacant', index=False)
res.to_file(out_file, layer='residential', index=False)




int_city_tracts = gpd.read_file('NYS-Tax-Parcels.gpkg', layer = 'Syracuse_City_Tracts', dtype=fips, index=False)

#set PROJECTION number (used by NYS agencies)
utm18n = 26918
#convert geo-data (from shapefile) to projection
int_city_tracts = int_city_tracts.to_crs(epsg=utm18n)



city_vacant = int_city_tracts.sjoin(vacant,how='left',predicate='intersects')

fullmv = city_vacant.copy()
print(fullmv['FULL_MV'].sum())


















