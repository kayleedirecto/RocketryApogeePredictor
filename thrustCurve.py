import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import os

def extractThrustcurve(filepath : str) -> pd.DataFrame:
    # Read the CSV, skipping the first 4 rows (adjust if necessary)
    df = pd.read_csv(filepath, skiprows=4, header=0)
    # Display the array (optional)
    print(df)
    return df

def interpolateCurve(df : pd.DataFrame) -> pd.DataFrame:
    # Ensure Time (s) is numeric for interpolation
    df['Time (s)'] = pd.to_datetime(df['Time (s)'])
    df['Time (s)'] = (df['Time (s)'] - df['Time (s)'].iloc[0]).dt.total_seconds() * 1000  # Convert to milliseconds

    # Drop duplicates or nearly identical time points
    df = df.drop_duplicates(subset='Time (s)')
    
    # Sort values to ensure monotonicity
    df = df.sort_values('Time (s)')

    # Create an interpolation function
    if len(df) < 2:
        raise ValueError("Not enough unique points in 'Time (s)' to perform interpolation.")
    
    interp_func = interp1d(df['Time (s)'], df['Thrust (N)'], kind='linear', fill_value='extrapolate')
    print ( interp_func)

    # Generate a new Time (s) grid with 1ms steps
    new_time = np.arange(df['Time (s)'].min(), df['Time (s)'].max(), 1)
    print (new_time)

    # Interpolate data
    new_values = interp_func(new_time)
    print (new_values)

    # Create the new DataFrame
    df_interpolated = pd.DataFrame({'Time (s)': new_time, 'Thrust (N)': new_values})

    print (df_interpolated)
    return df_interpolated

def updateCSV(df : pd.DataFrame, filename : str = 'ThrustCurve.csv') -> None:
    df.to_csv(filename, index=False)
    return

def interpolateCurve_Pandas(df : pd.DataFrame) -> pd.DataFrame:
    
    # Ensure the time column is a datetime or numeric type
    df['Time (s)'] = pd.to_datetime(df['Time (s)'])

    # Set the time column as the index
    df.set_index('Time (s)', inplace=True)

    # Resample to 1ms intervals
    df_resampled = df.resample('1ms').mean()

    # Interpolate missing values linearly
    df_interpolated = df_resampled.interpolate(method='linear')

    return df_interpolated

# extractThrustcurve("Cesaroni_10367N1800-P.csv")

def main() -> None:
    motorFile = "Cesaroni_10367N1800-P.csv"
    df = extractThrustcurve(motorFile)
    updateCSV(df, "Test.csv")

    interpolatedDataFrame = interpolateCurve_Pandas(df)
    updateCSV(interpolatedDataFrame, "LC_Curve.csv")
    
main()