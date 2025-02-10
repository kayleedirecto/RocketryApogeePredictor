import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def extractThrustcurve(filepath : str) -> pd.DataFrame:
    
    # Read the CSV, skipping the first 4 rows (adjust if necessary)
    df = pd.read_csv(filepath, skiprows=4, header=0)
    
    # Display the array (optional)
    # print(df)
    return df

def interpolateCurve(df : pd.DataFrame, timestep : float = 1e-4) -> pd.DataFrame:
    # Ensure Time (s) is numeric for interpolation
    
    timeVals = df['Time (s)'].to_numpy()       # Convert time column to numpy array
    thrustVals = df['Thrust (N)'].to_numpy()   # Convert thrust column to numpy array

    # Create an interpolation function
    if len(df) < 2:
        raise ValueError("Not enough unique points in 'Time (s)' to perform interpolation.")
    
    interp_func = interp1d(df['Time (s)'], df['Thrust (N)'], kind='linear', fill_value='extrapolate')
    
    # Rearrange arrays with necessary timestep
    newTime = np.arange(timeVals.min(), timeVals.max(), timestep)
    newThrust = interp_func(newTime)

    # Create the new DataFrame
    df_interpolated = pd.DataFrame({'Time (s)': newTime, 'Thrust (N)': newThrust})

    return df_interpolated

def updateCSV(df : pd.DataFrame, filename : str = 'ThrustCurve.csv') -> None:
    df.to_csv(filename, index=False)
    return

def main() -> None:
    motorFile = "Cesaroni_10367N1800-P.csv"
    df = extractThrustcurve(motorFile)
    
    ### TEST CSV TO CHECK INTERMEDIARY RESULTS ###
    # updateCSV(df, "Test.csv")

    interpolatedDataFrame = interpolateCurve(df)
    updateCSV(interpolatedDataFrame, "LC_Curve.csv")
    
main()