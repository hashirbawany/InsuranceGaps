#importing Packages & global settings
import geopandas as gpd
import pandas as pd
from pandas.core.arrays import categorical
import requests
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import Normalize
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import mapclassify as mc
from shapely import wkt
import mapclassify

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: f'{x:.6f}')




#loading  files
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



#analysis
#whats the insurance gap
merged_final['insurance_gap'] = merged_final['BUILDVALUE'] - merged_final['totalbuildinginsurancecoverage']

merged_final['insurance_gap'].isna().sum() #9
insurance_risk_combined2 = merged_final.dropna(subset=['insurance_gap'])
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
neg_gap = insurance_risk_combined3[insurance_risk_combined3['insurance_gap'] < 0]
pos_gap = insurance_risk_combined3[insurance_risk_combined3['insurance_gap'] > 0]

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


color_map = mcolors.ListedColormap([
    "white",       # -1
    "#fed976",     # class 0
    "#fd8d3c",     # class 1
    "#bd0026"      # class 2
])

bounds = [-1, 0, 1, 2, 3]
norm = mcolors.BoundaryNorm(bounds, color_map.N)

c0, c1, c2 = jenks.bins


fig, ax = plt.subplots(figsize=(13, 11))

combined_map.plot(
    column='jenks_class',
    cmap=color_map,
    norm=norm,
    edgecolor='grey',
    linewidth=0.3,
    ax=ax
)

ax.set_title("Underinsurance in Harris County", fontsize=16)
ax.set_axis_off()

legend_items = [
    mpatches.Patch(color="white",  label="None"),
    mpatches.Patch(color="#fed976", label="Low"),
    mpatches.Patch(color="#fd8d3c", label="Medium"),
    mpatches.Patch(color="#bd0026", label="High"),
]

ax.legend(
    handles=legend_items,
    title="Insurance Gap Categories",
    loc="lower left",
    fontsize=11,
    title_fontsize=12
)

plt.figtext(
    0.5, -0.02,
    f"Low: {0} to {c0:,.0f}   •   Medium: {c0:,.0f} to {c1:,.0f}   •   High: > {c1:,.0f}",
    wrap=True, ha="center", fontsize=10
)

# North arrow
ax.annotate(
    'N',
    xy=(0.95, 0.25),      # arrow head (higher)
    xytext=(0.95, 0.15),  # arrow tail (lower)
    arrowprops=dict(facecolor='black', width=4, headwidth=12),
    ha='center',
    va='center',
    fontsize=14,
    xycoords=ax.transAxes
)


# Scale bar
def scale_bar(ax, length, location=(0.1, 0.05), linewidth=3):
    x0, y0 = location
    ax.plot([x0, x0 + length], [y0, y0], transform=ax.transAxes,
            color='black', linewidth=linewidth)
    ax.text(x0 + length / 2, y0 - 0.02,
            f"{int(length * 100)} km",
            transform=ax.transAxes,
            ha='center', va='top', fontsize=10)

scale_bar(ax, length=0.1, location=(0.50, 0.05))

plt.show()



#income overlay
fig, ax = plt.subplots(figsize=(13, 11))

# base map: polygons with Jenks classes
combined_map.plot(
    column='jenks_class',
    cmap=color_map,
    norm=norm,
    edgecolor='grey',
    linewidth=0.3,
    ax=ax
)

# make a copy with centroids as geometry
centroids = combined_map.copy()
centroids["geometry"] = centroids.geometry.centroid

# scale dot sizes by income (tune the *50 and clip if needed)
dot_sizes = (centroids["median_household_income"] / centroids["median_household_income"].max()) * 100
dot_sizes = dot_sizes.fillna(0)

centroids.plot(
    ax=ax,
    markersize=dot_sizes,
    color="black",
    alpha=0.6
)

ax.set_title("Underinsurance in Harris County", fontsize=16)
ax.set_axis_off()

legend_items = [
    mpatches.Patch(color="white",  label="None"),
    mpatches.Patch(color="#fed976", label="Low"),
    mpatches.Patch(color="#fd8d3c", label="Medium"),
    mpatches.Patch(color="#bd0026", label="High"),
]
ax.legend(
    handles=legend_items,
    title="Insurance Gap Categories",
    loc="lower left",
    fontsize=11,
    title_fontsize=12
)

# north arrow
ax.annotate(
    'N',
    xy=(0.95, 0.25),
    xytext=(0.95, 0.15),
    arrowprops=dict(facecolor='black', width=4, headwidth=12),
    ha='center',
    va='center',
    fontsize=14,
    xycoords=ax.transAxes
)

# scale bar
def scale_bar(ax, length, location=(0.75, 0.05), linewidth=3):
    x0, y0 = location
    ax.plot([x0, x0 + length], [y0, y0], transform=ax.transAxes,
            color='black', linewidth=linewidth)
    ax.text(x0 + length / 2, y0 - 0.02,
            "10 km",
            transform=ax.transAxes,
            ha='center', va='top', fontsize=10)

scale_bar(ax, length=0.1)

plt.show()

combined_map.to_file("harris_underinsurance.shp")
