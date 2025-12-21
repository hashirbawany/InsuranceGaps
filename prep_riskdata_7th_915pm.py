#importing Packages & global settings
import geopandas as gpd
import pandas as pd
import numpy as np


pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: f'{x:.6f}')



#Loading & cleaning
risk = gpd.read_file(r"C:\Users\hashi\OneDrive - Higher Education Commission\Desktop\Uchicago Classes\Quarter 4\GIS\Final Project\NRI_Shapefile_CensusTracts\NRI_Shapefile_CensusTracts.shp")

keep_cols = [
    "TRACTFIPS", "COUNTYFIPS", "STATEFIPS", "NRI_ID",
    "RFLD_RISKV", "RFLD_RISKS", "RFLD_RISKR", "RFLD_EALB", "RFLD_AFREQ" , "RFLD_EXPB" , "RFLD_HLRB",
    "CFLD_RISKV", "CFLD_RISKS", "CFLD_RISKR", "CFLD_EALB", "CFLD_EXPB" , "CFLD_HLRB",
    "BUILDVALUE", "POPULATION",
    "RISK_SCORE", "EAL_SCORE",
    "SOVI_SCORE", "RESL_SCORE",
    "Shape_Area", "Shape_Leng",
    "geometry", "STATE",
    "STCOFIPS" , "COUNTY"

]

risk_flood = risk.loc[:,keep_cols]



#Encoding categories for  CFLD_RISKR & RFLD_RISKR variable
rating_to_code_map = {
    "Relatively Low": 2,
    "No Rating": 0,
    "Relatively Moderate": 3,
    "Very Low": 1,
    "Relatively High": 4,
    "Very High": 5,
    "Insufficient Data": 99,
    "Not Applicable" : 98
}

risk_flood['RFLD_RISKR_codes'] = risk_flood['RFLD_RISKR'].map(rating_to_code_map)
risk_flood['CFLD_RISKR_codes'] = risk_flood['CFLD_RISKR'].map(rating_to_code_map)

risk_flood_1 = risk_flood.copy()



# replacing 99,0,98 as 0 
risk_flood_1['RFLD_EALB']=np.where(
    risk_flood_1['RFLD_RISKR_codes'].isin([0,99,98]),
    0,
    risk_flood_1['RFLD_EALB']
)

risk_flood_1['CFLD_EALB']=np.where(
    risk_flood_1['CFLD_RISKR_codes'].isin([0,99,98]),
    0,
    risk_flood_1['CFLD_EALB']
)



#creating cumulative EL
risk_flood_1.loc[:,'cumulative_EL'] = risk_flood_1['RFLD_EALB'] + risk_flood_1['CFLD_EALB']



#keeping only harris county
risk_flood_1_harris = risk_flood_1.loc[risk_flood_1['STCOFIPS'] == '48201'].copy()

risk_flood_1_harris.shape #1115
risk_flood_1_harris['TRACTFIPS'].is_unique #unique at census level
risk_flood_1_harris['TRACTFIPS'].dtypes



#Creating a variable for conditional expected loss if flood occurs
risk_flood_1_harris['RFLD_EALB'].isna().sum() #0
risk_flood_1_harris['RFLD_HLRB'].isna().sum() #0
risk_flood_1_harris['CFLD_EALB'].isna().sum() #0
risk_flood_1_harris['CFLD_HLRB'].isna().sum() #0

risk_flood_1_harris['rlfd_loss'] = risk_flood_1_harris['RFLD_EXPB'] * risk_flood_1_harris['RFLD_HLRB']
risk_flood_1_harris['clfd_loss'] = risk_flood_1_harris['CFLD_EXPB'] * risk_flood_1_harris['CFLD_HLRB']

risk_flood_1_harris['total_loss'] = risk_flood_1_harris['rlfd_loss'] + risk_flood_1_harris['clfd_loss']

risk_flood_1_harris[['RFLD_EXPB' , 'RFLD_HLRB' , 'rlfd_loss' , 'RFLD_EALB' , 'RFLD_AFREQ' ]]
risk_flood_1_harris[['CFLD_EXPB' , 'CFLD_HLRB' , 'clfd_loss' , 'CFLD_EALB'  ]]



#is total loss higher than cumulative_EL
risk_flood_1_harris['total_loss_higher'] = np.where(
risk_flood_1_harris['total_loss'] > risk_flood_1_harris['cumulative_EL'],
1,
0
)

len(risk_flood_1_harris) #1115
sum(risk_flood_1_harris['total_loss_higher'])



#Exporting
risk_flood_1_harris.to_csv("risk_data_harris.csv", index=False)
risk_flood_1.to_csv("risk_data_full.csv", index=False)
