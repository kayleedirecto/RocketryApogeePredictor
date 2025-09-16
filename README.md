# Rocket Apogee Predictor 

This was the simulation I created for the 2024-2025 McMaster Rocketry Team to predict the apogee of our rocket! 

## Repository Structure 

```
RecoverySim24-25
├── LC2024Files                 # All files pertaining to Launch Canada 2024 Rocket  
├── ApogeePredictor.py          # The main simulation script
├── README.md                   # You're here! 
└── thrustCurve.py              # Supplementary script to obtain thrust curve + mass flow rate info  
```

## Math Overview 

This simulation uses a simplified 1D model, considering only the forces in the $z$ (upwards) direction to calculate apogee. We neglect wind, and all other forces acting in the $x$ direction. 

The main forces considered in this simulation are (1) thrust, (2) drag, and (3) gravity. During the simulation, we use the frame of reference such that the thrust and drag act strictly in the $z$ direction, and we only consider the portion of gravity acting in the negative $z$ direction (Gravity_1 in the image below). This simplifies the computation. This technically gives us the diagonal displacement of the rocket, but using simple trigonometry we can then calculate the vertical displacement to determine apogee.  A visual is shown below. 

<img width="200" height="270" alt="Picture1" src="https://github.com/user-attachments/assets/07be708c-449e-4250-a444-507c6549263e" />

<img width="200" height="270" alt="pic2" src="https://github.com/user-attachments/assets/24369458-c6c5-4229-aaf0-357da800c9b9" />

### Thrust Calculation 

The manufacturer of the motor will provide a thrust curve of the rocket, outlining the thrust force applied by the motor to the rocket over time. Using this, we can extrapolate the thrust force at any time, $t$, for our simulation. No math needed. 

### Drag Calculation 

#### Overall Equation 

The force of drag, $F_d$, on the rocket can be described by 

$\quad$ ${F_d = \frac{1}{2} \rho(z) v^2 C_d A}$

where, 

$\quad$ $\rho(z)$ = density of the air [kg m $^{-3}$], as a function of altitude, $z$ [m]

$\quad$ $v$ = velocity of the rocket relative to the air around it [m s $^{-1}$]

$\quad$ $C_d$ = determined coefficient of drag 

$\quad$ $A$ = cross section of rocket, perpendicular to the air flow [m $^2$]

Since we are considering a 1D model, the cross section is taken to be the circular cross section of the rocket. The relative velocity is simply taken to be the velocity of the rocket in the $z$ direction, since we are neglecting wind in the horizontal direction. 

Ongoing research is being done on calculations of the drag coefficient. Commonly used values vary by up to 0.1. For now, we use an average of values obtained using the $OpenRocket$ simulation. 

#### Barometric Formula for Air Density 

Air density, $\rho$ is a function of the altitude, $z$. therefore, this must also be calculated as the simulation progresses. We can calculate the density as a function of altitude using the barometric formula under the International Standard Atmosphere (ISA) model, 

$\quad$ $\rho(z) = \rho_b [\frac{T_b - (z - z_b)L_b}{T_b}]^{(\frac{g_0 M}{R L_b} - 1)}$ 

where, 

$\quad$ $\rho(z)$ = density of the air [kg m $^{-3}$], as a function of altitude, $z$ [m]

$\quad$ $\rho_b$ = Base density, 1.2250 kg m $^{-3}$ at the troposphere 

$\quad$ $T_b$ = Base temperature [K], 2.8815 K at troposphere 

$\quad$ $z$ = Height above sea level [m]

$\quad$ $z_b$ = Base height above sea level [m], 0 m at troposphere 

$\quad$ $L_b$ = Lapse rate at base level [K m $^{-1}$], 0.0065 K m $^{-1}$ at troposphere 

$\quad$ $g_0$ = Standard gravitational acceleration, 9.80665 m s $^{-2}$

$\quad$ $M$ = Molar mass of Earth's air, 0.0289644 kg mol $^{-1}$

$\quad$ $R$ = Universal gas constant, 8.3144598 N m mol $^{-1}$ K $^{-1}$

Note that the ISA model breaks up the earth's atmosphere into layers. Each layer is assigned its own base temperature, base altitude above sea level, base density, and lapse rate. Since model rocketry occurs between 0 and 11 km above mean sea level, we are in the troposphere. This gives us the base values as mentioned above.

### Gravity 

#### Overall Equation 

