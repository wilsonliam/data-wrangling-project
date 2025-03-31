import geopandas as gpd
import pandas as pd
import pygris
from datetime import datetime

from shapely.validation import make_valid


wildfire_gdf = gpd.read_file("datasets/California_Fire_Perimeters_(all).geojson")

wildfire_gdf = wildfire_gdf.set_crs(epsg=4326)

wildfire_gdf['date'] = pd.to_datetime(wildfire_gdf['ALARM_DATE'])

wildfire_gdf['geometry'] = wildfire_gdf['geometry'].apply(lambda geom: make_valid(geom) if not geom.is_valid else geom)


wa_counties = pygris.counties(state="CA", year=2022)

wildfire_projected = wildfire_gdf.to_crs(epsg=26910)
counties_projected = wa_counties.to_crs(epsg=26910)

monthly_county_acres = {}

for idx, county in counties_projected.iterrows():
    county_name = county['NAME']
    county_geom = county['geometry']
    
    intersecting_fires = wildfire_projected[wildfire_projected.geometry.intersects(county_geom)]
    
    if not intersecting_fires.empty:
        for _, fire in intersecting_fires.iterrows():
            year = fire['YEAR_']

            if year < 2000 or year > 2019:
                continue

            month = fire['date'].month

            #if pd.isna(month):
            #    continue
                
            fire_geom = fire['geometry']
            fire_acres = fire['GIS_ACRES']
            
            fire_gdf = gpd.GeoDataFrame(geometry=[fire_geom], crs=wildfire_projected.crs)
            county_gdf = gpd.GeoDataFrame(geometry=[county_geom], crs=counties_projected.crs)
            
            invalid = fire_gdf.loc[~fire_gdf.geometry.is_valid]

            intersection = gpd.overlay(fire_gdf, county_gdf, how='intersection')
            
            invalid = intersection.loc[~intersection.geometry.is_valid]
            
            if not intersection.empty:
                intersection_area = intersection.geometry.area.sum()
                original_area = fire_geom.area
                
                if original_area > 0:
                    proportion = intersection_area / original_area
                    key = (county_name, year, month)
                    if key not in monthly_county_acres:
                        monthly_county_acres[key] = 0
                        
                    monthly_county_acres[key] += fire_acres * proportion

results = []
for (county, year, month), acres in monthly_county_acres.items():
    results.append({
        'county': county,
        'year': year,
        'month': month,
        'wildfire_acres': acres
    })

monthly_county_df = pd.DataFrame(results)

monthly_county_df = monthly_county_df.sort_values(['county', 'year', 'month'])

monthly_county_df.to_csv('california_monthly_county_wildfire_acreage.csv', index=False)

