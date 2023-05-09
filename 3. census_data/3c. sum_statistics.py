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

#%%
#
# read in demographic data
pop_data = pd.read_csv('ocpop_by_tract.csv')

#%%
#
#in inflation-adjusted dollars
inc_stats_med = pop_data['Median household income'].median()
inc_stats_tot = pop_data['Total household income'].median()

#%%
#
#
pct_poc = (pop_data['pop_poc']/pop_data['pop_total'])*100
pop_data['pct_poc'] = pct_poc

#%%
#
#
pct_rent = (pop_data['housing_rental']/pop_data['housing_total'])*100
pop_data['pct_rent'] = pct_rent

#%%
#
#
summedinc = pop_data['Median household income'].sum()

#%%
#
#
# Set the default resolution for plots to 300 DPI
plt.rcParams['figure.dpi'] = 300

#
jg = sns.jointplot(data=pop_data,
                   y='pct_rent',
                   x='Median household income',
                   kind='hex')
jg.set_axis_labels('Median household income','pct_rent')
jg.fig.suptitle('D')
jg.fig.tight_layout()

#%%














