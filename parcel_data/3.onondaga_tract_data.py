# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 12:41:56 2023

@author: Yerouap
"""


import geopandas as gpd
import pandas as pd



#                       Load Onondaga County's Census tracts
#                               and tax parcel data
#
#
oc_tract = gpd.read_file('onondaga_tracts.gpkg', layer='tracts', dtype={'GEOID':str})
oc_tract = oc_tract.set_index('GEOID')



#                       Load economic development indicators
#
#
#
figrs = pd.read_csv('ocpop_by_bg.csv', dtype={'GEOID':str})
figrs = figrs.set_index('GEOID')


#
#
#
join = oc_tract.merge(figrs, on='GEOID',how='union', indicator=True)










