# This is the main program file
import pandas as pd

class Rocket():
    def __init__(self) -> None:
        # TEMP VALUES MUST BE CHANGED FOR REAL ONES
        self.wetMass = 10       # Mass with Fuel
        self.fuelMass = 2       # Mass of fuel  
        self.dryMass = self.wetMass - self.fuelMass
        
        self.topCrossSectionalArea = 0.0135
        
        self.CD = 0.6
        
class Parameters():
    def __init__(self, filePath : str, launchAltitude : int = 0, launchAngle : int = 0) -> None:
        self.data = pd.readcsv(filePath) #  Data frame will hold info on thrust curve, mass flow rate, drag coeff 

        self.timestep = 0.001 # 1ms timestep
        
        self.maxTime = 200      # After 200s if no break condition break
        
        self.launchAltitude = launchAltitude # Height above sea level 
        
        self.launchAngle = launchAngle      # Angle rocket is beign launched at (degrees) 
        
        # Integration Initial Conditions
        self.initialVelocity = 10e-6
        self.initialDisplacement = 10e-6

def getThrust(timeStep : int, data : pd.DataFrame = Parameters.data) -> float:
    
    return 

def updateMass () -> float:
    # if MFR = 0
    # return drymass
    
    # else calculate mass
    return

def getGravity() -> float: 
    # mass 
    # grav constant 
    # launch angle
    return 

def getDrag() -> float: 
    return

def getPressure() -> float:
    return

# Function to get temperature at current height., using ISA 
def getTemp(displacement : float) -> float: 
    # displacement : Current displacement of the rocket 
    baseTemp = 15.0 # Base temperature of troposphere [°C]
    lapseRate = 0.0065 # Lapse rate [°C/m]
    z = Parameters.launchAltitude + displacement # Current rocket height above sea level 

    tempC = baseTemp - lapseRate * z # Temperature in [°C]
    tempK = tempC + 273.15 # Temperature in K 

    # test 

    return tempK 

def getAcceleration() -> float:
    return
    # timestep 
    # forces (drag thrust grav)
    # mass 

def getVelocity() -> float: 
    return 

def getDisplacement() -> float: 
    return 

def main() -> None:
    velocity = [1e-6]
    displacement = []
    acceleration = []
    i = 0
    while True:
        altitude = displacement[i] + Parameters.launchAltitude
        
        #update mass 

        #getThrust
        #getGravity
        #getDrag

        #GetAcceleration

        #getvelocity 
        #get position 

        #update mass 

        #getThrust
        #getGravity
        #getDrag

        #get acceleration 

        #get velcotyi 
        #store everythign (velocity + postion + acc ) 


        #if statemenet for breaking conditions 


        i+=1


        
        pass
    
    

    
