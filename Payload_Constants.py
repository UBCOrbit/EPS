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
payloadstartTime = -1

def PayloadPower(sysTime):
    global payloadstartTime

    if(Flags.takePhotoFlag == 0):
        return 0
    if(payloadstartTime == -1):
        payloadstartTime = sysTime
        currentStateTimer = 0

    if(sysTime <= payloadstartTime + TURN_ON_DURATION):
        return (TURN_ON_POWERDRAW)
    elif(sysTime <= payloadstartTime + TURN_ON_DURATION + IDLE_UNTIL_PHOTO_DURATION):
        return (IDLE_UNTIL_PHOTO_POWERDRAW)
    elif(sysTime <= payloadstartTime + TURN_ON_DURATION + IDLE_UNTIL_PHOTO_DURATION + TAKE_PHOTO_DURATION):
        return (TAKE_PHOTO_POWERDRAW)
    elif(sysTime <= payloadstartTime + TURN_ON_DURATION + IDLE_UNTIL_PHOTO_DURATION + TAKE_PHOTO_DURATION + PHOTO_TO_CDH_DURATION_MAXIMUM):
        return (PHOTO_TO_CDH_POWERDRAW)
    elif(sysTime <= payloadstartTime + TURN_ON_DURATION + IDLE_UNTIL_PHOTO_DURATION + TAKE_PHOTO_DURATION + PHOTO_TO_CDH_DURATION_MAXIMUM + TURN_OFF_DURATION):
        return (TURN_OFF_POWERDRAW)
    else:
        return (POWER_OFF_POWERDRAW)
        takePhotoFlag = 0


def main():
    for t in range(500):
        print(str(PayloadPower(t)))
