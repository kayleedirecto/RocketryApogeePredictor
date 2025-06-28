# Rocket Apogee Predictor 

This repository predicts the apogee of a model rocket created for the McMaster Rocketry team. 

## Repository Structure 

```
RecoverySim24-25
├── LC2024Files                 # All files pertaining to Launch Canada 2024 Rocket  
├── ApogeePredictor.py          # The main simulation script! 
├── README.md                   # You're here! 
└── thrustCurve.py              # Supplementary script to obtain thrust curve + mass flow rate info  
```

## Math Overview 


## Algorithm 

The algorithm works in 2 main phases: 

### 1. Numerical integration using an ODE solver

The rocket's position and velocity are computed by solving a system of ordinary differential equations using *scipy.integrate.solve_ivp*: 

$\frac{dx}{dt} = dv$ , $\frac{dv}{dt} = \frac{T(t) - D(v, \rho) - G(m)}{m}$

where, 





## Usage 

As a suggestion, it may be useful to create a folder for each rocket motor simulation, containing the thrust curve file and any other useful info. 

### 1. Create the data file containing the thrust + mass flow rate information (MFR) using the *thrustCurve.py* file

The main apogee simulation requires data on the rocket's thrust and MFR. The script *thrustCurve.py* creates the necessary dataframe containing this information by interpolating thrust curve data and calculating the MFR. 

All variables that need to be changed for each motor can be found in the main function. 

1. To get started, download your rocket motor's thrust curve as a CSV file. This can usually be found on [thrustcurve.org](https://www.thrustcurve.org/). Save the path to this file in the *motorFile* variable. 

2. Change the value of the *Isp* variable to your motor's specific impulse (Isp). This can usualy also be found on [thrustcurve.org](https://www.thrustcurve.org/) or the manufacturer's website. 

3. Change the *fuelMass* variable to the fuel mass of the motor, in kg. This is used as a sanity check to ensure that the calculated MFR of the rocket is accurate. 

4. Adjust the *skipRows* variable based on the number of rows of text that needs to be skipped in the thrust curve file, so only the numerical data points are read. 

5. Change the *savedFileName* variable to the desired file name you would like the thrust curve + MFR info to save to. It is recommended the motor name is in the file name, for organization purposes. 

6. Run the script. 

The *thrustCurve.py* script will interpolate the downloaded thrust curve CSV to generate more thrust data points at smaller time intervals. It will then calculate the MFR at those same time intervals. The integral of the MFR should be within 2% relative error of the fuel mass, otherwise the file will not save, and investigation will be needed. 

### 2. Running the main simulation 

Now you can run the main simulation using *ApogeePredictor.py*! The only things that need to be changed are the rocket and launch parameters class initializations for each rocket launch you would like to simulate, found in the main function of *ApogeePredictor.py*. 

1. Change the rocket class initialization to your rocket's parameters. 

2. Change the launch parameters class initialization to your launch parameters. 

3. Run the simulation. 

The script will output multiple plots: 1) the position, velocity, and acceleration of the rocket over time, 2) the rocket mass over time, and 3) the drag, thrust, and gravity of the rocket over time. The script will also output the apogee prediction, maximum velocity, and maximum acceleration of the rocket flight. 
















