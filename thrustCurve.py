import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def extractThrustcurve(filepath : str) -> pd.DataFrame:
    # Read the CSV, skipping the first 4 rows (adjust if necessary)
    df = pd.read_csv(filepath, skiprows=4, header=0)
    # Display the array (optional)
    print(df)
    return df

def interpolateCurve(df : pd.DataFrame) -> pd.DataFrame:
    # Ensure Time (s) is numeric for interpolation
    
    timeVals = df['Time (s)'].to_numpy()       # Convert time column to numpy array
    thrustVals = df['Thrust (N)'].to_numpy()   # Convert thrust column to numpy array

    # Create an interpolation function
    if len(df) < 2:
        raise ValueError("Not enough unique points in 'Time (s)' to perform interpolation.")
    
    interp_func = interp1d(df['Time (s)'], df['Thrust (N)'], kind='linear', fill_value='extrapolate')
    
    newTime = np.arange(timeVals.min(), timeVals.max(), 0.001)
    newThrust = interp_func(newTime)

    # Create the new DataFrame
    df_interpolated = pd.DataFrame({'Time (s)': newTime, 'Thrust (N)': newThrust})

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

    interpolatedDataFrame = interpolateCurve(df)
    updateCSV(interpolatedDataFrame, "LC_Curve.csv")
    
main()