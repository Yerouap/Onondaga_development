# -*- coding: utf-8 -*-
"""
Onondaga_development
 
@author: Yerouap
May 2023
"""
#       - Import modules - 
#
import geopandas as gpd  # to work with geospatial data
import os                # to clear file path for geopackage

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
# filter down to Onondaga County
oc_tracts = census_tracts.query('COUNTYFP == "067"')
oc_tracts = oc_tracts.reset_index()

#%%
#
# clean non-essential data from query
oc_tracts = oc_tracts.drop(columns=[
                                    'index','NAME','NAMELSAD',
                                    'MTFCC','FUNCSTAT','ALAND',
                                    'AWATER','INTPTLAT','INTPTLON',
                                                                   ])

# set projected coordinate system to New York State's standard projection
utm18n = 26918  
# convert projection                            
oc_tracts = oc_tracts.to_crs(epsg=utm18n)   

#%%
#       - Select Census block groups in Onondaga County -
#
# read Census block group data
oc_bgs = gpd.read_file('tl_2021_36_bg.zip', dtype=fips)
#filter down to Onondaga County
oc_bgs = oc_bgs.query('COUNTYFP == "067"')
oc_bgs = oc_bgs.reset_index()

#%%
#
# clean non-essential data from query
oc_bgs = oc_bgs.drop(columns=['index','BLKGRPCE','NAMELSAD',
                              'MTFCC','FUNCSTAT','ALAND',
                              'AWATER','INTPTLAT','INTPTLON'])

#match projection to tracts
oc_bgs = oc_bgs.to_crs(oc_tracts.crs)

#put area in known units: 
oc_bgs['bg_area'] = oc_bgs.area

#%%
#       - Merge tracts and block groups -
#
# spatial join to merge block grop geographic data onto tracts geographic data
#   merge contains any common points
geo_merged = oc_tracts.sjoin(oc_bgs, how='left', predicate='intersects')

# clean merged DataFrame 
geo_merged = geo_merged.drop(['index_right', 'COUNTYFP_right'], axis=1)
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

# as csv file 
oc_tracts.to_csv('oc_tracts.csv', index=False)
oc_bgs.to_csv('oc_bgs.csv', index=False)
geo_merged.to_csv('oc_geo_merged.csv', index=False)



