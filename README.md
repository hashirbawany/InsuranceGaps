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
- Expected loss was calculated as $\mathbb{E}[L] = \mathbb{P}(F)\,\theta\,V,$

where $\mathbb{E}[L]$ denotes expected loss, $\mathbb{P}(F)$ is the probability of a flood,
$\theta$ is the historical damage ratio conditional on flooding, and $V$ is the building value.

- Designed a relational database schema in PostgreSQL to efficiently query data from NFIP dataset which contained 80million + observations
- Used postgre sql API to send queries directly from python interface
-
- Grouped policy level dataset at the census level to get an estimate for total assets insured against floods
- Recasted variables, analyzed NA values, removed outliers , coded categorical data, and merged all datasets together
- Generated choropleth maps in ArcGIS to visualize the distribution of underinsured census tracts accross harris county
- Used arcpy API to control map generation process in ArcGIS directly from python and enhance reprodcibailoty
- 
- 
  

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