As mentioned previously, we use the component of gravity opposite to the rocket's direction of flight, i.e. Gravity_1 in the image below. The angle, $\theta$ refers to the launch angle, which will be provided by the competition judges on launch day. 

<img width="220" height="250" alt="pic2" src="https://github.com/user-attachments/assets/810be4de-3ae4-4092-8d6f-2d715efe30a5" />

Therefore, the equation for gravity is

$\quad$ $F_g = \frac{m_{rocket} g_0}{cos\theta}$

where, 

$\quad$ $g_0$ = Standard gravitational acceleration, 9.80665 m s $^{-2}$

$\quad$ $m_{rocket}$ = Mass of rocket, calculated throughout flight [kg]

$\quad$ $\theta$ = Launch angle [rad]

#### Mass Calculation 

As the rocket will continously use fuel throughout the flight, the mass of the rocket will continuously change, and will need to be calculated at each timestep of the simulation. 

Using the rocket motor's thrust curve, we can calculate the mass-flow rate. The mass-flow rate is the mass that flows out of the rocket per unit time. This value allows us to determine the changing mass of the rocket during flight. 

To find the mass-flow rate at an instance in time, we use the thrust given from the thrust curve, along with the specific impulse, $I_{sp}$. The $I_{sp}$ is given by the manufacturer of the motor. 

The mass flow rate is given by 

$\quad$ $\dot{m(t)} = \frac{F_{thrust}(t)}{I_{sp}g_0}$

where, 

$\quad$ $g_0$ = Standard gravitational acceleration, 9.80665 m s $^{-2}$

$\quad$ $I_{sp}$ = Specific impulse, given by the manufacturer [Ns]

$\quad$ $F_{thrust}$ = Thrust force [N], as a function of time, $t$, taken from the thrust curve 

The current mass of the rocket at each timestep can be calculated by, 

$\quad$ $m(t)$ = $DryMass$ + ($WetMass(t-1)$ - $\dot{m(t)} * dt $)

where, 

$\quad$ $m(t)$ = Current mass at time $t$

$\quad$ $DryMass$ = Mass of the rocket, excluding the fuel 

$\quad$ $WetMass(t-1)$ = Mass of the fuel at the previous timestep 

$\quad$ $\dot{m(t)}$ = Mass flow rate at time $t$

$\quad$ $dt$ = Timestep 


## Algorithm 

The algorithm works in 2 main phases: 

### 1. Numerical integration using an ODE solver

The rocket's position and velocity are computed by solving a system of ordinary differential equations using *scipy.integrate.solve_ivp*: 

$\frac{dx}{dt} = v$ , $\frac{dv}{dt} = \frac{F_{thrust}(t) - F_{drag}(t) - F_{gravity}(t)}{m(t)}$

where, 

$\quad$ $F_{thrust}(t)$ = Thrust force at time $t$, obtained from thrust curve data

$\quad$ $F_{drag}(t)$ = Drag force, calculated at each time $t$ 

$\quad$ $F_{gravity}(t)$ = Gravity, calculated at each time $t$

$\quad$ $m(t)$ = Mass, calculated at each time $t$

### 2. Post Processing (Physics Calculated Manually) 

After solving for position and velocity at each timestep using the integrator, these solution values are used to manually calculate the other flight parameters, such as the acceleration. 

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


## Future Work 

Areas for future work include 

#### 1. Implementing a more accurate value for the drag coefficient, $C_d$

Currently an average value obtained using the $OpenRocket$ simulation is hardcoded into the program. Research could be done into the mathematics behind $C_d$ and how this can be implemented into the simulation. Please note, this seems quite involved, and may be a separate project in and of itself. Some reading material: http://ftp.demec.ufpr.br/foguete/bibliografia/TR-11%20AERODYNAMIC%20DRAG%20OF%20MODEL%20ROCKET.pdf

#### 2. Implementing a graphical user interface (GUI) 

Currently, the variables to create the necessary data frame and the variables describing the rocket and launch parameters must be manually changed in each file for each simulation run. Moving forward, it would be ideal to implement a GUI for easier usage, where users can simply input all rocket and launch parameters, run the simulation, then view the resulting plots. 

#### 3. Creating a full trajectory path simulation 

This simulation currently only predicts apogee. Future work should be done in implementing a full trajectory prediction, accounting for drogue parachute and main parachute ejections. This full trajectory calculation would be in 2D, so wind resistance must be taken into account. Ideally, the goal of this simulation would be to have a prediction for the horizontal distance travelled, to know the general radius of where the rocket could have landed for easier recovery. 










