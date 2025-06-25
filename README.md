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

As a suggestion, it may be useful to create a file for each rocket motor, containing the thrust curve file and any other useful info. 

### 1. Create the data file containing the thrust + mass flow rate information 

The main simulation requires data on the rocket's thrust and mass flow rate. The script ˆthrustCurve.pyˆ creates the necessary dataframe containing this information. 

To get started, download your rocket motor's thrust curve as a CSV file. This can usually be found on thrustcurve.org. These CSV files usual only contain a few thrust data points. To run an accurate simulation, we must interpolate more data points. This is 


### 2. Running the main simulation 






