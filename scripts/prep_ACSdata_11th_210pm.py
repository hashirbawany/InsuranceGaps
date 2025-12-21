#importing Packages & global settings
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: f'{x:.6f}')



#Importing  all ACS variants
acs4  = pd.read_csv("../data/rawdata/acs/nhgis0004_ds267_20235_tract.csv")
acs5  = pd.read_csv("../data/rawdata/acs/nhgis0005_ds267_20235_tract.csv")
acs6  = pd.read_csv("../data/rawdata/acs/nhgis0006_ds267_20235_tract.csv")
acs7  = pd.read_csv("../data/rawdata/acs/nhgis0007_ds267_20235_tract.csv")
acs8  = pd.read_csv("../data/rawdata/acs/nhgis0008_ds267_20235_tract.csv")
acs10 = pd.read_csv("../data/rawdata/acs/nhgis0010_ds267_20235_tract.csv")
acs11 = pd.read_csv("../data/rawdata/acs/nhgis0011_ds267_20235_tract.csv")




#cleaning each one by one
#acs 4
acs4_clean = acs4[[
    "TL_GEO_ID",
    "ASN1E001"
]].copy()

acs4_clean = acs4_clean.rename(columns={
    "ASN1E001": "total_population"
})


#acs5
acs5_clean = acs5[[
    "TL_GEO_ID",
    "ASN2E001",
    "ASN2E002",
    "ASN2E003",
    "ASN2E004",
    "ASN2E005",
    "ASN2E006",
    "ASN2E007",
    "ASN2E008",
    "ASN2E009",
    "ASN2E010"
]].copy()

acs5_clean = acs5_clean.rename(columns={
    "ASN2E001": "race_total",
    "ASN2E002": "white_alone",
    "ASN2E003": "black_alone",
    "ASN2E004": "american_indian_alaska_native",
    "ASN2E005": "asian_alone",
    "ASN2E006": "native_hawaiian_pacific_islander",
    "ASN2E007": "some_other_race",
    "ASN2E008": "two_or_more_races",
    "ASN2E009": "two_races_including_other",
    "ASN2E010": "two_races_excluding_other_three_plus"
})


#acs6
acs6_clean = acs6[[
    "TL_GEO_ID",
    "ASS7E001"
]].copy()

acs6_clean = acs6_clean.rename(columns={
    "ASS7E001": "total_housing_units"
})


#ac8
acs8_clean = acs8[[
    "TL_GEO_ID",
    "ASQPE001"
]].copy()

acs8_clean = acs8_clean.rename(columns={
    "ASQPE001": "median_household_income"
})


#acs10
acs10_clean = acs10[[
    "TL_GEO_ID",
    "ASQLE001"
]].copy()

acs10_clean = acs10_clean.rename(columns={
    "ASQLE001": "total_poverty_status_hh"
})

#acs11
acs11_clean = acs11[[
    "TL_GEO_ID",
    "ASS9E001",
    "ASS9E002",
    "ASS9E003"
]].copy()

acs11_clean = acs11_clean.rename(columns={
    "ASS9E001": "total_housing_units_acs11",
    "ASS9E002": "owner_occupied",
    "ASS9E003": "renter_occupied"
})


#merging
final_acs = (
    acs4_clean
    .merge(acs5_clean, on="TL_GEO_ID", how="left")
    .merge(acs6_clean, on="TL_GEO_ID", how="left")
    .merge(acs8_clean, on="TL_GEO_ID", how="left")
    .merge(acs10_clean, on="TL_GEO_ID", how="left")
    .merge(acs11_clean, on="TL_GEO_ID", how="left")
)



#saving data
final_acs.to_csv("../data/processed_data/final_acs.csv", index=False)

