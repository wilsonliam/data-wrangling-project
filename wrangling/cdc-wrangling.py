#import libraries

import pandas as pd
import numpy as np

#import asthma data
file_path = "/Users/andreastofko/Desktop/bmi-data-wrangling/Asthma County Level.txt"
asthma = pd.read_csv(file_path, delimiter='\t')

#view dataframe
print(asthma.head())

#data types
print(asthma.dtypes)

#drop extra columns
asthma1 = asthma.drop(columns=['Notes','Year Code','Month','State Code'])
print(asthma1.head())
print(asthma1.dtypes)

#convert month code to month
asthma1['Month'] = pd.to_datetime(asthma1['Month Code'], format= '%Y/%m').dt.month

#final table
asthma2 = asthma1[['State', 'County','County Code','Year', 'Month', 'Deaths', 'Population','Crude Rate']]
asthma2 = asthma2.sort_values(['County', 'Year', 'Month'])

asthma2.to_csv('cdc-asthma-related-deaths.csv', index=False)


#import COPD data
file_path2 = "/Users/andreastofko/Desktop/bmi-data-wrangling/COPD County Level.txt"
copd = pd.read_csv(file_path2, delimiter='\t')

#drop extra columns
copd1 = copd.drop(columns=['Notes','Year Code','Month','State Code'])

#convert month code to month
copd1['Month'] = pd.to_datetime(copd1['Month Code'], format= '%Y/%m').dt.month

#final table
copd2 = copd1[['State', 'County','County Code','Year', 'Month', 'Deaths', 'Population','Crude Rate']]
copd2 = copd2.sort_values(['County', 'Year', 'Month'])
copd2.to_csv('cdc-copd-related-deaths.csv', index=False)


#import hyperthermia data
file_path3 = "/Users/andreastofko/Desktop/bmi-data-wrangling/Hyperthermia County Level.txt"
hyperthermia = pd.read_csv(file_path3, delimiter='\t')

#drop extra columns (dropping population/crude rate because these are all suppressed/NA values)
hyperthermia1 = hyperthermia.drop(columns=['Notes','Year Code','Month','State Code'])

#convert month code to month
hyperthermia1['Month'] = pd.to_datetime(hyperthermia1['Month Code'], format= '%Y/%m').dt.month

#final table
hyperthermia2 = hyperthermia1[['State', 'County','County Code','Year', 'Month', 'Deaths', 'Population','Crude Rate']]
hyperthermia2 = hyperthermia2.sort_values(['County', 'Year', 'Month'])
hyperthermia2.to_csv('cdc-hyperthermia-related-deaths.csv', index=False)





