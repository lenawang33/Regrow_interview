import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import seaborn as sns
import requests as requests
import openpyxl as openpyxl
from statsmodels.stats.multicomp import pairwise_tukeyhsd


ks_qaqc = r"C:\Users\accio\OneDrive\Documents\Code\Regrow\Regrow_interview\Soil1_20231127_LW QAQC.xlsx"
ks_qaqc_df = pd.read_excel(ks_qaqc, sheet_name = "Soil1_20231127_LW Modified")

#selecting a small subset of data for practice analysis
data = ks_qaqc_df[['Sample ID',
                   'Organic C H2O ppm',
                   'Organic Matter LOI %']]

#Dropping samples that are duplicates, since that will put too much emphasis on fields with duplicates
data_drop = data[~data['Sample ID'].str.contains('Dup', na = False)]

data_drop[['Field', 'Sample']] = data_drop['Sample ID'].str.split('_', expand = True)


#Completing Tukey test on Organic C H2O ppm and Organic Matter LOI% as a loop, index columns as numbers
tukey_dfs = []
for i in range(1,3):
    column_name = data_drop.columns[i]
    print(f"{column_name}")
    
    # Perform Tukey's HSD test
    subset = data_drop[['Field', column_name]].dropna()
    tukey_result = pairwise_tukeyhsd(subset[column_name], subset['Field'])
    
    # Convert the result to a DataFrame
    tukey_df = pd.DataFrame(data = tukey_result._results_table.data[1:], 
                            columns = tukey_result._results_table.data[0]
                            )
    
    tukey_df['Variable'] = column_name  # Add a column to identify the variable
    tukey_dfs.append(tukey_df)  # Add the dataframes together from the list
print(tukey_dfs)




#Writing a function that filters through the dataframe with conditions
def filter_tukey_results(tukey_df, alpha = 0.05):
    """
    Filters Tukey's HSD results based on the significance level.
    
    Parameters:
    tukey_df (DataFrame): DataFrame containing Tukey's HSD results.
    alpha (float): Significance level for filtering.
    
    Returns:
    DataFrame: Filtered DataFrame with significant results.
    """
    return tukey_df[tukey_df['reject'] == True]

# Applying the filter function to each Tukey DataFrame
filtered_tukey_dfs = [filter_tukey_results(tukey_df) for tukey_df in tukey_dfs]

# Concatenating the filtered results into a single DataFrame
filtered_tukey_results = pd.concat(filtered_tukey_dfs, ignore_index = True)

# Displaying the filtered results
print(filtered_tukey_results)


#Creating random array, which is better for mathematical and vectorized operations
a = np.array([1, 2, 3, 4, 5])
b = np.array([12, 16, 19, 15, 17])

#Creating a dataframe from the lists
df = pd.DataFrame({'a':a, 'b': b})

def sum(x, y):
    return x + y

test = sum(a, b)



#Creating a random array of 1000 numbers
a = np.random.uniform(-10, 5, 1000)
b = np.random.uniform(-10, 5, 1000)

df1 = pd.DataFrame({'a':a, 'b': b})

#Filtering out negative values, calculate only the sum of the positive values
def sum(df, col1, col2):
    filtered_df = df[(df[col1] >= 0) & (df[col2] >= 0)]
    return filtered_df[col1] + filtered_df[col2]

test = sum(df1, df1.columns[0], df1.columns[1])

#Getting cities list
cities = [
    'Portland, OR', 'Eugene, OR', 'Salem, OR', 'Seattle, WA', 'Spokane, WA', 'Tacoma, WA',
    'San Francisco, CA', 'Los Angeles, CA', 'San Diego, CA', 'Sacramento, CA', 'Fresno, CA',
    'Denver, CO', 'Boulder, CO', 'Fort Collins, CO', 'Chicago, IL', 'Springfield, IL',
    'New York, NY', 'Buffalo, NY', 'Rochester, NY', 'Boston, MA', 'Cambridge, MA',
    'Austin, TX', 'Dallas, TX', 'Houston, TX', 'San Antonio, TX', 'Miami, FL', 'Orlando, FL',
    'Atlanta, GA', 'Savannah, GA', 'Minneapolis, MN', 'St. Paul, MN', 'Phoenix, AZ',
    'Tucson, AZ', 'Philadelphia, PA', 'Pittsburgh, PA', 'Detroit, MI', 'Ann Arbor, MI',
    'Salt Lake City, UT', 'Provo, UT', 'Las Vegas, NV', 'Reno, NV', 'Charlotte, NC',
    'Raleigh, NC', 'Columbus, OH', 'Cleveland, OH', 'Cincinnati, OH'
]
cities_df = pd.DataFrame(cities, columns = ['Cities'])
cities_separate = cities_df['Cities'].str.split(',', expand = True)
cities_separate.columns = ['City', 'State']


#count the number of cities within each state
state_counts = cities_separate['State'].value_counts().reset_index()

state_counts.columns = ['State', 'Count']

#Adding a random comment to see if I can avoid pushing to main branch. 

