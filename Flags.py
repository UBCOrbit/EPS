photo_taken_flag = 0         #Is set to 1 when payload has taken the photo
PAYLOAD_BOOT = 0             #Is set to 1 when payload needs to begin the boot in order to be ready for the photo time

Photo_in_CDH = 0             #Is set to 1 when CDH has finished downloading the photo from payload
transmission_begun = 0       #Is set to 1 when the Cubesat has begun downlinking

Recieve_Flag_Comm = 1        #Is set to 1 when the Cubesat receives a transmisson from ground control, currently defaults to immediately after awakening
Flag_Latch_Up =0             #Is set to 1 when a latchup event occurs

# COMMS (Under normal operation either transmitting or idling)
COMMS_TRANSMIT = 0          #Is set to 1 when COMMS is actively downlinking to earth   

#General
SLEEP_OUT = 0;              #Is set to 1 to exit orbital deployment state. Will begin booting and detumbling procedures

#Tranmission settable parameters
TRANSMIT_TIME = 0          #We set this at time which the photo is downlinked to earth. (Can set this in SingleOrbit.py)
SLEEP_OUT_TIME = 0         #We set this at time which the Cubesat exists orbital deployment state. (Can set this in SingleOrbit.py)
TAKE_PHOTO_TIME = 0        #We set this at time which "simTime" takes a photo (Can set this in SingleOrbit.py)
