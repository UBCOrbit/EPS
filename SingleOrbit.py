import Payload_Constants as Payload
import Flags

SECONDS_IN_AN_ORBIT = 5400
TAKE_PHOTO_TIME = 10
TOTAL_POWER_CONSUMED = 0

#Calculates the total power consumed per second
def main():
    global TOTAL_POWER_CONSUMED
    for simTime in range(SECONDS_IN_AN_ORBIT):
        SetFlags(simTime)
        TOTAL_POWER_CONSUMED = TOTAL_POWER_CONSUMED + Payload.PayloadPower(simTime)
    print("Total Power consumed in Joules: " + str(TOTAL_POWER_CONSUMED/1000))

#Sets the flags for each command at the correct time
def SetFlags(simTime):
    if simTime == TAKE_PHOTO_TIME:
        Flags.takePhotoFlag = 1



main()
