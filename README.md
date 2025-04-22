# data-wrangling-project
BMI6016
For the California File Data, the GeoJSON is too large to keep in GitHub. Download it from here:

https://gis.data.cnra.ca.gov/datasets/CALFIRE-Forestry::california-fire-perimeters-all/explore?location=36.922813%2C-119.269051%2C6.13

By clicking Download > GeoJSON

Group 2 Final Documentation

Background and Motivation:  
Desertification is the process by which previously fertile land degrades into desert land. The World Health Organization (WHO) has identified multiple sources of desertification that have caused this process to accelerate throughout the 20th and 21st centuries. Desertification has been linked to agricultural and livestock overproduction, urbanization, deforestation, and extreme weather events. Desertification can have massive impacts on human health. The WHO has identified potential challenges to human health, including higher threats of malnutrition, more water- and food-borne diseases, an increase in respiratory diseases, and an increase in the spread of infectious diseases. 


The impacts of desertification will be widespread and affect the global population, so each person has an interest in maintaining a healthy climate. However, some populations may be at an increased risk due to underlying health conditions. Many members of our project group come from a clinical background, meaning that we have worked with and known many people with respiratory diseases, such as asthma or chronic obstructive pulmonary disease (COPD), who are particularly sensitive to the effects of desertification. Our project aimed to examine the effects that desertification has already had on human health to better understand which regions may be at risk and how future health outcomes can be improved. Due to the notable increases in annual temperatures and wildfire activity, in combination with the high population density of the region, we believed that focusing on the coastal western United States would provide valuable insights into these trends.




Project Objectives: 

The primary goal of this project was to develop a database capable of capturing these trends at a more granular level, specifically focusing on the health-related outcomes that are affected by rising temperatures, prolonged drought, and the increasing number of wildfires in the coastal western United States from 2000 to 2020. We sought to understand the trends in conditions more closely associated with these environmental changes, including asthma, COPD, and heat-related illnesses. This was done by gathering monthly data on mortality rates through corresponding ICD codes for each county. The resulting database is structured to facilitate comparisons in these environmental changes with corresponding health outcomes for the respective counties and time periods.


More specifically, this database can be used to help researchers understand trends in desertification in the coastal western US over the last twenty years, by looking at how the frequency and severity of extreme heat events, droughts, and wildfires have changed in this time period. By comparing the frequency and severity of these events to mortality rates associated with asthma, COPD, and heat stroke, we aim to identify regions and populations that are more vulnerable to these climate factors to develop targeted strategies that will support these communities and mitigate these risks.




Data:

To understand these trends, we pulled data on wildfire acreage, temperature and precipitation, and mortality rates. Data was obtained as flat files from publicly available state databases. Datasets were created using consistent temporal and geospatial constraints, with monthly rates from 2000 to 2020 at the county level.


Wildfire data was queried from the Washington State Department of Natural Resources (DNR) Fire Statistics, CalFire California Fire Perimeters, and Oregon Department of Forestry (ODF) Fire Occurrence sites. These sources provided information on the total burned acreage for each wildfire incident. 


Data on regional precipitation and temperatures were pulled from the Oregon State University (OSU) PRISM database. This site gathers weather observations from a wide range of monitoring networks to develop spatial datasets on short- and long-term weather patterns.


Mortality data were queried from the Centers for Disease Control (CDC) Wide-ranging ONline Data for Epidemiologic Research (WONDER) database. This database provides aggregated mortality rates that can be specified using ICD codes. For our project, we filtered data using ICD codes linked with COPD (J44), asthma (J45), and hyperthermia (X30). These data was aggregated by the year, month, state, and county.


Data Processing and Database Design:

Data processing was completed using Python, and the relational database was constructed using SQL. The corresponding scripts and tables can be viewed in our GitHub folders. The following folders contain the datasets and the relevant scripts used to create our relational database.
 
Datasets:

This folder contains each of the raw flat files that were downloaded directly from the databases. 


Wrangling:

This contains the Python scripts used to modify each flat file and create the final CSVs. Datasets from each of the databases were relatively clean, but needed to be modified to fit the desired format of our relational database. 


Temperature and precipitation data were obtained from the OSU PRISM database as yearly raster zip files. Monthly rates were extracted, and the data were mapped from 4-kilometer regions to their corresponding counties. 


Wildfire data for Washington and California was provided in GeoJSON files that were converted to CSVs. Date and geospatial shape data were mapped to their respective counties. Wildfire incidents recorded in the Oregon dataset were recorded at the coordinate-level that were then mapped to the corresponding counties. The geopandas and pygris libraries were used to calculate geospatial intersections and obtain county boundary shapes. 


For each of the datasets, excess columns were removed so that the dataframes only contained information on the year, month, state, county, and variable of interest (e.g., wildfire acreage, precipitation, mortality rates). Data types were converted to a consistent format. 


Lastly, missingness was evaluated, and incomplete rows were removed. For example, the wildfire datasets contained rows with missing information on the corresponding month, which were excluded from the finalized dataset. Additionally, due to the sensitive nature of the data queried from CDC WONDER, only counts that were greater than 10 observations were included.


Finalized datasets were then converted to CSVs, which were then stored in the ‘Cleaned’ folder.


Cleaned:

Using the finalized CSVs as templates, SQL tables were created and stored in our relational database. This structure allows for efficient data retrieval and cross-referencing of environmental conditions with health outcomes, enabling deeper analysis of the effects of climate change on public health.


Three primary SQL tables were created to store the data. The PRISM table includes monthly drought severity indices, average temperatures, heat wave events by county. The Wildfires table stores total monthly county-level wildfire acreage. The Mortality table contains mortality counts for heat-related illness, asthma, and COPD by month and county.


Finally, visualizations were created to analyze the data quality and understand preliminary trends. Missingness was evaluated using heatmap analysis. Descriptive statistics and temporal trends were visualized in a series of bar charts and heatmaps.
