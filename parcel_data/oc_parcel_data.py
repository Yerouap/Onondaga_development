# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 12:41:56 2023

@author: Yerouap
"""


import geopandas as gpd
import pandas as pd

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
             'YR_BLT'       #
             ]

parcel_data = gpd.read_file('Onondaga_2021_Tax_Parcels_SHP_2203.zip', dtype=fips, index=False)
#parcels_data = parcel_data.sample(10)
parcel_data['PROP_CLASS'] = parcel_data['PROP_CLASS'].astype(float)

parcels = parcel_data[keep_cols]




#sub-types*
is_res = parcels['PROP_CLASS'].between(200,299)
res = parcels[is_res]
#sub-types*
is_vacant = parcels['PROP_CLASS'].between(300,399)
vacant = parcels[is_vacant]
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



samp_parcels = parcels.sample(5000)

samp_parcels_byzip = 

















