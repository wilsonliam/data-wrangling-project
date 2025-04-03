import pandas as pd

odf = pd.read_csv("datasets/ODF_Fire_Occurrence_Data_2000-2022_20250212.csv")

# i think reportdatetime has fewer missing values (eyeballing it) than ign or others
odf['ReportDateTime'] = pd.to_datetime(odf['ReportDateTime'], format='%m/%d/%Y %I:%M:%S %p')

odf['Year'] = odf['ReportDateTime'].dt.year
odf['Month'] = odf['ReportDateTime'].dt.month

monthly_acreage = odf.groupby(['County','Year','Month'], as_index=False) ['EstTotalAcres'].sum()

monthly_acreage.to_csv('oregon_monthly_county_wildfire_acreage.csv', index=False)
