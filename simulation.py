# This is the main program file
import pandas as pd
import math 

class Rocket():
    def __init__(self) -> None:
        # TEMP VALUES MUST BE CHANGED FOR REAL ONES
        self.fuelMass = 2       # Mass of fuel  
        self.dryMass = 8        # mass of the rocket without fuel
        self.currentMass = self.fuelMass + self.dryMass       # mass that will be updated as fuel is burnt
        
        self.topCrossSectionalArea = 0.0135
        
        self.CD = 0.6
        
    def updateMass(self, data : pd.DataFrame, dt : float, timeIndex : int) -> float:
        """
        Function to update mass of the rocket [kg]

        Args:
            data (pd.DataFrame): Dataframe with MFR + thrust force info
            dt (float) : Time step 
            timeIndex (int): Index of time you want to retrieve mass flow rate
        """
        massFlowRate = data['Mass Flow Rate (kg/s)'].loc[data.index[timeIndex]]   

        if massFlowRate < 1e-4:
            self.currentMass = self.dryMass # NOTE: might not need this 
        else:
            self.currentMass = self.currentMass - massFlowRate * dt
        
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
        self.initialAcceleration = 0
        
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

def getGravity(m_rocket, altitude, launchAngle) -> float: 
    #m_rocket (kg): current mass of the rocket
    #altitude (km): current height of the rocket above sea level
    #launchAngle (radians): launch angle of the rocket

    # CONSTANTS 
    g_universal = 9.8 #gravitational constant

    #force of gravity (in newtons)
    fg = m_rocket * g * math.cos(launchAngle)
    
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

def getDensity(altitude : float) -> float:
    """
    Function to get air density at current height, using barometric formula [kg m^-3]

    Args:
        altitude (float): Current altitude (height above sea level) of the rocket [m]

    Returns:
        density (float): Air density at the current height above sea level [kg m^-3]
    """
    baseDens = 1.2250 # [kg m^-3] baseline density of troposphere, 0 m above sea level 
    baseTemp = 288.15 # [K] Base temperature of troposphere
    lapseRate = 0.0065 # [K m^-1] Lapse rate
    const =  5.25588 # (gravity * molar mass of air) / (ideal gas constant * lapse rate)

    density = baseDens * ((baseTemp - lapseRate * altitude) / baseTemp) ** (const - 1) # Air density at the current height above sea level [kg m^-3]
    return density 

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

def getVelocity(velPrevious : float, acceleration : float, dt : float) -> float: 
# # # # # # # # # # # # # 
    """
    Function to update velocity at given time step [m s^-1]

    Args:
        velPrevious (float): Previous velocity [m s^-1] at timestep 
        acceleration (float): Acceleration [m s^-2] 
        dt (float): Time step [s]

    Returns:
        (float): Velocity [m s^-1] at next time step
    """
    return velPrevious + acceleration * dt

def getDisplacement(dispPrevious : float, velocity : float, dt : float) -> float: 
    """
    Function to update displacement at given time step [m]

    Args:
        dispPrevious (float): Previous displacement [m]
        velocity (float): Velocity [m s^-1]
        dt (float): Time step [s]

    Returns:
        (float): Displacement at next time step [m]
    """
    return dispPrevious + velocity * dt

def main() -> None:

    # Initializing rocket and launch parameters 

    ourRocket = Rocket()
    launchParameters = Parameters('', 100, 2)

    MFRThrustData = pd.read_csv("RecoverySim24-25/Thrust_MFR.csv")
    
    velocity = [launchParameters.initialVelocity]
    displacement = [launchParameters.initialDisplacement]
    acceleration = [launchParameters.initialAcceleration]
    time = [1e-6]
    thrust = [0]
    gravity = [0] 
    drag = [0]
    density = [0]
    dt = launchParameters.timestep
    # massFlowRate = [] #needs to be changed when the massFlowRate is a list. This should be the first index of the mfr list
    
    i = 0
    while True:
        altitude = displacement[i] + launchParameters.launchAltitude 


        # Updating velocity and displacement 
        
        velocityHalfTimeStep = getVelocity(velocity[i], acceleration[i], (dt/2.0)) # Velocity at timestep i + 1/2 
        displacementFullTimeStep = getDisplacement(displacement[i], velocityHalfTimeStep, dt) # Displacement at timestep i + 1
        
        # Now calculating acceleration for timestep i + 1
       
        densityFullTimeStep = getDensity(altitudeFullTimeStep) # Density at timestep i + 1
        ourRocket.updateMass(MFRThrustData, dt, i+1) # Updating mass at timestep i + 1. 
        altitudeFullTimeStep = displacementFullTimeStep + launchParameters.launchAltitude # Altitude at timestep i + 1
        # Calculating all forces at timestep i + 1
        thrustFullTimeStep = getThrust(i+1, MFRThrustData)
        gravityFullTimeStep = getGravity(ourRocket.currentMass, altitudeFullTimeStep, launchParameters.launchAngle)  # Gravity at timestep i + 1, using altitude and mass at timestep i + 1
        dragFullTimeStep = getDrag(velocityHalfTimeStep, densityFullTimeStep, data[], ourRocket.topCrossSectionalArea) # TODO: COMPLETE DATA FOR DRAG COEFFICIENT Drag at timestep i + 1
        accelerationFullTimeStep = getAcceleration(dragFullTimeStep, gravityFullTimeStep, thrustFullTimeStep, ourRocket.currentMass) 
       
        # Now catching up velocity to full timstep 

        velocityFullTimeStep = getVelocity(velocityHalfTimeStep, accelerationFullTimeStep, (dt/2.0))
        
        # if statement for breaking conditions 
        
        if (displacementFullTimeStep < 0) or (time[i] > 2000):  # When rocket starts to move downwards OR time is too long 
            break 

        # Storing all variables at full time step 
        
        velocity.append(velocityFullTimeStep) 
        acceleration.append(accelerationFullTimeStep)
        displacement.append(displacementFullTimeStep)
        time.append(time[i] + dt) 
        thrust.append(thrustFullTimeStep) 
        gravity.append(gravityFullTimeStep)
        drag.append(dragFullTimeStep) 
        density.append(densityFullTimeStep) 

        i += 1 

    print("Apogee: " + str(max(displacement)))

    # Now plotting graphs 

    # 1) Acceleration, velocity, displacement 
    plt.figure(1)

    plt.subplot(1, 3, 1)
    plt.plot(time, displacement, label = 'Displacement')
    plt.title('Displacement')

    plt.subplot(1, 3, 2)
    plt.plot(time, velocity, label = 'Velocity')
    plt.title('Velocity')

    plt.subplot(1, 3, 3)
    plt.plot(time, acceleration, label = 'Acceleration')
    plt.title('Acceleration')

    # 2) Forces 

    plt.figure(2)

    plt.subplot(1, 3, 1)
    plt.plot(time, thrust, label = 'Thrust')
    plt.title('Thrust')

    plt.subplot(1, 3, 2)
    plt.plot(time, drag, label = 'Drag')
    plt.title('Drag')

    plt.subplot(1, 3, 3)
    plt.plot(time, gravity, label = 'Gravity')
    plt.title('Gravity')

    # 3) Density 

    plt.figure(3) 
    plt.plot(time, density, label = 'Density')
    plt.title('Density')






    

    
