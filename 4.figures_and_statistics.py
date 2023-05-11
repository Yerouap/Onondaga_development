# -*- coding: utf-8 -*-
"""
Onondaga_development

@author: Yerouap
May 2023
"""
#       - Import Modules -
#
 
import pandas as pd              # to manipulate and structure data
import matplotlib.pyplot as plt  # to make statistical graphs
import seaborn as sns            # to make more sophisticated statistical graphs
import geopandas as gpd          # to work with geospatial data
import numpy as np               # to work with numeric data
import os                        # to clear file path for geopackage

#%%
#       - Load some output files -
#
# read in parcel data
parcel_data = gpd.read_file('oc_parcels.gpkg')

# read in census data
pop_data = pd.read_csv('oc_pops.csv', dtype={'GEOID':str})
pop_data = pop_data.set_index('GEOID')

# read in Onondaga County's tract geospatial data
census_tracts = gpd.read_file('oc_geometry.gpkg', layer='tracts', dtype={'GEOID':str})
census_tracts = census_tracts.set_index('GEOID')

#%%
#
#
# merge geospatial data onto census data
pop_tracts = pd.merge(pop_data, census_tracts, on='GEOID', how='left')
pop_tracts = gpd.GeoDataFrame(pop_tracts, geometry='geometry')

#set projection
utm18n = 26918
pop_tracts = pop_tracts.to_crs(epsg=utm18n)

out_file = 'oc_pop_tracts.gpkg'

# check if file exists and remove if does
if os.path.exists(out_file):
    os.remove(out_file)

# as layers in geopackage
pop_tracts.to_file(out_file, layer='pop_tracts', index=False)

# as csv
pop_tracts.to_csv('oc_pop_tracts.csv', index=True)

#%%
#
#
# merge any of the data in the geometry of these dataframes
pop_tracts_parcels = gpd.sjoin(pop_tracts, parcel_data, how='left', predicate='intersects')

keep_cols = [
             'LAND_AV','TOTAL_AV', 
             'FULL_MV','YR_BLT', 
             'PROP_CLASS','OWNER_TYPE',
             'geometry','pop_total', 
             'pop_white','pop_poc',
             'housing_total', 
             'housing_owned','housing_rental', 
             'med_hh_income','tot_hh_income',
             'tot_pop_measured_poverty','tot_pop_below_poverty',
             'tot_pop >= poverty','med_gross_rent',
             'med_owner_cost%','med_value_owner-occupied_housing_units'
                                                                       ]
#clean
pop_parcels = pop_tracts_parcels[keep_cols]

# group by tract 
grpd = pop_parcels.groupby(['GEOID']).agg({
                                           'LAND_AV':np.sum,'TOTAL_AV':np.sum,
                                           'pop_total':np.sum,'pop_white':np.sum,
                                           'FULL_MV':np.sum, 'pop_poc':np.sum,
                                           'housing_total':np.sum,'housing_rental':np.sum,
                                           'FULL_MV':np.sum,'med_hh_income':np.sum,
                                           'tot_pop_measured_poverty':np.sum,'tot_pop_below_poverty':np.sum,
                                           'med_gross_rent':np.sum,'med_value_owner-occupied_housing_units':np.sum
                                                                                                                    })

#%%
#       - compute some figures and statistics at census tract level - 
#
#
stats = pd.DataFrame()

#
pct_poc = round(100*(grpd['pop_poc'] / grpd['pop_total']),2)
print('\nPercent population that is people of color:', pct_poc)

#
pct_rental = round(100*(grpd['housing_rental'] / grpd['housing_total']),2)
print('\nPercent rental housing units:', pct_rental)

#
med_inc = grpd['med_hh_income'].sort_values()
med_inc = med_inc.sort_values()[3:]

#
pct_bel_pov = round(100*(grpd['tot_pop_below_poverty'] / grpd['tot_pop_measured_poverty']),2)

#
stats['pct_poc'] = pct_poc.astype(int)
stats['pct_rental'] = pct_rental.astype(int)
stats['med_inc'] = med_inc.astype(int)
stats['pct_bel_pov'] = pct_bel_pov.astype(int)
      
      
# .query('vacant == True')
#%%
#       - Make some graphs -
#
# Set the default resolution for plots to 300 DPI
plt.rcParams['figure.dpi'] = 300

#jointplot
jg = sns.jointplot(data=stats,
                    y='pct_rental',
                    x='med_inc',
                    kind='hex')
jg.set_axis_labels('Median household income','pct_rental')
jg.fig.suptitle('D')
jg.fig.tight_layout()


# 4-dimensional plot
fg = sns.relplot(data=stats,
                  x='med_inc',
                  y='pct_rental',
                  hue='pct_bel_pov',
                  size='pct_poc',
                  #sizes=(10,200),
                  facet_kws={'despine': False,
                            'subplot_kws':
                            {'title': 'Characteristics by tracts'}})
fg.set_axis_labels('med_inc', 'Percent Rental')
fg.refline(x=med_inc, y=pct_rental)
fg.tight_layout()




