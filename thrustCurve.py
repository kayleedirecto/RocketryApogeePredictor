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

    # Create an interpolation function
    interp_func = interp1d(df['Time (s)'], df['Thrust (N)'], kind='linear', fill_value='extrapolate')

    # Generate a new Time (s) grid with 1ms steps
    new_time = np.arange(df['Time (s)'].min(), df['Time (s)'].max(), 1)

    # Interpolate data
    new_values = interp_func(new_time)

    # Create the new DataFrame
    df_interpolated = pd.DataFrame({'Time (s)': new_time, 'Thrust (N)': new_values})

    return df_interpolated

def updateCSV(df : pd.DataFrame, filename : str = 'ThrustCurve.csv') -> None:
    df.to_csv(filename, index=False)
    return

# extractThrustcurve("Cesaroni_10367N1800-P.csv")

def main() -> None:
    motorFile = "Cesaroni_10367N1800-P.csv"
    df = extractThrustcurve(motorFile)
    updateCSV(df, "Test.csv")

    interpolatedDataFrame = interpolateCurve(df)
    updateCSV(interpolatedDataFrame, "LC_Curve.csv")
    
main()