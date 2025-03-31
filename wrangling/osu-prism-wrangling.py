import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import pygris
from datetime import datetime


counties = pygris.counties(state=['WA','OR','CA'], year=2022)

def extract_county_data(county_geometry, raster_path):
    src = rasterio.open(raster_path)
    temp_gdf = gpd.GeoDataFrame(geometry=[county_geometry], crs=counties.crs)

    to_crs = src.crs if src.crs is not None else "EPSG:4326"
    temp_gdf = temp_gdf.to_crs(to_crs)

    out_image, _ = mask(src, [temp_gdf.geometry.values[0]], crop=True, all_touched=True)

    no_data = src.nodata
    valid_data = (out_image[out_image != no_data] if no_data is not None else out_image.flatten())

    if len(valid_data) > 0:
        pixel_area_km2 = 16  # 4km x 4km gridds

        if "ppt" in raster_path:
            return np.sum(valid_data) * pixel_area_km2 * 1e-6  # mm to km3

        elif "tmax" in raster_path:
            return np.max(valid_data)


results = []
years = range(2000, 2021)

for idx, county in counties.iterrows():
    county_name = county["NAME"]
    county_fips = county["COUNTYFP"]
    county_geom = county["geometry"]

    print(f"{county_name}")

    for year in years:
        for month in range(1, 13):
            date_str = f"{year}{month:02d}"

            ppt_file = f'datasets/PRISM_ppt_all/PRISM_ppt_stable_4kmM3_{year}_all_bil/PRISM_ppt_stable_4kmM3_{date_str}_bil.bil'
            tmax_file = f'datasets/PRISM_tmax_all/PRISM_tmax_stable_4kmM3_{year}_all_bil/PRISM_tmax_stable_4kmM3_{date_str}_bil.bil'

            ppt_total = (extract_county_data(county_geom, ppt_file))
            tmax_max = (extract_county_data(county_geom, tmax_file))

            results.append(
                {
                    "county_name": county_name,
                    "county_fips": county_fips,
                    "year": year,
                    "month": month,
                    "date": datetime(year, month, 1),
                    "precipitation_total_km3": ppt_total,
                    "max_temperature_c": tmax_max,
                }
            )

df = pd.DataFrame(results)
df.to_csv("all_county_prism_data.csv", index=False)

