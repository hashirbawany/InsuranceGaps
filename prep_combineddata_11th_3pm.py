#importing Packages & global settings
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely import wkt
import mapclassify

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: f'{x:.6f}')



#loading and merging all files
risk_data = pd.read_csv(
    "risk_data_harris.csv",
    dtype={"TRACTFIPS": str})

insurance_data = insurance_census = pd.read_csv(
    "insurance_census.csv",
    dtype={"censustract": str}
)

acs_data = pd.read_csv("final_acs.csv")

#checking both are unique on census level
assert risk_data['TRACTFIPS'].is_unique, "Column contains duplicate values!"
assert insurance_data['censustract'].is_unique, "Column contains duplicate values!"
assert acs_data['TL_GEO_ID'].is_unique

#merging  files
merged_1 = risk_data.merge(
    insurance_data,
    left_on="TRACTFIPS",
    right_on="censustract",
    how="left"
)

merged_final = merged_1.merge(
    acs_data,
    left_on="TRACTFIPS",
    right_on=acs_data["TL_GEO_ID"].astype(str),
    how="left"
)



#exploratory analysis
#whats the insurance gap
merged_final['insurance_gap'] = merged_final['BUILDVALUE'] - merged_final['totalbuildinginsurancecoverage']

merged_final['insurance_gap'].isna().sum() #9
insurance_risk_combined2 = merged_final.dropna(subset=['insurance_gap']).copy()
insurance_risk_combined2['insurance_gap'].isna().sum()

insurance_risk_combined2['insurance_gap'].describe()
#The negative gaps tells us that building value in NRI risk data is severly underestimaed
# count           1106.000000
# mean      -681284087.542495
# std       1645207200.463038
# min     -12122389936.000000
# 25%       -938444214.250000
# 50%       -127273352.000000
# 75%        168128601.750000
# max       3360385129.000000



# Preparing dataframe for ArcGIS
insurance_risk_combined2['geometry'] = insurance_risk_combined2['geometry'].apply(wkt.loads)

insurance_risk_combined3 = gpd.GeoDataFrame(
    insurance_risk_combined2,
    geometry='geometry'
)

insurance_risk_combined3 = insurance_risk_combined3.set_crs(epsg=3857)
insurance_risk_combined3 = insurance_risk_combined3.to_crs(epsg=4326)

#categorizing
neg_gap = insurance_risk_combined3[insurance_risk_combined3['insurance_gap'] < 0].copy()
pos_gap = insurance_risk_combined3[insurance_risk_combined3['insurance_gap'] > 0].copy()

len(neg_gap) #658
len(pos_gap) #448

jenks = mapclassify.NaturalBreaks(
    pos_gap['insurance_gap'],
    k=3
)

pos_gap['jenks_class'] = jenks.find_bin(pos_gap['insurance_gap'])

neg_gap['jenks_class'] = -1

combined_map = pd.concat([neg_gap, pos_gap], ignore_index=True)
len(combined_map)


combined_map.to_file("harris_underinsurance.shp")

