# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 15:39:59 2023

@author: Yerouap
"""



import geopandas as gpd
import os



#set PROJECTION number (used by NYS agencies)
utm18n = 26918

##OUTPUT file
out_file = 'onondaga_tracts.gpkg'


#                       [Select Census tracts in Onondaga County 2021]
#
#TIGER/Line Files and Shapefiles contain geographic entity codes (GEOIDs) that 
#can be linked to the Census Bureau’s demographic data


# NEED DTYPE:STR!!!!
county = gpd.read_file('tl_2021_36_tract.zip')
oc_tract = county.query('COUNTYFP == "067"')
oc_tract = oc_tract.reset_index()
oc_tract = oc_tract.drop(columns='index')
#convert geo-data (from shapefile) to projection
oc_tract = oc_tract.to_crs(epsg=utm18n)



#                       [Create new geopackage to file results]
#
#check if OUTPUT file exists and remove if does
if os.path.exists(out_file):
    os.remove(out_file)


#                       [Save results in geopackage]
#write layer(s)
oc_tract.to_file(out_file, layer='tracts', index=False)

oc_tract.to_csv('onondaga_tracts.csv', index=False)








#???
#set PROJECTION number (used by NYS agencies)
#utm18n = 26918
#???
##OUTPUT file
#out_file = 'onondaga.gpkg'
#          or
#OCparcels = gpd.read_file('Onondaga_Tax_Parcels_SHP_2203-parcels.gpkg')


#                       Load Onondaga County's Census tracts
#                               and tax parcel data    
#
#
#TIGER/Line Files and Shapefiles contain geographic entity codes (GEOIDs) that 
#can be linked to the Census Bureau’s demographic data
#
#
#read in New York's 2021 Census tract data
#county = gpd.read_file('tl_2021_36_tract.zip', dtype={'GEOID':str})
#select Onondaga County
#oc = county.query('COUNTYFP == "067"')
#oc = oc.reset_index()
#oc = oc.drop(columns='index')
#???
#convert geo-data (from shapefile) to projection
#oc = oc.to_crs(epsg=utm18n)























