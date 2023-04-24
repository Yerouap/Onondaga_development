# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 12:41:56 2023

@author: Yerouap
"""


import geopandas as gpd
import pandas as pd



#                       Load Onondaga County's Census tracts
#                               and tax parcel data

oc = pd.read_csv('onondaga_tracts.csv')
#read in Onondaga County tax parcel data
parcels = gpd.read_file('Onondaga_2021_Tax_Parcels_SHP_2203.zip', dtype={'GEOID':str})
#join parcel data onto tracts
oc_parcels= oc.sjoin(parcels,how='left',predicate='intersects')
oc_parcels.set_index('GEOID')


#parcels_sample = parcels.sample(10)
#oc_sample = oc.sample(10)
#oc_sample = oc_sample.to_crs(epsg=utm18n)
oc_parcels_sample = oc_parcels.sample(10)
print(list(oc_parcels_sample))



#



#                       [Read in dempographic data]
#
pop = pd.read_csv('OCpop_by_bg.csv', dtype={'GEOID':str})
#
pop = pop.set_index('GEOID')
#
pop['pop_poc'] = pop['pop_total'] - pop['pop_white']




#                       [Read in block group shapefile and 
#                           merge on demographic data]
#

#filter to Onondaga County
#
oc_parcels_core = oc_parcels.reset_index()
keep_cols = ['GEOID', 'COUNTYFP', 'geometry']
oc_parcels_core = oc_parcels_core.set_index('GEOID')
oc_parcels_core = oc_parcels[keep_cols]



oc_parcels_core = oc_parcels_core.to_crs(oc.crs)

#
#oc_parcels_core['area'] = oc_parcels['SQ_FT'].area
#
oc_parcels_cpop = oc_parcels_core.merge(pop, on='GEOID', indicator=True)
#
print(oc_parcels_core['_merge'].value_counts())
#oc_parcels_core = oc_parcels_core.drop(columns='_merge')   























