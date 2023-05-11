# Planning for Economic Development in Onondaga County
### Alexander Yerou, May 2023
### Maxwell School at Syracuse University

___
## Motivation
Over the next twenty years, Micron Technology plans to spend up to $100 billion building the nation’s largest semiconductor fabrication facility in Clay New York. This historic investment is motivated by New York’s Green CHIPS Program which offers up to $10 billion in economic incentives for environmentally friendly semiconductor manufacturing and supply chain projects. Expansive cross-sector investments in the semiconductor industry are expected to create transformational economic development, job growth, and fiscal mobility in the Central New York Region. However, many residents may be disadvantaged by an increase in the cost of living, property taxes, and inability to avoid gentrification. The goal of this project is to visualize potential patterns of displacement and identify areas in Onondaga County that are the most at risk.  

### This project aims to:
- Identify areas in Onondaga County with high concentrations of low-income households, minority populations, or renters which may be more susceptible to displacement due to rising housing costs.
- Visualize potential patterns of displacement and identify areas in Onondaga County that are the most at risk. 
- Serve as a tool for the administration of the Green CHIPS funding so that Onondaga County delivers on its promise for inclusive growth and economic development.


___

## Instructions
This project uses Python to clean and merge datasets, and QGIS to build maps.

### Python Files:
The following files should be run in order. Output files are saved to the main project folder.

**1.oc_geometry.py:** Uses geospatial data from *'tl_2021_36_tract.zip'* and *'tl_2021_36_bg.zip'*.
Zip files can be found [[Here](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.2021.html#list-tab-790442341)].
Creates a geopackage to join with Onondaga County's economic and demographic data in the remaining files.

**2.oc_parcel_data.py:** Clean and aggregate tax parcel data for Onondaga County. 

**3.oc_census_data.py:** Retrieve demographic data from American Community Survey 5-year data (2021) 
to identify populations in Onondaga County, particularly communities that are 
traditionaly underrepresented in tech. 

**4.figures_and_statistics.py:** Compute socio-economic ratios and summary statistics 
to identify households in Onondaga County that are at the greatest risk of gentrification.

## Input Files
**tl_2021_36_tract.zip:** TIGER/Line Files contain geographic 
entity codes (GEOIDs) that can be linked to the Census Bureau’s demographic data.
This file includes geographic data at the tract level.

**tl_2021_36_bg.zip:** TIGER/Line Files contain geographic 
entity codes (GEOIDs) that can be linked to the Census Bureau’s demographic data.
This file includes geographic data at the block group level.

A projection is systematic transformation of the latitudes and longitudes into 
a plain surface where units are quite commonly represented as meters 
(instead of decimal degrees)

**Onondaga_2021_Tax_Parcels_SHP_2203.zip:**

**https://api.census.gov/data/2021/acs/acs5:**

## Output Files
**oc_geometry.gpkg:**

**oc_tracts.csv:**

**oc_bgs.csv:**

**oc_geo_merged:**

**oc_parcels.gpkg:**

**oc_parcels.csv:**

**oc_pops.csv:**

**findings.png:**

## QGIS
**onondaga_development.qgz:**

## Tableau


















