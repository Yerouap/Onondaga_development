# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 15:39:59 2023

@author: Yerouap
"""



import geopandas as gpd
import os
import pandas as pd


#set PROJECTION number (used by NYS agencies)
utm18n = 26918

##OUTPUT file
out_file = 'onondaga_tracts.gpkg'


#                       [Select Census tracts in Onondaga County 2021]

# 
county = gpd.read_file('tl_2021_36_tract.zip')
oc = county.query('COUNTYFP == "067"')
oc = oc.reset_index()
oc = oc.drop(columns='index')
#convert geo-data (from shapefile) to projection
oc = oc.to_crs(epsg=utm18n)



#                       [Create new geopackage to file results]
#check if OUTPUT file exists and remove if does
if os.path.exists(out_file):
    os.remove(out_file)


#                       [Save results in geopackage]
#write layer(s)
oc.to_file(out_file, layer='tracts', index=False)
































