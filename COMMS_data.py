# Units are in milliWatt
# Time is in seconds

import Flags

# States(3 states):  sleep, idle, transmit
state = 'sleep'
state_timer = -1

# Idle waiting for
idle_power_max = 540
idle_power_typical = 298
idle_time = 90 * 60 - 90  # For all time except for 90s transmission

# Sleep during launch
sleep_power = 0

# Transmit Picture
transmit_duration = 90
transmit_power = 3410  # Max and typical are similar values

#This is the main function, it calls the statemachine updating function, SetFlags, and then returns a power consumption value depending on what the state is
def commsPower(sysTime):
    global state

    setFlags(sysTime)

    #Reads the state and returns the power draw accordingly
    if(state == 'transmitting'):
        return transmit_power
    elif(state == 'sleep'):
        return sleep_power
    elif(state == 'idle'):
        return idle_power_typical

#This is the statemachine update function
def setFlags(sysTime):
    global transmit_duration, state_timer, state

    #This sets a flag when the system starts to transmit and increments it every loop after that
    if(Flags.COMMS_TRANSMIT == 1 and state_timer == -1):
        state_timer = 0
    elif(state_timer != -1):
        state_timer = state_timer + 1

    #This drives the statemachine
    if state == 'sleep' and Flags.SLEEP_OUT == 1:       #'Wakes' the comms system when the sleep out flag is set to one
        state = 'idle'
    elif (Flags.COMMS_TRANSMIT == 1) and (state_timer >= transmit_duration):        #Checks to see how long comms has been transmitting and finishes the transmission if its been long enough
        Flags.COMMS_TRANSMIT = 0
        state_timer = -1        #resets the state_timer varaible to prepare it for another transmission
        state = 'idle'
    elif (Flags.COMMS_TRANSMIT == 1) and (state == 'idle'):
        state = 'transmitting'
