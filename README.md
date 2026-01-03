# Overview 

This project analyzes insurance coverage gaps across census tracts in Harris County, Texas.

---

## Research Questions

- Which census tracts in Harris County, Texas are the most underinsured with respect to flood risk?
- How large are the insurance gaps at the tract level?
- What is the correlation between insurance gaps and census tract demographics?
  
---

## Data Sources

- National Risk Index (NRI) provided census level estimates of expected annual flood damages  
- National Flood Insurance Program (NFIP) provided policy level insurance coverage amounts  
- American Community Survey (ACS) 5 year estimates provided socio demographic variables at the census tract level  

---

## Methodology 
- Expected loss was calculated as  $\mathbb{E}[L] = \mathbb{P}(F) \times \theta \times V$,  where $\mathbb{E}[L]$ denotes expected loss, $\mathbb{P}(F)$ is the probability of a flood, $\theta$ is the historical damage ratio conditional on flooding, and $V$ is building value.
- Expected losses from riverine flooding and coastal flooding were aggregated.
- Total insurance coverage at the census tract level was calculated by summing coverage amounts across all NFIP policies within each tract.
- Underinsurance was quantified as the difference between estimated damages conditional on flooding and total insured coverage.
- Risk levels were categorized using Jenks natural breaks optimization.

---

## Tools used
- Designed and implemented a relational database schema in **PostgreSQL** to efficiently store and query the NFIP dataset containing over 80 million policy records.
- Used PostgreSQL APIs to execute SQL queries directly from Python.
- Used **Python (pandas and geopandas)** to conduct exploratory analysis, aggregate policy level data, recode variables, handle missing values, remove outliers, and merge datasets.
- Generated choropleth maps in **ArcGIS Pro** to visualize spatial patterns of underinsurance across Harris County.
- Used the **ArcPy API** to automate map generation and layout creation, improving reproducibility.

---


## Limitations and Next Steps

### Risk estimates in the NRI dataset are based on historical data, which may underestimate future losses as climate risks intensify.
- Conduct scenario modeling to simulates increases in flood risk (e.g., 10 percent and 20 percent) and recompute resulting underinsurance gaps.
- Construct alternative risk metrics using forward looking climate projections.

### Publicly available insurance data are limited to NFIP policies and do not capture private flood insurance coverage, leading to underestimation of total coverage.
- Apply machine learning methods such as K nearest neighbors using household level covariates to estimate likely coverage for non NFIP households.
