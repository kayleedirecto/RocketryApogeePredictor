# Rocket Apogee Predictor 

This repository predicts the apogee of a model rocket! 

## Repository Structure 

```
RecoverySim24-25
├── LC2024Files                 # All files pertaining to Launch Canada 2024 Rocket  
├── ApogeePredictor.py          # The main simulation script! 
├── README.md                   # You're here! 
└── thrustCurve.py              # Supplementary script to obtain thrust curve + mass flow rate info  
```

## Math Overview 


## Usage 

As a suggestion, it may be useful to create a folder for each rocket motor, containing the thrust curve file and any other useful info. 

### 1. Create the data file containing the thrust + mass flow rate information (MFR) using the *thrustCurve.py* file

The main simulation requires data on the rocket's thrust and MFR. The script *thrustCurve.py* creates the necessary dataframe containing this information by interpolating thrust curve data and calculating the MFR. 

1. To get started, download your rocket motor's thrust curve as a CSV file. This can usually be found on [thrustcurve.org](https://www.thrustcurve.org/). Save the path to this file in the *motorFile* variable. 

2. Change the value of the *Isp* variable to your motor's specific impulse (Isp). This can usualy also be found on [thrustcurve.org](https://www.thrustcurve.org/) or the manufacturer's website. 

3. Change the *fuelMass* variable to the fuel mass of the motor, in kg. This is used as a sanity check to ensure that the calculated MFR of the rocket is accurate. 

4. Adjust the *skipRows* variable based on the number of rows of text that needs to be skipped in the thrust curve file, so only the numerical data points are read. 

5. Change the *savedFileName* variable to the desired file name you would like the thrust curve + MFR info to save to. It is recommended the motor name is in the file name, for organization purposes. 

6. Run the script. 

The *thrustCurve.py* script will interpolate the downloaded thrust curve CSV to generate more thrust data points at smaller time intervals. It will then calculate the MFR at those same time intervals. The integral of the MFR should be within 2% relative error of the fuel mass, otherwise the file will not save, and investigation will be needed. 

### 2. Running the main simulation 








