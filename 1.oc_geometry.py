# -*- coding: utf-8 -*-
"""
Onondaga_development

Create a geopackage that contains geospatial data for Onondaga County's 
Census tracts and block groups.

@author: Yerouap
"""
#
# TIGER/Line Files and Shapefiles contain geographic entity codes (GEOIDs) 
# that can be linked to the Census Bureau’s demographic data.
#

#%%
#       - Import modules - 
#
# to read geospatial data 
import geopandas as gpd
# to clear geopackage's file path
import os

#%%
#       - Select Census tracts in Onondaga County - 
#
# set dictionary to define variable type 
fips = {
        'STATEFP': str, 
        'COUNTYFP': str, 
        'TRACTCE': str, 
        'GEOID': str
        }

# read Census tract data
census_tracts = gpd.read_file('tl_2021_36_tract.zip', dtype=fips)

# filter tract data for Onondaga County and clean query
oc_tracts = census_tracts.query('COUNTYFP == "067"')
oc_tracts = oc_tracts.reset_index()
oc_tracts = oc_tracts.drop(columns=['index','NAME','NAMELSAD',
                                  'MTFCC','FUNCSTAT','ALAND',
                                  'AWATER','INTPTLAT','INTPTLON'])

# set projection and convert to NYS standard
utm18n = 26918
oc_tracts = oc_tracts.to_crs(epsg=utm18n)

# print(oc_tract.columns)

#%%
#       - Import Census block groups -
#
#read Census block group data
oc_bgs = gpd.read_file('tl_2021_36_bg.zip')

#filter for Onondaga County
oc_bgs = oc_bgs.query('COUNTYFP == "067"')
oc_bgs = oc_bgs.reset_index()
oc_bgs = oc_bgs.drop(columns=['index','BLKGRPCE','NAMELSAD',
                              'MTFCC','FUNCSTAT','ALAND',
                              'AWATER','INTPTLAT','INTPTLON'])

#match projection to NYS standard
oc_bgs = oc_bgs.to_crs(oc_tracts.crs)

#put area in known units: 
oc_bgs['bg_area'] = oc_bgs.area

#%%
#       - Merge tracts and block groups -
#
#
geo_merged = oc_tracts.sjoin(oc_bgs, how='left', predicate='intersects')

#
geo_merged = geo_merged.drop(['index_right', 'COUNTYFP_right'], axis=1)

#
geo_merged = geo_merged.reset_index(drop=True)

#%%
#       - Create geopackage to file results -
#
# set output file
out_file = 'oc_geometry.gpkg'

# check if file exists and remove if does
if os.path.exists(out_file):
    os.remove(out_file)

#%%
#       - Save results -
#
# as layer in geopackage
oc_tracts.to_file(out_file, layer='tracts', index=False)
oc_bgs.to_file(out_file, layer='bgs', index=False)
geo_merged.to_file(out_file, layer='geo_merged', index=False)


# as csv
oc_tracts.to_csv('oc_tracts.csv', index=False)
oc_bgs.to_csv('oc_bgs.csv', index=False)
geo_merged.to_csv('oc_geo_merged.csv', index=False)






