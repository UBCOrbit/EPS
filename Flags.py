takePhotoFlag = 0
Recieve_Flag_Comm = 1
FLAG_Turn_ON_Payload = 0
Flag_Signal_ADCS = 0
FLAG_Receive_PayLoad =0
Flag_Signal_COMMS= 0
Flag_Latch_Up =0

# COMMS
COMMSTRANSMIT = 0
COMMSSLEEP = 1
COMMSIDLE= 0

#General
SLEEPOUT = 0; # For signal turn on

#ADSC
#Flags needed to be Pased through other system
CDH_TAKE_PHOTO = 0
CDH_TURN_ON = 0
CDH_TAKE_PHOTO_FINISH = 0
ADSC_POWER = 0

#Global Variables which only used by ADSC
SLEEP_STATE = 0
SLEEP_POWERDRAW = 0
SLEEP_TIME = 0

DETUMBLING_STATE = 1
DETUMBLING_STATE_POWER = 100   #assumption
DETUMBLING_STATE_TIME = 10    #assumption

COURSE_STATE = 2
COURSE_STATE_POWER = 200       #assumption

PICTURE_STATE = 3
PICTURE_STATE_POWER = 500    #assumption

ADSC_STATE = 0
FIRST_TIME = 1              #use it in Detumbling state to calculate the power
