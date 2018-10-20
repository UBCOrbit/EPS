# Units are in milliWatt
# Time is in seconds

# States
COMMSTRANSMIT = 0
COMMSSLEEP = 1
COMMSIDLE = 0
SLEEPOUT = 0

state_timer = 0

# Idle waiting for
idle_state = 1
idle_power_max = 540
idle_power_typical = 298
idle_time = 90 * 60 - 90  # For all time except for 90s transmission

# Sleep during launch
sleep_power = 0

# Transmit Picture
transmit_time = 90
transmit_power = 3410  # Max and typical are similar values


def commsPower():
    global COMMSTRANSMIT
    global COMMSSLEEP
    global COMMSIDLE
    global SLEEPOUT

    global state_timer

    if COMMSSLEEP == 1 and Sleep_out == 1:
        COMMS_sleep = 0
        COMMS_idle = 1

    elif COMMS_transmit == 1 and state_timer >= transmit_time:
        COMMSTRANSMIT = 0
        COMMSIDLE = 1
        state_timer = 0

    state_timer += 1

    if COMMSTRANSMIT:
        return transmit_power

    elif COMMSSLEEP:
        return sleep_power

    elif COMMSIDLE:
        return idle_power_typical
