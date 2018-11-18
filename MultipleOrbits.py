#Variables named something_time denote the time at which the action is started
#Variables named something_duration denote the duration of the action
#Eg. TAKE_PHOTO_TIME = 150 means to take a photo 150 seconds into the simulation and DETUMBLE_DURATION = 20 means that it takes 20 seconds to detumble

import Payload_Constants as PAYLOAD
import Flags
import COMMS_data as COMMS
import CDH_Modes as CDH
import ADCS_Power_sequence as ADCS


SIMULATION_DURATION = 86000      #One full orbit is 5400 seconds
TAKE_PHOTO_TIME = [900,6300,11700]       #Takes a photo at simTime == TAKE_PHOTO_TIME seconds (eg 400 seconds into simulation)
TOTAL_POWER_CONSUMED = 0
TRANSMIT_TIME = [1300,6700,12100]     #Time at which the photo is downlinked to earth. Will default to ASAP if this time is set to something before the photo is taken (eg set transmit time to 200 and take photo time to 600, it will transmit as soon as CDH has the photo data)
SLEEP_OUT_TIME = 10     #Time at which the Cubesat is awoken from orbital deployment state
PAYLOAD_BOOT_TIMES = []
#Calculates the total power consumed per second
#Loads the power for every second into unique subsystem lists with every second being an indiviudal element in the list
def main():
    global TOTAL_POWER_CONSUMED
    #subsystem lists
    CDH_CONSUMPTION=[]
    COMMS_CONSUMPTION=[]
    PAYLOAD_CONSUMPTION=[]
    ADCS_CONSUMPTION=[]

    #Simulates mission time by incrementing a variable every loop, where one loop is one mission second
    with open("PowerConsumption.txt", "w") as text_file:
        print("    COMMS     CDH     PAYLOAD     ADCS",file=text_file)
        for simTime in range(SIMULATION_DURATION):              #One Orbit
            transmission(simTime)    #Sets the values that a transmission from ground control would set
            ADCS_power = ADCS.ADCS_power(simTime)       #Calls the ADCS power function and stores the vaule in a variable for printing later
            ADCS_CONSUMPTION.append(ADCS_power)     #Stores the variable value in the ADCS list as a new element
            COMMS_power = COMMS.commsPower(simTime)     #Repeats the above steps  for each subsystem
            COMMS_CONSUMPTION.append(COMMS_power)
            CDH_power = CDH.CDHPower(simTime)
            CDH_CONSUMPTION.append(CDH_power)
            PAYLOAD_power = PAYLOAD.PayloadPower(simTime)
            PAYLOAD_CONSUMPTION.append(PAYLOAD_power)
            print("%d    %d          %d        %d             %d" % (simTime,COMMS_power,CDH_power,PAYLOAD_power,ADCS_power),file=text_file)       #Prints the values for that second in columns in units of millijoules



    Total_Power = sum(CDH_CONSUMPTION) + sum(COMMS_CONSUMPTION) + sum(PAYLOAD_CONSUMPTION) + sum(ADCS_CONSUMPTION) #Sums all elements of every list to compute the total power

    print("Total Power(J) =", Total_Power /1000)             #Total Power, divided by 1000 to change the units to Joules from millijoules

#Sets the values that a transmisson from ground control would
#Flags file is used to share information between the different python source files (Subsystems, etc)
def transmission(simTime):
    global SLEEP_OUT_TIME, TAKE_PHOTO_TIME, TRANSMIT_TIME, PAYLOAD_BOOT_TIMES

    if simTime == 0:        #Generates a list of time values that payload should boot at based on the times to take photos at
        for times in TAKE_PHOTO_TIME:
            boot_time = times - PAYLOAD.TURN_ON_DURATION - PAYLOAD.IDLE_UNTIL_PHOTO_DURATION -1
            PAYLOAD_BOOT_TIMES.append(boot_time)

    Flags.TAKE_PHOTO_TIME = TAKE_PHOTO_TIME
    Flags.PAYLOAD_BOOT_TIMES =  PAYLOAD_BOOT_TIMES
    Flags.TRANSMIT_TIMES = TRANSMIT_TIME
    Flags.SLEEP_OUT_TIME = SLEEP_OUT_TIME


main()
