#ADSC Power and State Second by second

#SLEEP_STATE
SLEEP_STATE = 0
SLEEP_POWERDRAW = 0
SLEEP_TIME = 0

#DETUMBLING_STATE
DETUMBLING_STATE = 1
DETUMBLING_STATE_POWER = 100   #assumption
DETUMBLING_STATE_TIME = 10    #assumption

#COURSE_STATE
COURSE_STATE = 2
COURSE_STATE_POWER = 200       #assumption
COURSE_STATE_DURATION = 10000000    #ALWAYS

#PICTURE_STATE
PICTURE_STATE = 3
PICTURE_STATE_POWER = 500    #assumption
PICTURE_STATE_DURATION = 100    #assumption


#need initial define in main function
ADSC_STATE = SLEEP_STATE
FIRST_TIME = 1

#global variable
CDH_TAKE_PHOTO = 0
CDH_TURN_ON = 0
CDH_TAKE_PHOTO_FINISH = 0
SYSTEM_TIME = 0
ADSC_POWER = 0
ADSC_STATE = 0

#Main function is to simulate the ADSC_POWER_COMSUPTION function
def main():
    global ADSC_STATE, SLEEP_STATE, SYSTEM_TIME, ADSC_POWER, CDH_TURN_ON, CDH_TAKE_PHOTO, CDH_TAKE_PHOTO_FINISH
    ADSC_STATE = SLEEP_STATE
    for SYSTEM_TIME in range (0, 100):
        ADSC_POWER_COMSUPTION(SYSTEM_TIME)
        print ("ADSC Power comsumed: %d mJ"   % ADSC_POWER)
#at 5 second, turn on the ADSC
        if SYSTEM_TIME == 5:
            CDH_TURN_ON = 1
            print ("\nTURN ON ADSC, Start Detumbling")


#wait for the detumbling finish and at 40s, receive the take picture commond
        if SYSTEM_TIME == 40:
            CDH_TAKE_PHOTO_FINISH = 0
            CDH_TAKE_PHOTO = 1
            print ("\nTake Photo Now")

#at 80s, finish taking picture, go back to the course state
        if SYSTEM_TIME == 80:
            CDH_TAKE_PHOTO = 0
            CDH_TAKE_PHOTO_FINISH = 1
            print ("\nFinish Take Photo, Move to Course")

    print ("\n \nMission Finish!   The Total Power in ADSC is %d mW"  % ADSC_POWER)






def ADSC_POWER_COMSUPTION (SYSTEM_TIME):
    t0 = 0
#Sleep state
    global SLEEP_STATE, DETUMBLING_STATE, CDH_TURN_ON, FIRST_TIME, COURSE_STATE, ADSC_POWER, DETUMBLING_STATE_POWER, ADSC_STATE, PICTURE_STATE, CDH_TAKE_PHOTO_FINISH, CDH_TAKE_PHOTO

    if ADSC_STATE == SLEEP_STATE:
        # DO NOTHING
        if CDH_TURN_ON == 1:
            ADSC_STATE = DETUMBLING_STATE


#detumbling state
    if ADSC_STATE == DETUMBLING_STATE:
    # DO SOMETHING NOT SURE
        if FIRST_TIME == 1:
            t0 = SYSTEM_TIME
            FIRST_TIME = 0

        if SYSTEM_TIME >= DETUMBLING_STATE_TIME+t0:
            ADSC_STATE = COURSE_STATE
            FIRST_TIME = 1
            print ("\nFinish Detumbling, Move to Course")
        ADSC_POWER = ADSC_POWER + DETUMBLING_STATE_POWER     #accumulate ADSC power second by second



#course state
    if ADSC_STATE == COURSE_STATE:
    # DO SOMETHING NOT SURE

        if CDH_TAKE_PHOTO == 1:
            ADSC_STATE = PICTURE_STATE

        ADSC_POWER = ADSC_POWER + COURSE_STATE_POWER



#picture state
    if ADSC_STATE == PICTURE_STATE:
    #DO SOMETHING NOT SURE

        if CDH_TAKE_PHOTO_FINISH == 1:
            ADSC_STATE = COURSE_STATE

        ADSC_POWER = ADSC_POWER + PICTURE_STATE_POWER



main()
