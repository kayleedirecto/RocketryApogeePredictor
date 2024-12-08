# This is the main program file
import pandas as pd
import math 

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

def getGravity(m_rocket, altitude, launchAngle) -> float: 
    #m_rocket (kg): current mass of the rocket
    #altitude (km): current height of the rocket above sea level
    #launchAngle (radians): launch angle of the rocket

    # CONSTANTS 
    g_universal = 6.67e-11 #Nm^2/kg^2 (universal gravitational constant)
    m_earth = 5.972e24 #kg (mass of the earsth)
    r_earth = 6.378e6 #m (radius of the earth)

    #force of gravity (in newtons)
    fg = (g_universal * m_rocket * m_earth * math.cos(launchAngle))/(r_earth + altitude)
    return fg

def getDrag(velocity : float, density : float, data : pd.DataFrame = Parameters.data, crossArea : float = Rocket.topCrossSectionalArea) -> float: 
    """
    Function to get drag force

    Args:
        velocity (float): Relative velocity of the rocket, in y dimension is just velocity [m s^-2]
        density (float): Current density [kg m^-3]
        data (pd.DataFrame): Holds coefficient of drag data 

    Returns:
        drag (float): Drag force [N]
    """
    drag = 0.5 * data[] * density * crossArea * velocity * velocity
    
    return drag 

def getDensity(displacement : float, temp : float, launchAltitude : float = Parameters.launchAltitude) -> float:
    """
    Function to get air density at current height, using barometric formula [kg m^-3]

    Args:
        displacement (float): Current displacement of the rocket [m]
        temp (float): Current temperature at height above sea level [K]
        launchAltitude (float): Height of launch altitude above sea level [m]

    Returns:
        density (float): Air density at the current height above sea level [kg m^-3]
    """
    baseDens = 1.2250 # [kg m^-3] baseline density of troposphere, 0 m above sea level 
    baseTemp = 288.15 # [K] Base temperature of troposphere
    lapseRate = 0.0065 # [K m^-1] Lapse rate
    const =  5.25588 # (gravity * molar mass of air) / (ideal gas constant * lapse rate)
    z = launchAltitude + displacement # Current rocket height above sea level 

    density = baseDens * ((baseTemp - lapseRate * z) / baseTemp) ** (const - 1) # Air density at the current height above sea level [kg m^-3]
    return density 

def getTemp(displacement : float, launchAltitude : float = Parameters.launchAltitude) -> float: 
    """
    Function to get temperature at current height above sea level, using ISA 

    Args:
        displacement (float): Current displacement of the rocket [m]
        launchAltitude (float): Height of launch altitude above sea level [m]

    Returns:
        temp (float): Temperature at the current height above sea level [K]
    """

    baseTemp = 288.15 # Base temperature of troposphere [K]
    lapseRate = 0.0065 # Lapse rate [K m^-1]
    z = launchAltitude + displacement # Current rocket height above sea level 

    temp = baseTemp - lapseRate * z # Temperature in [K]

    return temp

def getAcceleration(drag : float, gravity : float, thrust : float,  mass : float) -> float:
    """
    Function to get acceleration [m s^-2] 

    Args:
        drag (float): Drag force [N]
        gravity (float): Gravity force [N]
        Thrust (float): Thrust force [N]
        mass (float): Current mass of rocket [kg] 

    Returns:
        acceleration (float): Acceleration [m s^-2] 
    """
    force = drag + gravity + thrust

    acceleration = force / mass 

    return acceleration 

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

        #getacceleration

        #getvelocity 
        #get position 

        # NOTE : Do we want to gte velocity and displacement in a function or just like this in the loop? 
        vx[oplanet] = vx[oplanet]+ax*(dt/2);
        vy[oplanet] = vy[oplanet]+ay*(dt/2);
        x[oplanet] = x[oplanet]+vx[oplanet]*dt;
        y[oplanet] = y[oplanet]+vy[oplanet]*dt;

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
    
    

    
