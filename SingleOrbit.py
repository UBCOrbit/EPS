import Payload_Constants as Payload
import Flags

SECONDS_IN_AN_ORBIT = 5400
#TAKE_PHOTO_TIME = 10
TOTAL_POWER_CONSUMED = 0

#Calculates the total power consumed per second
def SingleOrbitSimulation(TAKE_PHOTO_TIME):
    global TOTAL_POWER_CONSUMED
    for simTime in range(SECONDS_IN_AN_ORBIT):
        SetFlags(simTime,TAKE_PHOTO_TIME)
        #payload
        #ADCS
        TOTAL_POWER_CONSUMED = TOTAL_POWER_CONSUMED + Payload.PayloadPower(simTime)
        printToFile(simTime+1,50.0,30.0,20.0,20.0)
    print("Total Power consumed in Joules: " + str(TOTAL_POWER_CONSUMED/1000))
    return [100,200,500,300]

#Sets the flags for each command at the correct time
def SetFlags(simTime,TAKE_PHOTO_TIME):
    if simTime == TAKE_PHOTO_TIME:
        Flags.takePhotoFlag = 1

def printToFile(Time, CDHPow, PayloadPow, COMMSPow, ADCSPow):
    global file
    if Time == 1:
        file = open("Output.txt","w")
        file.write(" Time \t CDH \t Payload \t COMMS \t ADCS\n")

    file.write(" %3.2lf  %6.2lf  %6.2lf  %6.2lf  %6.2lf \n" %(Time,CDHPow ,PayloadPow,COMMSPow, ADCSPow))
