'''
Things to change if running a new simulation:
- Rocket class intialization 
- Parameters class initialization 
'''

import pandas as pd
import math 
from math import pi 
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

# Class to hold rocket properties 
class Rocket():
    def __init__(self, fuelMass : float, dryMass : float, diameter : float, CD : float) -> None:
        self.fuelMass = fuelMass                                    # Mass of fuel  
        self.dryMass = dryMass                                      # Mass of the rocket without fuel
        self.currentMass = self.fuelMass + self.dryMass             # Mass that will be updated as fuel is burnt
        self.diameter = diameter                                    # Largest diameter of rocket body tube 
        self.topCrossSectionalArea = pi * (self.diameter / 2) ** 2  # Cross sectional area of rocket 
        self.CD = CD                                                # Coefficient of drag 
        
    def updateMass(self, data: pd.DataFrame, dt: float, time: float) -> float:
        """
        Function to update mass of the rocket [kg]

        Args:
            data (pd.DataFrame): DataFrame with mass flow rate (MFR) + thrust force info
            dt (float): Time step 
            time (float): Time (s) you want to retrieve mass flow rate at 
        """
        if time > data['Time (s)'].iloc[-1]: 
            self.currentMass = self.dryMass # Brute force way to ensure fuel is depleted once thust is complete 
        else: 
            massFlowRate = np.interp(time, data['Time (s)'], data['Mass Flow Rate (kg/s)'])
            newFuelMass = self.fuelMass - massFlowRate * dt
            if newFuelMass < 0:
                print("Warning: Fuel mass below zero! Possible error in mass flow rate. Fuel mass = ", newFuelMass, ". Assuming fuel mass = 0.")
                self.currentMass = self.dryMass # Will just assume fuel mass is depleted 
            else:
                self.fuelMass = newFuelMass
                self.currentMass = self.fuelMass + self.dryMass

# Class to hold general parameters of launch             
class Parameters():
    def __init__(self, filePath : str, launchAltitude : int = 0, launchAngle : int = 0) -> None:
        self.data = pd.read_csv(filePath)           # Path of data frame holding info on thrust curve and MFR
        self.timestep = 0.0001                      # Timestep 
        self.maxTime = 200                          # Max time for breaking conditions 
        self.launchAltitude = launchAltitude        # Height above sea level 
        self.launchAngle = launchAngle              # The angle away from positive y axis the rocket is launched at (radians)
        self.initialVelocity = 10e-2                # Initial conditions not 0 to ensure no problems during integration 
        self.initialDisplacement = 10e-2
        self.initialAcceleration = 10e-2
        
def getThrust(time : float, data : pd.DataFrame) -> float:
    """
    Function to get thrust force [m s^-2] 

    Args:
        time (float): Time (s) you want to retrieve thrust at  
        data (pd.DataFrame): Dataframe with MFR + thrust force info

    Returns:
        thrust (float): Thrust force [m s^-2] 
    """
    if (time > data['Time (s)'].iloc[-1]):
        thrust = 0
    else: 
        thrust = float(np.interp(time, data['Time (s)'], data['Thrust (N)']))
    return thrust

def getGravity(rocketMass : float, launchAngle : float) -> float: 
    """
    Function to get force of gravity [m s^-2] 

    Args:
        rocketMass (float): Current mass of rocket
        launchAngle (float): Launch angle of rocket [rad]

    Returns:
        (float): Component of gravity acting in the direction of drag/thrust [N]
    """
    gUniversal = 9.8 # Standard gravity 

    return rocketMass * gUniversal / math.cos(launchAngle) 

def getDrag(velocity : float, density : float, dragCoeff : float, crossArea : float) -> float: 
    """
    Function to get drag force

    Args:
        velocity (float): Relative velocity of the rocket [m s^-2]
        density (float): Current air density [kg m^-3]
        data (pd.DataFrame): Holds coefficient of drag data 

    Returns:
        drag (float): Drag force [N]
    """
    drag = 0.5 * dragCoeff * density * crossArea * velocity * velocity 
    
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

def getODESystem(rocket,params): 
    """
    Function to create the ODE system for the integrator solver 

    Args: 
        rocket (class): Class containing the rocket information 
        params (class): Class containing the launch parameters 
    Returns: 
        dSdt (function): Matrix containing the ODE system for the integrator to solve 
    """

    def dSdt(t, S): 
        x, v = S # Extracting x (position) and v (velocity) from S vector 

        rocket.updateMass(params.data, params.timestep, t) # Getting mass for the current time 
        rho = getDensity(x + params.launchAltitude) # Density at the current altitude 
        gravity = getGravity(rocket.currentMass, params.launchAngle) 
        thrust = getThrust(t, params.data)
        drag = getDrag(v, rho, rocket.CD, rocket.topCrossSectionalArea)

        a = (thrust - drag - gravity) / rocket.currentMass
        return [v, a]
    
    return dSdt

