import pandas as pd
from datetime import datetime

# input and output files defined
input_file = r'Raw_Data_SPY_10Y_General.csv'
output_file = r'Fixed_Data_SPY_10Y_General.csv'

# Pandas reads input file into data
data = pd.read_csv(input_file)

# Defines the old date format and the new date format when the date column is named 'Date'

old_date_format = "%m/%d/%Y"  # Adjust if your date format is different
new_date_format = "%Y-%m-%d"  # New fixed format

# Converts the date column to datetime first, and then changes them to desired format
data['Date'] = pd.to_datetime(data['Date'], format=old_date_format)  # read original date in datetime format
data['Date'] = data['Date'].dt.strftime(new_date_format)  # Format to the new date format

# Write the cleaned data to a new CSV file
data.to_csv(output_file, index=False)

# Print success message
print(f"Fixed date data successfully written to {output_file}")


