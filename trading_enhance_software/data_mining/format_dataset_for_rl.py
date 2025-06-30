import os
import numpy as np
from pathlib import Path
import pandas as pd
import subprocess


def read_csvs_and_apply_timedelta(comb_dict):
    modified_dfs = {}
    for source, assets in comb_dict.items():
        modified_dfs[source] = {}
        for asset, timeframes in assets.items():
            modified_dfs[source][asset] = {}
            for timeframe, info in timeframes.items():
                file_path = info["file_path"]
                timedelta_hours = info["timedelta"]

                # Placeholder for loading the actual DataFrame from CSV
                df = pd.read_csv(file_path, index_col=0, parse_dates=True)
                df.index = df.index + pd.Timedelta(hours=timedelta_hours)

                modified_dfs[source][asset][timeframe] = df
    return modified_dfs


# List to hold all the DataFrames across sources, assets, and timeframes
def merge_dataframes(modified_dfs):
    all_dfs = []

    for source in modified_dfs:
        for asset in modified_dfs[source]:
            for timeframe in modified_dfs[source][asset]:
                # Access the DataFrame
                df = modified_dfs[source][asset][timeframe]
                # Append the DataFrame to our list
                all_dfs.append(df)

    # Concatenate all DataFrames along the columns using their datetime index for alignment
    merged_df = pd.concat(all_dfs, axis=1, ignore_index=False).sort_index()

    return merged_df


def timestamp_to_week_cycle(timestamp, milliseconds_in_week=7 * 24 * 60 * 60 * 1000):
    # Calculate the total number of milliseconds since the beginning of the week (Monday)
    total_milliseconds = (
        (timestamp.dayofweek * 24 * 60 * 60 * 1000)
        + (timestamp.hour * 60 * 60 * 1000)
        + (timestamp.minute * 60 * 1000)
        + (timestamp.second * 1000)
        + timestamp.microsecond / 1000
    ) % milliseconds_in_week

    # Map the milliseconds to a 2π cycle
    radians = (total_milliseconds / milliseconds_in_week) * 2 * np.pi
    return np.sin(radians), np.cos(radians)


def timestamp_to_weekday_hour(timestamp):
    day = timestamp.weekday()
    hour = timestamp.hour

    return day, hour


# should be {'month_remaining': '1200000', 'hour_remaining': '60000', 'minute_remaining': '1200'} on Max Business Plan

SAVE_FOLDER = "./data/dataset"
Path(SAVE_FOLDER).mkdir(parents=True, exist_ok=True)

price_column = "close_0060_BTC"

subprocess.run(
    [
        "python",
        "dataMining/RL_Data_Scraper.py",
        "--coins",
        "BTC",
        "--resolutions",
        "1h,1d",
        "--start_time",
        "2020-07-01T00:00:00",
        "--end_time",
        "2024-03-11T00:00:00",
        "--endpoint_file_paths",
        "./data/endpoints_file_path_binance.json",
        "--save_folder",
        "./data/test/binance/historical",
        "--mode",
        "historical",
    ]
)

comb_dict = {
    "binance": {
        "BTC": {
            "1h": {
                "file_path": "./data/test/binance/historical/scraped_binance_BTC_1h_2024-03-11_00:00:00.csv",
                "timedelta": 1,
            },
            "24h": {
                "file_path": "./data/test/binance/historical/scraped_binance_BTC_1d_2024-03-11_00:00:00.csv",
                "timedelta": 24,
            },
        }
    }
}

modified_dfs = read_csvs_and_apply_timedelta(comb_dict)
merged_df = merge_dataframes(modified_dfs)
pd.set_option("display.max_rows", None)

# Detect rows without any NaN values
rows_without_nan = merged_df.dropna().index

# # Index of the first non-NaN row
# first_non_nan_index = rows_without_nan[0] if not rows_without_nan.empty else None

# Choose first index manually
first_non_nan_index = merged_df.index[3000]
print("datetime of the first index:", first_non_nan_index)

# Index of the last non-NaN row
last_non_nan_index = rows_without_nan[-1] if not rows_without_nan.empty else None
print("datetime of the last index:", last_non_nan_index)

# The actual slicing
merged_df = merged_df.loc[first_non_nan_index:last_non_nan_index]

merged_df = merged_df.fillna(0.0)


# Add columns for time encoding
# merged_df['week_sin'], merged_df['week_cos'] = zip(*merged_df.index.map(timestamp_to_week_cycle))
merged_df["weekday"], merged_df["hour"] = zip(
    *merged_df.index.map(timestamp_to_weekday_hour)
)

cols = merged_df.columns.tolist()  # Get the list of all columns
reordered_cols = cols[-2:] + cols[:-2]  # Last two columns to the front
merged_df = merged_df[reordered_cols]  # Apply new column order

merged_df.to_csv(os.path.join(SAVE_FOLDER, "merged_df.csv"))

# Save final dataset as .npy files

close_price_index = merged_df.columns.get_loc(price_column)
price_array = np.array(merged_df.iloc[:, close_price_index])
price_array = np.expand_dims(price_array.astype(np.float32), axis=1)

tech_array = np.array(merged_df).astype(np.float32)

print("price_array shape:", price_array.shape)
print("tech_array shape:", tech_array.shape)

np.save(os.path.join(SAVE_FOLDER, "price_outfile.npy"), price_array)
np.save(os.path.join(SAVE_FOLDER, "metrics_outfile.npy"), tech_array)
