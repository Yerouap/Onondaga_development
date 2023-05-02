# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 19:10:24 2023

@author: Yerouap
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

census_data = pd.read_csv('ocpop_by_tract.csv')



pct_poc = (census_data['pop_poc']/census_data['pop_total'])*100
pct_rent = (census_data['housing_rental']/census_data['housing_total'])*100
census_data['pct_poc'] = pct_poc
census_data['pct_rent'] = pct_rent


summedinc = census_data['Median household income'].sum()







# fig1, ax1 = plt.subplots()

# #construct figure
# census_data.plot.scatter('YR_BLT', 'SQFT_LIV', ax=ax1)
# ax1.set_title('Characteristics of Zip Codes')
# fig1.tight_layout()

#################################

# jg2 = sns.jointplot(data=census_data,
#                    y='pct_rent',
#                    x='Median household income',
#                    kind='hex')
# jg2.set_axis_labels('Median household income','pct_rent')
# jg2.fig.suptitle('D')
# jg2.fig.tight_layout()



jg2 = sns.jointplot(data=census_data,
                   y='pct_rent',
                   x='Median household income',
                   kind='hex')
jg2.set_axis_labels('Median household income','pct_rent')
jg2.fig.suptitle('D')
jg2.fig.tight_layout()
















