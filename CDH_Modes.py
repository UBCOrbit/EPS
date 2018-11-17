
import CDH_Constants as CDH
import Flags
import COMMS_data as COMMS
import Payload_Constants as PAYLOAD
import ADCS_Power_sequence as ADCS
CDHMode = 'inital'
CDHstartTime = -1
#All POWER UNITS IN milliwatts(mW)
#ALL TIME UNITS IN seconds(s)
#Voltage Units in Volts(V)

#Updates the subsystem statemachine/drives the rest of the cubsat since this is CDH
def setflags(sysTime):
    global CDHMode

    #Awakes the cubesat from orbital deployment state
    if sysTime == Flags.SLEEP_OUT_TIME:
            Flags.SLEEP_OUT = 1

    #Begins the downlink of the photo, after checking the photo has be stored in the CDH ram. Will delay transmisson until CDH has finished aquiring the photo if transmission time is set to begin before CDH has the photo
    if sysTime >= Flags.TRANSMIT_TIME and Flags.Photo_in_CDH == 1 and Flags.transmission_begun == 0:
            Flags.COMMS_TRANSMIT = 1
            Flags.transmission_begun = 1

    #Starts the payload boot squence based on how long it takes to boot and how long it is set to idle before taking the photo
    if(sysTime == (Flags.TAKE_PHOTO_TIME - PAYLOAD.TURN_ON_DURATION - PAYLOAD.IDLE_UNTIL_PHOTO_DURATION -1)):
        Flags.PAYLOAD_BOOT = 1

    #Recieves a transmission from ground control, currently set to receive immedately after awakening. Possibly subject to change
    if(Flags.Recieve_Flag_Comm == 1):
        Flags.Recieve_Flag_Comm = 0
        CDHMode = 'receive comms'

    #CDH downloads the photo from payload and stores it in CDH ram for
    elif(Flags.photo_taken_flag == 1 and Flags.Photo_in_CDH != 1):
        if(CDH.Receive_beginning == -1):         #Sets a time so CDH knows how long its been downloading the photo from payload
            CDH.Receive_beginning = sysTime
        CDHMode = 'receive payload'

    #Emulates a Latchup event
    elif(Flags.Flag_Latch_Up == 1):
        CDHMode = 'receive latchup'

    #CDH will operate nominally
    else:
        CDHMode ='idle'
        return


def CDHPower(sysTime):
    global CDHstartTime
    global CDHMode
    setflags(sysTime)

    #Consumes no power if in orbital deployment state
    if(Flags.SLEEP_OUT == 0):
        return 0

    #Will set a variable so that CDH always knows its inital start time
    if(CDHstartTime == -1):
      CDHstartTime = sysTime

    #Will return the power taken to boot CDH for as long as CDH_Turn_ON_Duration is set to
    if(sysTime <  CDHstartTime + CDH.CDH_Turn_ON_Duration ):
        return (CDH.CDH_Turn_ON)

    #Returns the power consumed by CDH while signaling other systems to boot for as long as the durations are set
    if(CDHMode == 'receive comms'): #assuming Turning on payload, and signaling ADCS have same duration
        if(sysTime < CDHstartTime + CDH.CDH_Turn_ON_Duration + CDH.Turn_ON_Payload_Duration):
            return(CDH.Turn_ON_Payload + CDH.Signal_ADCS + CDH.COMM_Periodic)

    #Returns the power consumed by CDH while downloading the photo from payload as long as the durations are set
    elif(CDHMode == 'receive payload'):
        if(sysTime < CDH.Receive_beginning + PAYLOAD.PHOTO_TO_CDH_DURATION_MAXIMUM):
            return(CDH.Signal_COMMS + CDH.COMM_Periodic)
        else:
            Flags.Photo_in_CDH = 1

    #Currently unused function, but is designed to return the power needed to clear a latch up event and power cycle the cubesat
    elif(CDHMode == 'Receive Latchup'):
        if(sysTime < CDHstartTime + CDH.CDH_Turn_ON_Duration + CDH.Turn_ON_Payload_Duration + CDH.Signal_COMMS_Duration+ CDH.Turn_OFFON_MCU_Duration):
            return(CDH.Turn_OFFON_MCU)

    #If CDH is not performing any other specific tasks returns a "idle" power
    return(CDH.COMM_Periodic + CDH.Idle)
