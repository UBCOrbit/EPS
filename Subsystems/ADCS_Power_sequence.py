#ADCS Power and State Second by second
from Subsystems import Flags

#SLEEP_STATE
SLEEP_STATE = 0

#DETUMBLING_STATE (detumble after cubesat awakes from orbital deployment state )
DETUMBLING_STATE = 1
DETUMBLING_STATE_POWER = 1200       #assumption
DETUMBLING_STATE_DURATION = 50      #assumption

#COURSE_STATE (maintains correct course in orbit)
COURSE_STATE = 2
COURSE_STATE_POWER = 150            #assumption
COURSE_STATE_DURATION = 10000000    #ALWAYS

#PICTURE_STATE (Gets set When Payload turns on)
PICTURE_STATE = 3
PICTURE_STATE_POWER = 500           #assumption
PICTURE_STATE_DURATION = 100        #assumption

#need initial define in main function
ADCS_STATE = SLEEP_STATE

#global variable
CDH_TURN_ON = 0                    #Is set to 1 when SLEEP_OUT is set to 1 (at time when exiting orbital deployment state.)
ADCS_POWER = 0                     #Is set to different values deppending on ADCS state. (DETUMBLING_STATE_POWER, COURSE_STATE_POWER, PICTURE_STATE_POWER)
ADCS_STATE = 0
ADCS_start_time = -1

#Function calls ADCS_Power_consumption function and return power per second to main(singleOrbit.py)
def ADCS_power(sysTime):
    global ADCS_POWER, CDH_TURN_ON, ADCS_start_time

    if(Flags.SLEEP_OUT == 0):              #Checking if Cubesat is in orbital deployment state. If so, output power = 0.
        return 0
    if(ADCS_start_time == -1):
        ADCS_start_time = sysTime          #Save ADCS Start Time in simulation
    ADCS_POWER_COMSUPTION(sysTime)

#Turn on CDH when cubesat awakes from orbital deployment state
    if Flags.SLEEP_OUT == 1:
        CDH_TURN_ON = 1


    return ADCS_POWER  #Returns ADCS Power consumtion to main(singleOrbit.py)


#ADCS Power Consumptiosns for different states
def ADCS_POWER_COMSUPTION (sysTime):
#Sleep State to Detumbling State
    global SLEEP_STATE, DETUMBLING_STATE, CDH_TURN_ON, COURSE_STATE, ADCS_POWER, DETUMBLING_STATE_POWER, ADCS_STATE, PICTURE_STATE,ADCS_start_time
    if ADCS_STATE == SLEEP_STATE:              #Checking if ADCS is in sleep state. If yes, do nothing.
        # DO NOTHING
        if CDH_TURN_ON == 1:                   #Checking if CDH is on. If yes, set ADCS State to detumbling state. This if is only checked if ADCS was previously in sleep state.
            ADCS_STATE = DETUMBLING_STATE

#Detumbling State to Course State
    if ADCS_STATE == DETUMBLING_STATE:         #Checking if cubesat is in detumbling state.
        if sysTime > DETUMBLING_STATE_DURATION + ADCS_start_time :   #Chekcing when to change ADCS state to course state. It waits until cubesat is done detumbling
            ADCS_STATE = COURSE_STATE
        ADCS_POWER = DETUMBLING_STATE_POWER    #Sets ADCS power to detumbling power consumption per second.

#Course State to Picture State
    if ADCS_STATE == COURSE_STATE:             #Checking if CubeSat is in Course state.
        if Flags.PAYLOAD_BOOT == 1 and Flags.photo_taken_flag == 0:   #When payload turns on, ADCS goes into picture state to position cubesat for photo
            ADCS_STATE = PICTURE_STATE
        ADCS_POWER = COURSE_STATE_POWER        #Sets ADCS power to course state power consumption per second.

#Picture State to Course State
    if ADCS_STATE == PICTURE_STATE:            #Checking if CubeSat is in Picture state.
        if Flags.photo_taken_flag == 1:        #When Payload takes photo, ADCS goes back to course state.
            ADCS_STATE = COURSE_STATE
        ADCS_POWER =  PICTURE_STATE_POWER      #Sets ADCS power to picture state power consumption per second.
