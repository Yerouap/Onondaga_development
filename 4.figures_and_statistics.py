# -*- coding: utf-8 -*-
"""
Onondaga_development

Compute socio-economic ratios and summary statistics to identify households 
???in Onondaga County that are at the greatest risk of gentrification.
"""
# import modules
import pandas as pd
# module
import matplotlib.pyplot as plt
# module
import seaborn as sns
import geopandas as gpd
import os
#
fips = {
        'STATEFP': str, 
        'COUNTYFP': str, 
        'TRACTCE': str, 
        'GEOID': str
        }


# read in demographic data
pop_data = pd.read_csv('oc_pops.csv', dtype=fips)
pop_data = pop_data.set_index('GEOID')

parcel_data = gpd.read_file('oc_parcels.gpkg')


census_tracts = gpd.read_file('oc_geometry.gpkg', layer='tracts', dtype=fips)
census_tracts = census_tracts.set_index('GEOID')
census_geo = census_tracts.drop(columns=['STATEFP','COUNTYFP','TRACTCE'])


pop_tracts = pd.merge(pop_data, census_tracts, on='GEOID', how='left')
pop_tracts = gpd.GeoDataFrame(pop_tracts, geometry='geometry')




pop_tracts_parcels = gpd.sjoin(parcel_data, pop_tracts, how='left', predicate='intersects')

keep_cols = [
             'LAND_AV', 'TOTAL_AV', 'FULL_MV',
             'YR_BLT', 'PROP_CLASS','OWNER_TYPE','geometry',
             'pop_total', 'pop_white', 'pop_black',
             'pop_hispanic_latino', 'housing_total', 'housing_owned',
             'housing_rental', 'Median household income', 'Total household income',
             'tot pop poverty determined', 'tot pop below pov',
             'tot pop at or above pov', 'Median gross rent',
             'Median owner cost as a percentage of household income',
             'Median value of owner-occupied housing units', 'pop_poc', 'TRACTCE']

pop_parcels = pop_tracts_parcels[keep_cols]

grpd = pd.DataFrame()
grpd = pop_parcels.groupby('TRACTCE')

pct_poverty = pop_parcels.loc('tot pop below pov') / pop_parcels.loc('tot pop poverty detrmined')


# #in inflation-adjusted dollars
# inc_stats_med = pop_data['Median household income'].median()
# inc_stats_tot = pop_data['Total household income'].median()


# #
# #
# pct_poc = (pop_data['pop_poc']/pop_data['pop_total'])*100
# pop_data['pct_poc'] = pct_poc


# #
# #
# pct_rent = (pop_data['housing_rental']/pop_data['housing_total'])*100
# pop_data['pct_rent'] = pct_rent


# #
# #
# summedinc = pop_data['Median household income'].sum()


# #
# #
# # Set the default resolution for plots to 300 DPI
# plt.rcParams['figure.dpi'] = 300

# #
# jg = sns.jointplot(data=pop_data,
#                    y='pct_rent',
#                    x='Median household income',
#                    kind='hex')
# jg.set_axis_labels('Median household income','pct_rent')
# jg.fig.suptitle('D')
# jg.fig.tight_layout()
















