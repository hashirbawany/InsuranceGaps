#Importing packages
from sqlalchemy import create_engine
import pandas as pd



#Extracting data from database using SQL query 
# engine = create_engine("postgresql://postgres:*****%40*******@localhost:5432/insurancepolicy")

# query = """
# SELECT 
#     policycost,
#     policycount,
#     totalbuildinginsurancecoverage,
#     totalcontentsinsurancecoverage,
#     censustract,
#     countycode
# FROM fema_nfip_policies
# WHERE countycode = '48201'
#   AND "cancellationdateoffloodpolicy" IS NULL;
# """

# #test = pd.read_sql(query, engine)

# insurance_data = test.reset_index(drop=True)    

# insurance_data.to_csv("../data/processed_data/insurance_data.csv", index=False)



# Loading downloaded data and exploring
insurance_data = pd.read_csv(
    "../data/processed_data/insurance_data.csv",
    dtype={"censustract": str}
)


insurance_data.head()

insurance_data.shape #(9216500, 6)

insurance_data.dtypes

insurance_data.isna().sum() #3656 NAs in census tracts


#exploring NAs
mask = insurance_data['censustract'].isna()
insurance_data[~mask].shape #9212844

#since only 3k out of 9million are missing we will drop
insurance_data_cleaned = insurance_data[~mask]



#collapsing to census level
insurance_census = insurance_data_cleaned.groupby(['censustract'])[['totalbuildinginsurancecoverage', 'policycount']].sum()

insurance_census = insurance_census.reset_index()


#exporting to csv
insurance_census.to_csv("../data/processed_data/insurance_census.csv", index=False)


