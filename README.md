# UBC-Orbit---EPS

Welcome to EPS Github

This contains files for different subsystem and a main that helps us create a file containing power simulation information

This program simulates the power consumption of a cubesat for every second for an arbitaray amount of time, photos taken and transmissions made


Each subsystem is in its own file and they all share information with each other through the Flags.py file. The MultipleOrbits.py file currently runs the simulation with the timings specified in the variable declarations at the top of the file.

Each subsystem file is broken down into two parts, the statemachine function, called `SetFlags(sysTime)` to update it through its various states and a power calculation function, `PayloadPower(sysTime)` which returns a value for the power consumed by the subsystem in that second based on what state it is in.  

The main loop in MultipleOrbits.py calls the statemachine update function and then the power consumption calculation function of each subsystem in an arbitrary order. It then appends these values to a unique list for each subsystem and prints these lists to a text file called PowerConsumption.txt. It also performs some input sanity checks to ensure valid input data and will output error messages if they fail


# Style guidelines

All variables have an 'underscore' in them and no capital letters. e.g., space_variable or counter_

All global variables are declared as capital letters. e.g., GLOBAL_VARIABLE

All functions have the first letter non-capital and no space. e.g., isTrue()
