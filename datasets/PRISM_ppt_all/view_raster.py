import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import pygris
from datetime import datetime

ppt_base_dir = "PRISM_ppt_all"
tmax_base_dir = "PRISM_tmax_all"
output_file = "ca_county_prism_data.csv"

counties = pygris.counties(state="CA", year=2020)


def extract_county_data(county_geometry, raster_path):
    with rasterio.open(raster_path) as src:
        # Create temp GeoDataFrame with proper CRS
        temp_gdf = gpd.GeoDataFrame(geometry=[county_geometry], crs=counties.crs)

        # Convert to raster CRS if needed
        if temp_gdf.crs != src.crs:
            to_crs = src.crs if src.crs is not None else "EPSG:4326"
            temp_gdf = temp_gdf.to_crs(to_crs)

        try:
            # Mask raster with county geometry
            out_image, _ = mask(
                src, [temp_gdf.geometry.values[0]], crop=True, all_touched=True
            )

            # Handle no-data values
            no_data = src.nodata
            valid_data = (
                out_image[out_image != no_data]
                if no_data is not None
                else out_image.flatten()
            )

            if len(valid_data) > 0:
                pixel_area_km2 = 16  # 4km x 4km

                # For precipitation: calculate volume
                if "ppt" in raster_path:
                    return np.sum(valid_data) * pixel_area_km2 * 1e-6  # mm to km³

                # For temperature: take maximum value
                elif "tmax" in raster_path:
                    return np.max(valid_data)
        except Exception as e:
            print(f"Error processing {os.path.basename(raster_path)}: {e}")

        return None


def process_prism_data():
    results = []
    years = range(2000, 2021)

    for idx, county in counties.iterrows():
        county_name = county["NAME"]
        county_fips = county["COUNTYFP"]
        county_geom = county["geometry"]

        print(f"Processing {county_name} County ({idx+1}/{len(counties)})")

        for year in years:
            for month in range(1, 13):
                date_str = f"{year}{month:02d}"

                # Get file paths
                ppt_file = os.path.join(
                    ppt_base_dir,
                    f"PRISM_ppt_stable_4kmM3_{year}_all_bil",
                    f"PRISM_ppt_stable_4kmM3_{date_str}_bil.bil",
                )

                tmax_file = os.path.join(
                    tmax_base_dir,
                    f"PRISM_tmax_stable_4kmM3_{year}_all_bil",
                    f"PRISM_tmax_stable_4kmM3_{date_str}_bil.bil",
                )

                # Process data if files exist
                ppt_total = (
                    extract_county_data(county_geom, ppt_file)
                    if os.path.exists(ppt_file)
                    else None
                )
                tmax_max = (
                    extract_county_data(county_geom, tmax_file)
                    if os.path.exists(tmax_file)
                    else None
                )

                # Store results
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

    # Create DataFrame and save to CSV
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

    return df


if __name__ == "__main__":
    process_prism_data()