def apogeeEvent(t, S): 
    """
    Function used as breaking condition in ODE solver to break when apogee is reached, i.e. when v = 0 
    Look into solve_ivp documentation for more info on the events argument 
    """
    x, v = S
    return v # Returns v value. ODE solver will break when this value = 0

# More specifications for events argument
apogeeEvent.terminal = True # Terminates when detecting the apogee event 
apogeeEvent.direction = -1 # Only terminates when velocity goes from positive to negative 

def main() -> None:

    # Initializing rocket and launch parameters 
    print("Initializing parameters")
    ourRocket = Rocket(4.835, 17.625, 0.132, 0.501994898) # Using data from LC 2024
    launchParameters = Parameters('LC2024Files/Cesaroni_8187M1545-P_ThrustMFR.csv', 295, 0.0523599)
    
    # Initializing system of ODEs to be solved by integrator 
    S0 = (launchParameters.initialDisplacement, launchParameters.initialVelocity)
    t = np.arange(stop = launchParameters.maxTime, step = launchParameters.timestep) # Times to solve at 
    dSdt = getODESystem(ourRocket, launchParameters)
    print("Solving...")
    solution = solve_ivp(dSdt, (t[0], t[-1]), S0, t_eval = t, events = apogeeEvent)
    print("Finished integration")

    tPlot = t[0:len(solution.y[0])] # Only plotting t values that the solution was calculated at 
    displacement = solution.y[0]
    velocity = solution.y[1]

    # Now getting the other values 
    print("Now obtaining acceleration, mass, thrust, drag, gravity...")
    acceleration = []
    rocketMass = []
    thrust = []
    drag = []
    gravity = []
    for i in range(len(tPlot)): 
        ourRocket.updateMass(launchParameters.data, launchParameters.timestep, tPlot[i]) # NOTE: It will probably show a warning, but the error in mass flow rate is very small. 
        rho = getDensity(displacement[i] + launchParameters.launchAltitude)
        gravityVal = getGravity(ourRocket.currentMass, launchParameters.launchAngle)
        thrustVal = getThrust(tPlot[i], launchParameters.data)
        dragVal = getDrag(velocity[i], rho, ourRocket.CD, ourRocket.topCrossSectionalArea)

        a = (thrustVal - dragVal - gravityVal) / ourRocket.currentMass
        
        acceleration.append(a)
        rocketMass.append(ourRocket.currentMass)
        thrust.append(thrustVal)
        drag.append(dragVal)
        gravity.append(gravityVal)

    # Technically just calculated the diagonal displacement of the rocket. 
    # We can use some trigonometry to get strictly the vertical displacement (technically negligible, but easy calculation)
    displacement *= math.sin((math.pi / 2) - launchParameters.launchAngle)
    velocity *= math.sin((math.pi / 2) - launchParameters.launchAngle)
    acceleration = np.array(acceleration) * math.sin((math.pi / 2) - launchParameters.launchAngle)
    
    # 1) Acceleration, velocity, displacement 
    plt.figure(1)

    plt.subplot(1, 3, 1)
    plt.plot(tPlot, displacement, label = 'Displacement')
    plt.ylabel ("Displacement [m]")
    plt.xlabel("Time [s]")
    plt.title('Displacement')

    plt.subplot(1, 3, 2)
    plt.plot(tPlot, velocity, label = 'Velocity')
    plt.xlabel("Time [s]")
    plt.ylabel("Velocity [m/s]")
    plt.title('Velocity')

    plt.subplot(1, 3, 3)
    plt.plot(tPlot, acceleration, label = 'Acceleration')
    plt.xlabel("Time [s]")
    plt.ylabel("Acceleration [m/s^2]")
    plt.title('Acceleration')

    # 2) Forces 

    plt.figure(2)

    plt.subplot(1, 3, 1)
    plt.plot(tPlot, thrust, label = 'Thrust')
    plt.xlabel("Time [s]")
    plt.ylabel("Thrust [N]")
    plt.title('Thrust')

    plt.subplot(1, 3, 2)
    plt.plot(tPlot, drag, label = 'Drag')
    plt.xlabel("Time [s]")
    plt.ylabel("Drag [N]")
    plt.title('Drag')

    plt.subplot(1, 3, 3)
    plt.plot(tPlot, gravity, label = 'Gravity')
    plt.xlabel("Time [s]")
    plt.ylabel("Gravity [N]")
    plt.title('Gravity')

    plt.figure(3) 
    plt.plot(tPlot, rocketMass, label = "Rocket Mass")
    plt.xlabel("Time [s]")
    plt.ylabel("Rocket Mass [kg]")
    plt.title("Rocket Mass Over Time")

    plt.show()

    print("Apogee predicted at ", max(displacement), " m")
    print("Max velocity = ", max(velocity), " m/s")
    print("Max acceleration = ", max(acceleration), "m/s^2")

main()
    



    

    
