# Flood Risk and Insurance Gap Mapping

Automated geospatial analysis of insurance coverage gaps using census tract level data.

---

## Research Questions
Which census tracts in Harris County, Texas are the most under insured from flood risk?
How large are the insurance gaps at the tract level?
Whats the corelation between insurance gap and demographics of a census tract?

---

## Data Sources

- National Risk Index (NRI) provided census level data on annual damages from floods 
- National Flood Insurance Program (NFIP) provided insured amount against each flood insurance policy.
- American Community Survey (ACS) 5 year estimates provided census level data on socio-demographic variables.

---

## Methodology & tools 


\[
\mathbb{E}[D \mid F] = \frac{\mathbb{E}[D]}{\mathbb{P}(F)}
\]

- Expected damages was calculated by multipl



The NFIP dataset contained approximately 80 million policy records and could not be processed directly in memory. To handle this scale, the raw data were imported into a relational database using pgAdmin and filtered using Structured Query Language to isolate Harris County records and relevant variables. The resulting subset was then loaded into Python, aggregated to the census tract level, and then merged with ACS and NRI datasets. The merged dataset was saved as a shapefile and  later used as an input in the automated GIS Script. 

---

## Key Capabilities Demonstrated

- Creating and managing large relational databases in pgAdmin
- Querying databases directly from Python using APIs and SQL
- Data wrangling to merge multiple datasets, create indexes, and prepare analysis ready tables
- Reading and applying ArcGIS Pro API documentation to use ArcPy for end to end map and layout automation

---

## Technical Stack

- Python  
- ArcPy  
- ArcGIS Pro  
- pandas and geopandas  
- PostgreSQL and SQL  

---


