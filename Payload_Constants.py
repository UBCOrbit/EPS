#POWER DRAW untits are milliwatts
#Duration units are seconds
import Flags


#POWER_OFF_STATE
POWER_OFF_POWERDRAW = 0
POWER_OFF_DURATION = 0

#TURN_ON_STATE
TURN_ON_POWERDRAW = 1000
TURN_ON_DURATION = 30

#IDLE_UNTIL_PHOTO_STATE
IDLE_UNTIL_PHOTO_POWERDRAW = 500
IDLE_UNTIL_PHOTO_DURATION = 120  #ASSUMED VALUE

#TAKE_PHOTO_STATE
TAKE_PHOTO_POWERDRAW = 1000
TAKE_PHOTO_DURATION = 1

#PHOTO_TO_CDH_STATE
PHOTO_TO_CDH_POWERDRAW = 500
PHOTO_TO_CDH_DURATION_MINIMUM = 90 #SEMI-ASSUMED VALUE
PHOTO_TO_CDH_DURATION_MAXIMUM = 180 #SEMI-ASSUMED VALUE

#TURN_OFF_STATE
TURN_OFF_POWERDRAW = 1000
TURN_OFF_DURATION = 5

#Sets the start time of the payload to an out of bounds number so it can be set in the code
payload_start_time = -1
state = 'off'

#This is the main function, it calls the statemachine updating function, SetFlags, and then returns a power consumption value depending on what the state is
def PayloadPower(sysTime):
    global payload_start_time, state
    SetFlags(sysTime)

    #Reads the state and returns the power draw accordingly
    if(Flags.SLEEP_OUT == 0):
        return POWER_OFF_POWERDRAW
    elif(state == 'booting'):
        return (TURN_ON_POWERDRAW)
    elif(state == 'idling until photo'):
        return (IDLE_UNTIL_PHOTO_POWERDRAW)
    elif(state =='taking photo'):
        return (TAKE_PHOTO_POWERDRAW)
    elif(state == 'transfering photo to cdh'):
        return (PHOTO_TO_CDH_POWERDRAW)
    elif(state == 'shutting down'):
        return (TURN_OFF_POWERDRAW)
    else:
        return (POWER_OFF_POWERDRAW)

#This is the statemachine update function
def SetFlags(sysTime):
    global payload_start_time, state

    #This sets a flag the frist time it's called so it knows how long it's been 'running' for
    if(payload_start_time == -1 and Flags.PAYLOAD_BOOT == 1):
        payload_start_time = sysTime

    #This checks the payload boot flag and sets the state accordingly
    if(Flags.PAYLOAD_BOOT == 0):
        state = 'off'
    elif(sysTime <= payload_start_time + TURN_ON_DURATION):       #If the system time is less than the time it takes to turn on, it sets the state to booting
        state = 'booting'
    elif(sysTime <= payload_start_time + TURN_ON_DURATION + IDLE_UNTIL_PHOTO_DURATION):       #just adds the times up and sets the state accordingly
        state = 'idling until photo'
    elif(sysTime <= payload_start_time + TURN_ON_DURATION + IDLE_UNTIL_PHOTO_DURATION + TAKE_PHOTO_DURATION):
        state ='taking photo'
    elif(sysTime <= payload_start_time + TURN_ON_DURATION + IDLE_UNTIL_PHOTO_DURATION + TAKE_PHOTO_DURATION + PHOTO_TO_CDH_DURATION_MAXIMUM):
        state = 'transfering photo to cdh'
        Flags.photo_taken_flag = 1      #sets a global flag to let the other subsystems know when it has taken a photo
    elif(sysTime <= payload_start_time + TURN_ON_DURATION + IDLE_UNTIL_PHOTO_DURATION + TAKE_PHOTO_DURATION + PHOTO_TO_CDH_DURATION_MAXIMUM + TURN_OFF_DURATION):
        state = 'shutting down'
    else:
        Flags.PAYLOAD_BOOT = 0          #Does some clean up with the flags
        Flags.photo_taken_flag = 0
        payload_start_time = -1
        state = 'off'
