# Code for custom code recipe compute-correlation (imported from a Python recipe)

# To finish creating your custom recipe from your original PySpark recipe, you need to:
#  - Declare the input and output roles in recipe.json
#  - Replace the dataset names by roles access in your code
#  - Declare, if any, the params of your custom recipe in recipe.json
#  - Replace the hardcoded params values by acccess to the configuration map

# See sample code below for how to do that.
# The code of your original recipe is included afterwards for convenience.
# Please also see the "recipe.json" file for more information.

# import the classes for accessing DSS objects from the recipe
import dataiku
# Import the helpers for custom recipes
from dataiku.customrecipe import *

# Inputs and outputs are defined by roles. In the recipe's I/O tab, the user can associate one
# or more dataset to each input and output role.
# Roles need to be defined in recipe.json, in the inputRoles and outputRoles fields.

# Retrieve array of dataset names from 'input' role, then create datasets
input_names = get_input_names_for_role('input')
input_datasets = [dataiku.Dataset(name) for name in input_names]

# For outputs, the process is the same:
output_names = get_output_names_for_role('main_output')
output_datasets = [dataiku.Dataset(name) for name in output_names]

# Retrieve parameter values from the of map of parameters
threshold = get_recipe_config()['threshold']

# Note about typing:
# The configuration of the recipe is passed through a JSON object
# As such, INT parameters of the recipe are received in the get_recipe_config() dict as a Python float.
# If you absolutely require a Python int, use int(get_recipe_config()["my_int_param"])


#############################
# Your original recipe
#############################
print('test')
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np

# Read the input
input_dataset = input_datasets[0]
df = input_dataset.get_dataframe()
column_names = df.columns

# We'll only compute correlations on numerical columns
# So extract all pairs of names of numerical columns
pairs = []
for i in xrange(0, len(column_names)):
    for j in xrange(i + 1, len(column_names)):
        col1 = column_names[i]
        col2 = column_names[j]
        if df[col1].dtype == "float64" and \
           df[col2].dtype == "float64":
            pairs.append((col1, col2))

# Compute the correlation for each pair, and write a
# row in the output array
output = []
for pair in pairs:
    corr = df[[pair[0], pair[1]]].corr().iloc[0][1]
    if np.abs(corr) > threshold:
        output.append({"col0" : pair[0],                       "col1" : pair[1],
                       "corr" :  corr})

# Write the output to the output dataset
output_dataset =  output_datasets[0]
output_dataset.write_with_schema(pd.DataFrame(output))