#ADSC Power and State

#SLEEP_STATE
SLEEP_POWERDRAW = 0
SLEEP_TIME = 0

#DETUMBLING_STATE
DETUMBLING_STATE_POWER = 100   #assumption
DETUMBLING_STATE_TIME = 120    #assumption

#COURSE_STATE
COURSE_STATE_POWER = 200       #assumption
COURSE_STATE_DURATION = 10000000    #ALWAYS

#PICTURE_STATE
PICTURE_STATE_POWER = 500    #assumption
PICTURE_STATE_DURATION = 100    #assumption


#need initial define in main function
ADSC_state = SLEEP_STATE
FIRST_TIME = 1

#global variable
 glo CDH_TURN_ON
 glo CDH_TAKE_PHOTO_FINISH
 glo SYSTEM_TIME


#Sleep state
    if(ADSC_state == SLEEP_STATE){
        # DO NOTHING
        if(CDH_TURN_ON == 1){
        ADSC_state = DETUMBLING_STATE
        }
    }

#detumbling state
    if(ADSC_state == DETUMBLING_STATE){
    # DO SOMETHING NOT SURE
        if(FIRST_TIME == 1){
            t0 = SYSTEM_TIME;
            FIRST_TIME = 0
        }
        if(SYSTEM_TIME >= DETUMBLING_STATE_TIME+t0){
        ADSC_state = COURSE_STATE
        ADSC__Detumbling_Power = DETUMBLING_STATE_TIME * DETUMBLING_STATE_POWER
        FIRST_TIME = 1
        }
    }

#course state
    if(ADSC_state == COURSE_STATE){
    # DO SOMETHING NOT SURE
        if(FIRST_TIME == 1){
            t0 = SYSTEM_TIME
            FIRST_TIME = 0
        }

        if(CDH_TAKE_PHOTO == 1){
        ADSC_state = PICTURE_STATE
        ADSC_Course_Power = (SYSTEM_TIME - t0) * COURSE_STATE_POWER
        FIRST_TIME = 1
        }
    }

#picture state
    if(ADSC_state == PICTURE_STATE){
    #DO SOMETHING NOT SURE
        if(FIRST_TIME == 1){
            t0 = SYSTEM_TIME
            FIRST_TIME = 0
        }
        if(CDH_TAKE_PHOTO_FINISH == 1){
        ADSC_state = COURSE_STATE
        ADSC_Picture_Power = (SYSTEM_TIME - t0) * PICTURE_STATE_POWER
        FIRST_TIME = 1
        }
    }
