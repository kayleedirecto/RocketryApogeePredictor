import pandas as pd
import math 

MFRThrustData = pd.read_csv("RecoverySim24-25/Thrust_MFR.csv")
print(MFRThrustData.head())

def getThrust(timeIndex : int, data : pd.DataFrame) -> float:
    """
    Function to get thrust force [m s^-2] 

    Args:
        timeIndex (int): Index of time you want to retrieve thrust force 
        data (pd.DataFrame): Dataframe with MFR + thrust force info

    Returns:
        thrust (float): Thrust force [m s^-2] 
    """
    thrust = data['Thrust (N)'].loc[data.index[timeIndex]]   
    return thrust

print("At time step 3, thrust = ", getThrust(3, MFRThrustData))