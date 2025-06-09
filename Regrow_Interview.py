import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import seaborn as sns
import requests as requests


####### QAQC Analysis Sample##########
#Reading in the Kansas data
ks_qaqc = "https://raw.githubusercontent.com/lenawang33/Regrow_interview/main/Kansas_Duplicates.csv"
ks_qaqc_df = pd.read_csv(ks_qaqc)


# Calculating variance for each field, excluding the first 10 columns (including only numeric)
variance = ks_qaqc_df.groupby('Field').var(numeric_only = True)

# Calculating sum of variances
sum_variance = variance.iloc[:, 10:].sum()

#Calculating sample precision
sample_precision = 3 / sum_variance # 3 is the number of degrees of freedom for the sample variance

#Calculating coefficient of variance
mean_values = ks_qaqc_df.mean(numeric_only  = True)
std_values = ks_qaqc_df.std(numeric_only = True)
coefficient_of_variation = std_values / mean_values
print(coefficient_of_variation)

#Combining coefficient of variation with sample precision
vari_prec = pd.concat([sample_precision, coefficient_of_variation], axis = 1)
vari_prec.columns = ['sample_precision', 'coefficient_of_variation']
print(vari_prec)


#Arranging the plots into a single figure
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
# Plotting coefficient of variation
sns.histplot(vari_prec['coefficient_of_variation'], bins=30, kde=True, ax=axes[0])
axes[0].set_title('Distribution of Coefficient of Variation')
axes[0].set_xlabel('Coefficient of Variation')
axes[0].set_ylabel('Frequency')
# Plotting sample precision
sns.histplot(vari_prec['sample_precision'], bins=30, kde=True, ax=axes[1])
axes[1].set_title('Distribution of Sample Precision')
axes[1].set_xlabel('Sample Precision')
axes[1].set_ylabel('Frequency')
plt.tight_layout()
plt.show()


# Identifying soil data with high coefficient of variation greater than 0.8 and sample precision greater than 0.05
vari_prec2 = vari_prec[(vari_prec['coefficient_of_variation'] > 0.8) & (vari_prec['sample_precision'] < 0.05)]

# Displaying fields with high coefficient of variation and low sample precision
print("Fields with high coefficient of variation and low sample precision:")
print(vari_prec2) #The ones that have high variation and low precision (less good data) are %Na Sat, Rhizobia, Protozoan


###Spatial Plotting Sample##########

#Reading in Oregon Well data
or_well_loc = "https://raw.githubusercontent.com/lenawang33/Regrow_interview/main/First3_Last3_GWMA.csv"
or_well_df = pd.read_csv(or_well_loc, encoding = 'utf-8')


#Reading in Oregon outline geojson
or_outline_loc = "https://raw.githubusercontent.com/lenawang33/Regrow_interview/main/Oregon_State_Boundary_4303926865431890091.geojson"
response1 = requests.get(or_outline_loc)
or_outline = response1.content.decode('utf-8') #Decode as UTF-8
or_outline_gdf = gpd.read_file(or_outline)

#Reading in Southern Willamette Valley geojson
swv_loc = "https://raw.githubusercontent.com/lenawang33/Regrow_interview/main/Groundwater_Management_Area_So_Willamette_Valley.geojson"
response = requests.get(swv_loc)
swv_outline = response.content.decode('utf-8')  # Decode as UTF-8
swv_outline_gdf = gpd.read_file(swv_outline)



#Plotting the wells in the Southern Willamette Valley coloring wells by Last
fig2, ax = plt.subplots(figsize = (20, 20))
or_well_gdf = gpd.GeoDataFrame(or_well_df, 
                               geometry = gpd.points_from_xy(or_well_df['Long_Dec'], or_well_df['Lat_Dec']))
or_well_gdf.plot(ax = ax,
                 column = 'Last',
                 legend = True,
                 markersize = 50,
                 cmap = 'viridis',
                 alpha = 0.7,
                 legend_kwds = {'label': "Average Nitrate \nmg NO$_3$-N/L \n(2021-2024)", 'shrink': 0.5, 
                                'orientation': 'vertical'}
                 )
# Adding the Southern Willamette Valley boundary
swv_outline_gdf.boundary.plot(ax = ax, 
                              color='blue',
                              linewidth = 1,
                              label = 'SWV Outline')
# Adding labels and title
ax.set_title('Oregon Domestic Wells in Southern Willamette Valley')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
#Make sure the legend does not overlap with the plot
ax.legend(loc = 'lower right', bbox_to_anchor = (1, 0.8), 
          fontsize = 7)
#Building inset plot in the lower left corner
inset_ax = ax.inset_axes([0.09, 0.0, 0.35, 0.2])  # Location of inset plot
or_outline_gdf.boundary.plot(ax = inset_ax, color = 'black', linewidth = 1)
swv_outline_gdf.boundary.plot(ax = inset_ax, color = 'blue', linewidth = 1)
inset_ax.set_xlim(-125, -116)  # Region of interest
inset_ax.set_ylim(41, 47)      # Region of interest
inset_ax.set_title('OR', fontsize = 8, pad = 0.05)  # Make inset title text smaller
inset_ax.tick_params(axis = 'both', labelsize = 3, pad = 0.05)  # Make tick labels smaller
plt.show()








