#Variables named something_time denote the time at which the action is started
#Variables named something_duration denote the duration of the action
#Eg. TAKE_PHOTO_TIMES = 150 means to take a photo 150 seconds into the simulation and DETUMBLE_DURATION = 20 means that it takes 20 seconds to detumble

import Payload_Constants as PAYLOAD
import Flags,sys, random,math
import COMMS_data as COMMS
import CDH_Modes as CDH
import ADCS_Power_sequence as ADCS


SIMULATION_DURATION =3600*24    #One full orbit is 5400 seconds
TAKE_PHOTO_TIMES = []       #Takes a photo at simTime == TAKE_PHOTO_TIMES seconds (eg 400 seconds into simulation)
TRANSMIT_TIMES = []     #Time at which the photo is downlinked to earth.
NUMBER_OF_PHOTOS = 16
SLEEP_OUT_TIME = 100     #Time at which the Cubesat is awoken from orbital deployment state
PAYLOAD_BOOT_TIMES = []     #Place holder array used to store calculated values
#Calculates the total power consumed per second
#Loads the power for every second into unique subsystem lists with every second being an indiviudal element in the list
def main():
    #subsystem lists
    CDH_CONSUMPTION=[]
    COMMS_CONSUMPTION=[]
    PAYLOAD_CONSUMPTION=[]
    ADCS_CONSUMPTION=[]
    inputSanityCheck()
    transmission()    #Sets the values that a transmission from ground control would set
    #Simulates mission time by incrementing a variable every loop, where one loop is one mission second
    with open("PowerConsumption.txt", "w") as text_file:
        print("    COMMS     CDH     PAYLOAD     ADCS",file=text_file)
        for simTime in range(SIMULATION_DURATION):              #One Orbit
            ADCS_power = ADCS.ADCS_power(simTime)       #Calls the ADCS power function and stores the vaule in a variable for printing later
            ADCS_CONSUMPTION.append(ADCS_power)     #Stores the variable value in the ADCS list as a new element
            COMMS_power = COMMS.commsPower(simTime)     #Repeats the above steps  for each subsystem
            COMMS_CONSUMPTION.append(COMMS_power)
            CDH_power = CDH.CDHPower(simTime)
            CDH_CONSUMPTION.append(CDH_power)
            PAYLOAD_power = PAYLOAD.PayloadPower(simTime)
            PAYLOAD_CONSUMPTION.append(PAYLOAD_power)
            if(simTime % 60 == 0 and simTime != 0):
                ADCS_power = (sum(ADCS_CONSUMPTION[-60:]))/60
                COMMS_power = (sum(COMMS_CONSUMPTION[-60:]))/60
                CDH_power = (sum(CDH_CONSUMPTION[-60:]))/60
                PAYLOAD_power = (sum(PAYLOAD_CONSUMPTION[-60:]))/60
                print("%d    %d          %d        %d             %d" % (simTime,COMMS_power,CDH_power,PAYLOAD_power,ADCS_power),file=text_file)       #Prints the values for that second in columns in units of millijoules

    Total_Power = sum(CDH_CONSUMPTION) + sum(COMMS_CONSUMPTION) + sum(PAYLOAD_CONSUMPTION) + sum(ADCS_CONSUMPTION) #Sums all elements of every list to compute the total power

    print("Total Power =", Total_Power /1000, "J")             #Total Power, divided by 1000 to change the units to Joules from millijoules
#Sets the values that a transmisson from ground control would
#Flags file is used to share information between the different python source files (Subsystems, etc)
def transmission():
    global SLEEP_OUT_TIME, TAKE_PHOTO_TIMES, TRANSMIT_TIMES, PAYLOAD_BOOT_TIMES

    #if simTime == 0:        #Generates a list of time values that payload should boot at based on the times to take photos at
    for times in TAKE_PHOTO_TIMES:
        boot_time = times - PAYLOAD.TURN_ON_DURATION - PAYLOAD.IDLE_UNTIL_PHOTO_DURATION -1
        PAYLOAD_BOOT_TIMES.append(boot_time)

    Flags.TAKE_PHOTO_TIMES = TAKE_PHOTO_TIMES
    Flags.PAYLOAD_BOOT_TIMES =  PAYLOAD_BOOT_TIMES
    Flags.TRANSMIT_TIMES = TRANSMIT_TIMES
    Flags.SLEEP_OUT_TIME = SLEEP_OUT_TIME


