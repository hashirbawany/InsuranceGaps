# Flood Risk and Insurance Gap Mapping

Automated geospatial analysis of insurance coverage gaps using census tract level data.

---

## Overview

This project automates the creation of publication ready geospatial maps analyzing flood risk and insurance gaps in Harris County, Texas using ArcGIS Pro and Python. The workflow integrates spatial data processing, map symbology, and layout generation into a fully scripted and reproducible GIS pipeline.

---

## Data Sources

- National Risk Index (NRI)  
- National Flood Insurance Program (NFIP) policy level data  
- American Community Survey (ACS) 5 year estimates 

---

## Methods

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


