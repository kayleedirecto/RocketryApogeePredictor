'''
NOTE Things you need to change if you want to get the thrust curve for different motors: 
1. motorFile - the csv file containing the thrust curve data points 
2. Isp - the specific impulse 
3. fuelMass - fuel mass of motor, used to check interpolation of mass flow rate is accurate 
4. In extractThrustcurve, adjust number of rows to skip from the motor file csv  
'''

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy import integrate
import matplotlib.pyplot as plt

def extractThrustcurve(filepath : str) -> pd.DataFrame:
    """
    Reads the motor file CSV to extract the thrust curve data 

    Args:
        filepath (str): File path to the motor file CSV 

    Returns:
        df (pd.dataframe): Data frame containing thrust curve info 
    """

    df = pd.read_csv(filepath, skiprows=4, header=0) # NOTE: Adjust number of rows to skip if necessary 

    return df

def interpolateCurve(df : pd.DataFrame, timestep : float = 1e-4) -> pd.DataFrame:
    """
    Interpolates the thrust curve to add more data points 

    Args:
        df (pd.dataframe): Dataframe extracted from motor file CSV 
        timestep (float): Time step between time points desired 

    Returns:
        df_interpolated (pd.dataframe): Data frame containing thrust curve with extrapolated points  
    """

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
    """
    Creates new CSV file  

    Args:
        df (pd.dataframe): Dataframe you would like to save  
        filename (str): File name to save to. "ThrustCurve.csv" by default  

    Returns:
        None
    """
    df.to_csv(filename, index=False)
    return

def calculateMassFlowRate(df : pd.DataFrame, Isp : float) -> pd.DataFrame: 
    """
    Calculates mass flow rate (MFR) from thrust curve   

    Args:
        df (pd.dataframe): Dataframe containing thrust info   
        Isp (float): Specific impulse of motor  

    Returns:
        df (pd.dataframe): Updated dataframe containing MFR info 
    """
    g0 = 9.80665 # Standard gravity [m/s]
    df['Mass Flow Rate (kg/s)'] = df['Thrust (N)'] / (Isp * g0)
    return df
    
def main() -> None:
    Isp = 172.65 # [s], Specific impulse of motor 
    fuelMass = 4.835 # [kg] Fuel mass in kg , used to check MFR calculated properly 
    motorFile = "Cesaroni_8187M1545-P.csv" # Path desired to motor file 
    df = extractThrustcurve(motorFile)
    
    interpolatedDataFrame = interpolateCurve(df) 
    interpolatedDataFrame = calculateMassFlowRate(interpolatedDataFrame, Isp) # Calculating mass flow rate

    # Integrating MFR to ensure it is within reasonable relative error of actual fuel mass 
    integratedMFR = integrate.trapz(interpolatedDataFrame['Mass Flow Rate (kg/s)'], interpolatedDataFrame['Time (s)'])
    print("Integrated MFR = ", integratedMFR)
    print("Actual fuel mass = ", fuelMass)
    relativeError = (integratedMFR - fuelMass) / fuelMass
    print("Relative error = ", relativeError, "%")

    if abs(relativeError) > 2: 
        print("Potential problem with integration. Integrated mass flow rate not within 2% of actual fuel mass. Not saving file. Check fuel mass, thrust curve, or integration.")
    else: 
        print("Saving file...")
        updateCSV(interpolatedDataFrame, motorFile[:-4] + "_ThrustMFR.csv") # Saving thrust / MFR file to corresponding motor file name 
    
main()