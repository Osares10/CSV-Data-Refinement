# Combine multiple csv files into a single csv file, interpolating missing data.

import os
import pandas as pd

def combine_csv_files(file_list, variable, initial_time, final_time):
    combined_data = pd.DataFrame(columns=['time', variable])

    for file_path in file_list:
        # Extract filename without extension
        filename = os.path.splitext(os.path.basename(file_path))[0]

        # Read the csv file, parsing 'time' column as datetime
        df = pd.read_csv(file_path, parse_dates=['time'])

        # Check if the variable column exists in the DataFrame
        if variable in df.columns:
            # Filter data based on initial and final time
            df = df[(df['time'] >= initial_time) & (df['time'] <= final_time)]

            # Create a new column with the data from the variable
            df[filename] = df[variable]

            # Append the relevant columns to the combined data
            combined_data = pd.merge(combined_data, df[['time', filename]], on='time', how='outer')

    # Set 'time' column as the index
    combined_data = combined_data.set_index('time')

    # Group by index (time) and aggregate the values
    combined_data = combined_data.groupby(combined_data.index).mean()

    # Resample and interpolate missing data
    combined_data = combined_data.resample('10T').interpolate(method='time')

    # Save the combined data to a new csv file
    combined_data.to_csv(variable + '.csv')

# Example usage
file_list = ['accuweather.csv', 'awc.csv', 'bme680.csv', 'open_meteo.csv', 'openweathermap.csv', 'station-SD.csv', 'station.csv']
variable = 'windSpeed'
initial_time = '2023-04-30 23:00'
final_time = '2023-05-15 23:50'

combine_csv_files(file_list, variable, initial_time, final_time)
