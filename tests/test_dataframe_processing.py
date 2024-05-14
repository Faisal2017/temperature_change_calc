import pandas as pd
from unittest.mock import patch
import pytest
from flight_temp_pipeline.dataframe_processing import clean_and_handle_missing_data, greater_than_5_change, process_dataframe


def test_clean_and_handle_missing_data():
    data = {
        'missionTime': [1, 2, 4, 4, 5],
        'S1_TC_BC_Ambient.temperature': [20, None, 22, 22, 24]
    }
    df = pd.DataFrame(data)

    cleaned_df = clean_and_handle_missing_data(df)

    # check if missing value is interpolated
    assert cleaned_df['S1_TC_BC_Ambient.temperature'].isna().sum() == 0

    # check interpolated value is 21
    assert cleaned_df['S1_TC_BC_Ambient.temperature'].iloc[1] == 21

    # length of df should be 1 less after removing duplicate
    assert len(cleaned_df) == 4


def test_greater_than_5_change():
    data = {
        'missionTime': [1, 2, 3, 4, 5],
        'S1_TC_BC_Ambient.temperature': [20, 25, 25, 30, 40]
    }
    df = pd.DataFrame(data)

    changes = greater_than_5_change(df)

    assert 'S1_TC_BC_Ambient.temperature' in changes
    assert len(changes['S1_TC_BC_Ambient.temperature']) == 1
