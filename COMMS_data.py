# Units are in milliWatt
# Time is in seconds

#import Flags

# States
COMMS_TRANSMIT = 0
COMMS_SLEEP = 1
COMMS_IDLE = 0
SLEEP_OUT = 0

state_timer = 0

# Idle waiting for
idle_power_max = 540
idle_power_typical = 298
idle_time = 90 * 60 - 90  # For all time except for 90s transmission

# Sleep during launch
sleep_power = 0

# Transmit Picture
transmit_time = 90
transmit_power = 3410  # Max and typical are similar values


def commsPower():
    global COMMS_TRANSMIT
    global COMMS_SLEEP
    global COMMS_IDLE
    global SLEEP_OUT

    global state_timer

    if COMMS_SLEEP == 1 and SLEEP_OUT == 1:
        COMMS_SLEEP = 0
        COMMS_IDLE = 1

    if (COMMS_TRANSMIT == 1) and (state_timer >= transmit_time):
        COMMS_TRANSMIT = 0
        COMMS_IDLE = 1
        state_timer = 0

    if (COMMS_TRANSMIT == 1) and (COMMS_IDLE == 1):
        COMMS_IDLE = 0
        state_timer = 0

    state_timer = state_timer + 1

    if COMMS_TRANSMIT == 1:
        return transmit_power

    elif COMMS_SLEEP == 1:
        return sleep_power

    elif COMMS_IDLE == 1:
        return idle_power_typical


def main():
    global COMMS_TRANSMIT
    global COMMS_SLEEP
    global COMMS_IDLE
    global SLEEP_OUT

    SLEEP_OUT = 1;

    for t in range(0,150):
        if t == 10:
            COMMS_TRANSMIT = 1;

        print(commsPower())
main()
