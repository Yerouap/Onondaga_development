# -*- coding: utf-8 -*-
"""
Onondaga_development

Create a geopackage that contains the geospatial data for Onondaga County's 
Census tracts and block groups.
"""

#   to read geospatial data 
import geopandas as gpd
#   to clear the geopackage's file path
import os

#%%

# set file for geospatial data

out_file = 'onondaga_tracts.gpkg'

#%%

#       Select Census tracts in Onondaga County 

#  TIGER/Line Files and Shapefiles contain geographic entity codes (GEOIDs) that 
#can be linked to the Census Bureau’s demographic data

#

fips = {
        'STATEFP': str, 
        'COUNTYFP': str, 
        'TRACTCE': str, 
        'GEOID': str
        }

county = gpd.read_file('tl_2021_36_tract.zip', dtype=fips)
oc_tract = county.query('COUNTYFP == "067"')
oc_tract = oc_tract.reset_index()
oc_tract = oc_tract.drop(columns=['index',
                                  'NAME',
                                  'NAMELSAD',
                                  'MTFCC',
                                  'FUNCSTAT'])



#set PROJECTION number (used by NYS agencies)
utm18n = 26918
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





#                       Import Census block groups
#
oc_bgs = gpd.read_file('tl_2021_36_bg.zip')

#Onondaga County
oc_bgs = oc_bgs.query('COUNTYFP == "067"')
#match projection to geopackage
oc_bgs = oc_bgs.to_crs(oc_tract.crs)
#put area in known units
oc_bgs['bg_area'] = oc_bgs.area

#
oc_bgs.to_file(out_file, layer='bgs', index=False)



#                       Merge tracts and block groups
#
geo_merged = oc_tract.sjoin(oc_bgs, how='left',predicate='intersects')
geo_merged2 = oc_tract.sjoin(oc_bgs, how='left',predicate='contains')
geo_merged = geo_merged.drop(['index_right'], axis=1)
geo_merged = geo_merged.reset_index(drop=True)
geo_merged.to_file(out_file, layer='geo_merged', index=False)
geo_merged2.to_file(out_file, layer='geo_merged2', index=False)












