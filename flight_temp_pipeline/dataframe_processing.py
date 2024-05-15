import os

import pandas as pd
import seaborn as sns
import scipy
import matplotlib.pyplot as plt


UPLOAD_DIRECTORY = os.getenv('UPLOAD_DIRECTORY', '../uploads/')
print(UPLOAD_DIRECTORY)

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


def plot_line_graph(df_passed_in, time_string):
    # set the 'missionTime' column as the index
    df_passed_in.set_index('missionTime', inplace=True)

    # Plot the data
    ax = df_passed_in.plot(figsize=(10, 6))
    ax.set_xlabel('Mission Time (Seconds)')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title('Temperature Variation Over Time')
    ax.grid(True)

    # Adjust the legend position and layout
    ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1), borderaxespad=0)
    plt.tight_layout()
    plot_file_name = f'uploads/{time_string}/temp_change_line_graph.pdf'

    plt.savefig(plot_file_name)


def greater_than_5_change(dataframe):
    temperature_columns = [col for col in dataframe.columns if 'temperature' in col]

    for column in temperature_columns:
        dataframe[f'Change_in_temp: {column}'] = dataframe[column].diff()

    # threshold for the rate of change
    temp_threshold = 5

    temp_changes = {}

    for column in temperature_columns:
        condition = dataframe[f'Change_in_temp: {column}'].abs() > temp_threshold

        if condition.any():
            temp_changes[column] = dataframe[condition][['missionTime', f'Change_in_temp: {column}']]

    return temp_changes


def clean_and_handle_missing_data(df):
    df.interpolate(inplace=True)

    # first duplicate occurrences are dropped
    df.drop_duplicates(keep='first', inplace=True)

    # drop any nulls still left and not providing any useful info
    df = df.dropna()

    return df


def process_dataframe(df, time_string):
    df = clean_and_handle_missing_data(df)

    df_to_plot = df.drop(df.columns[0], axis=1)

    plot_line_graph(df_to_plot, time_string)

    temp_changes = greater_than_5_change(df)

    for sensor_name, df in temp_changes.items():
        safe_name = sensor_name.replace('.', '_').replace(' ', '_')

        file_name = f"uploads/{time_string}/{safe_name}.csv"

        df.to_csv(file_name, index=False)

        print(f"Written: {file_name}")