def inputSanityCheck():
    global SLEEP_OUT_TIME, TAKE_PHOTO_TIMES, TRANSMIT_TIMES, PAYLOAD_BOOT_TIMES
    parseData()
    orbit_number = 0
    if len(TAKE_PHOTO_TIMES) != len(TRANSMIT_TIMES):
        print('\x1b[1;37;41m' + "ERROR!" + '\x1b[0m')           #Fancy String management to put a red box around the words in the middle
        print('\x1b[1;37;41m' + "Number of photos and transmits are not equal" + '\x1b[0m')         #Fancy String management to put a red box around the words in the middle
        sys.exit()

    for TAKE_PHOTO_TIME, TRANSMIT_TIME in zip(TAKE_PHOTO_TIMES,TRANSMIT_TIMES):
        orbit_number = orbit_number + 1
        if TRANSMIT_TIME < SLEEP_OUT_TIME or TAKE_PHOTO_TIME < SLEEP_OUT_TIME:
            print('\x1b[1;37;41m' + "ERROR!" + '\x1b[0m')       #Fancy String management to put a red box around the words in the middle
            print('\x1b[1;37;41m' + "TRANSMISSION OR PHOTO SCHEDULED BEFORE AWAKENING" + '\x1b[0m')     #Fancy String management to put a red box around the words in the middle
            print('\x1b[1;37;41m' + "Photo Time %d: " % orbit_number + str(TAKE_PHOTO_TIME) + '\x1b[0m')
            print('\x1b[1;37;41m' + "Transmission Time %d: " % orbit_number + str(TRANSMIT_TIME) + '\x1b[0m')
            sys.exit()
        if TRANSMIT_TIME - TAKE_PHOTO_TIME > 5400:
            print('\x1b[1;37;41m' + "ERROR!" + '\x1b[0m')       #Fancy String management to put a red box around the words in the middle
            print('\x1b[1;37;41m' + "Transmit Time for Photo Time %d is after that orbit completes" % orbit_number + '\x1b[0m')     #Fancy String management to put a red box around the words in the middle
            print('\x1b[1;37;41m' + "Photo Time %d: " % orbit_number + str(TAKE_PHOTO_TIME) + '\x1b[0m')
            print('\x1b[1;37;41m' + "Transmission Time %d: " % orbit_number + str(TRANSMIT_TIME) + '\x1b[0m')
            sys.exit()
        elif TRANSMIT_TIME - TAKE_PHOTO_TIME < 0:
            print('\x1b[1;37;41m' + "ERROR!" + '\x1b[0m')       #Fancy String management to put a red box around the words in the middle
            print('\x1b[1;37;41m' + "Transmit Time %d is before the photo is taken" %(orbit_number) + '\x1b[0m')        #Fancy String management to put a red box around the words in the middle
            print('\x1b[1;37;41m' + "Photo Time %d: " % orbit_number + str(TAKE_PHOTO_TIME) + '\x1b[0m')
            print('\x1b[1;37;41m' + "Transmission Time %d: " % orbit_number + str(TRANSMIT_TIME) + '\x1b[0m')
            sys.exit()
        elif TRANSMIT_TIME - TAKE_PHOTO_TIME < PAYLOAD.PHOTO_TO_CDH_DURATION_MAXIMUM:
            print('\x1b[1;37;41m' + "ERROR!" + '\x1b[0m')       #Fancy String management to put a red box around the words in the middle
            print('\x1b[1;37;41m' + "Transmit Time %d is before the photo has been transfered to CDH" %(orbit_number) +'\x1b[0m')      #Fancy String management to put a red box around the words in the middle
            print('\x1b[1;37;41m' + "Transmission Time should be at least %d seconds after the photo is taken" % PAYLOAD.PHOTO_TO_CDH_DURATION_MAXIMUM + '\x1b[0m')
            print('\x1b[1;37;41m' + "Photo Time %d: " % orbit_number + str(TAKE_PHOTO_TIME) + '\x1b[0m')
            print('\x1b[1;37;41m' + "Transmission Time %d: " % orbit_number + str(TRANSMIT_TIME) + '\x1b[0m')
            sys.exit()
        elif (TAKE_PHOTO_TIME >= SIMULATION_DURATION) or TRANSMIT_TIME >= SIMULATION_DURATION:
            print('\x1b[1;37;41m' + "ERROR!" + '\x1b[0m')       #Fancy String management to put a red box around the words in the middle
            print('\x1b[1;37;41m' + "Transmit Time or photo time %d is outside the simulation duration" %(orbit_number) +'\x1b[0m')      #Fancy String management to put a red box around the words in the middle
            print('\x1b[1;37;41m' + "Simulation duration is %d" % SIMULATION_DURATION + '\x1b[0m')
            print('\x1b[1;37;41m' + "Photo Time %d: " % orbit_number + str(TAKE_PHOTO_TIME) + '\x1b[0m')
            print('\x1b[1;37;41m' + "Transmission Time %d: " % orbit_number + str(TRANSMIT_TIME) + '\x1b[0m')
            
            print("Maximum Number of photos possible: %d" %)
            sys.exit()

def parseData():
    for t in range(NUMBER_OF_PHOTOS):
        if t < 1:
            photo = random.randrange(SLEEP_OUT_TIME, 5400*(t+1) - PAYLOAD.PHOTO_TO_CDH_DURATION_MAXIMUM)
        else:
            photo = random.randrange(5400*t, 5400*(t+1) - PAYLOAD.PHOTO_TO_CDH_DURATION_MAXIMUM)
        TAKE_PHOTO_TIMES.append(photo)
        transmit = random.randrange(photo + PAYLOAD.PHOTO_TO_CDH_DURATION_MAXIMUM, 5400*(t+1))
        TRANSMIT_TIMES.append(transmit)
        print(transmit)


main()
