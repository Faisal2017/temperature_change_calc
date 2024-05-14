import os
import sys
import time


import pandas as pd
import seaborn as sns
import scipy
import matplotlib.pyplot as plt
import json
import csv



# # Define the directory to save files, using an environment variable
UPLOAD_DIRECTORY = os.getenv('UPLOAD_DIRECTORY', 'uploads/')

print(UPLOAD_DIRECTORY)

# # Ensure the directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


def plot_line_graph(df_passed_in):
    # Set the 'missionTime' column as the index
    df_passed_in.set_index('missionTime', inplace=True)

    # Plot the data
    ax = df_passed_in.plot(figsize=(10, 6))
    ax.set_xlabel('Mission Time (Seconds)')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title('Temperature Variation Over Time')
    ax.grid(True)

    # Adjust the legend position and layout
    ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1), borderaxespad=0)

    plt.tight_layout()  # Ensures all plot elements fit within the figure area
    # plt.show()

    cwd = os.getcwd()

    cwd2 = os.path.join(cwd, "uploads/")
    # os.makedirs(cwd + '/uploads')

    print(cwd2)

    time_string = time.strftime("%Y%m%d-%H%M%S")
    plot_file_name = f'uploads/{time_string}_line_graph.pdf'

    plt.savefig(plot_file_name)

    # plt.savefig(f'{time_string}_line_graph.pdf')
    # plt.savefig(f'/home/fal/Desktop/rocketlab/uploads/{time_string}_line_graph.pdf')


def read_csv_and_process(df):
    # cwd = os.getcwd()
    # print(cwd)

    # csv_file_location = cwd + '/FlightAcl.csv'
    # csv_file_location = '/home/fal/Desktop/rocketlab/FlightAcl.csv'

    # df = pd.read_csv(csv_file_location)
    # print('len df : ', len(df))

    # Handle missing data
    # Option 3: Interpolate (linear by default, can be changed to 'time' if 'missionTime' is datetime)
    df.interpolate(inplace=True)

    # Remove duplicates, first occurrences are dropped, can change to 'last' if required
    df.drop_duplicates(keep='first', inplace=True)

    # drop any nulls still left and not providing any useful info
    df = df.dropna()

    # Display final info to verify the cleaning
    print('len df : ', len(df))

    df_to_plot = df.drop(df.columns[0], axis=1)

    plot_line_graph(df_to_plot)

    # # Calculating the temperature change for each temperature channel except 'missionTime'
    # temperature_columns = [col for col in df.columns if 'temperature' in col]
    #
    # for column in temperature_columns:
    #     df[f'Change_{column}'] = df[column].diff().abs()  # Calculate absolute temperature change
    #
    # # Define a threshold for the temperature change
    # threshold = 5
    #
    # # Identify and print where the temperature change is greater than 5 °C
    # temp_changes = []
    #
    # for column in temperature_columns:
    #
    #     changes_gt_threshold = df[df[f'Change_{column}'] > threshold][['missionTime', column, f'Change_{column}']]
    #
    #     if not changes_gt_threshold.empty:
    #         temp_changes.append((column, changes_gt_threshold))
    #
    # # Output the results
    # # for sensor, data in temp_changes:
    # #     print(f"Exceedances for {sensor}:")
    # #     print(data)

    # Calculating the rate of change for each temperature channel except 'missionTime'
    temperature_columns = [col for col in df.columns if 'temperature' in col]
    for column in temperature_columns:
        df[f'Change_in_temp: {column}'] = df[column].diff()

    # Define a threshold for the rate of change
    temp_threshold = 5

    # Find where the change in temp is greater than 5 °C/s
    temp_changes = {}

    for column in temperature_columns:
        condition = df[f'Change_in_temp: {column}'].abs() > temp_threshold
        if condition.any():
            temp_changes[column] = df[condition][['missionTime', f'Change_in_temp: {column}']]

    # Output the results
    # for sensor, data in temp_changes.items():
    #     print(f"Exceedances for {sensor}:")
    #     print(data)

    for sensor_name, df in temp_changes.items():
        safe_name = sensor_name.replace('.', '_').replace(' ', '_')  # Replace dots and spaces for filename safety

        file_name = f"/home/fal/Desktop/rocketlab/uploads/{safe_name}.csv"

        df.to_csv(file_name, index=False)

        print(f"Written: {file_name}")


# if __name__ == '__main__':
#     read_csv_and_process('a')
