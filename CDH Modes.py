#CommandDataHandling (CDH) - EPS

#All POWER UNITS IN milliwatts(mW)
#ALL TIME UNITS IN seconds(s)
#Voltage Units in Volts(V)

#PowerRanks(mW) = Current(mA) * Voltage(V)
Voltage = 3.3
PR_1_Max = 840 * Voltage
PR_1_Typical = 400 * Voltage
PR_2_Max = 420 * Voltage
PR_2_Typical = 200 * Voltage
PR_3_Typical = 0.004 * Voltage

#Sleep
Sleep= 0

#After launch Turn on CDH
CDH_Turn_ON = 5                     #Assumed Value
CDH_Turn_ON_Duration = 1            #Assumed Value, 1 sec to turn on

#Periodic Communicaton With Other Sybsystems
COMM_Periodic= 0.00264              #[(4uA/5sec) * 3.3V ] -> Always On
COMM_Periodic_Duration = 5400       # Duration of 1 orbit

#Receiving Commands from Comms

#Recieve_COMM = 1                   #Assumed Value
#Recieve_COMM_Duration = 1          #Assumed Value
Turn_ON_Payload = PR_2_Typical
Turn_ON_Payload_Duration = 1        #Assumed Value

#Signal ADCS
Signal_ADCS = PR_2_Typical
Signal_ADCS_Duration = 1            #Assumed Value

#Signal COMMS to send Picture
Signal_COMMS = PR_2_Typical
Signal_COMMS_Duration = 1           #Assumed Value

#LATCH -> Turn Off then turn ON MCU
Turn_OFFON_MCU = 10                 #Assumed Value
Turn_OFFON_MCU_Duration = 2         #Assumed Value

#IF 1 MCU Dies, all power values 2/3

#MCs are put into low power Mode
MC_Low_Power_Mode = PR_3_Typical


#MAIN Code
CDHstartTime = -1
Recieve_Flag_Comm = 1
FLAG_Turn_ON_Payload = 0
Flag_Signal_ADCS = 0
FLAG_Receive_PayLoad =0
Flag_Signal_COMMS= 0
Flag_Latch_Up =0

def CDHPower(sysTime):
    global CDHstartTime
    global Recieve_Flag_Comm
    global FLAG_Turn_ON_Payload
    global Flag_Signal_ADCS
    global FLAG_Receive_PayLoad
    global Flag_Signal_COMMS
    global Flag_Latch_Up


    if(CDHstartTime == -1):
      CDHstartTime = sysTime
      currentStateTimer = 0
    if(sysTime == 0):
        return (CDH_Turn_ON)

    if(sysTime > 30):                                #Time @ which COMM signals CDH
        if (Recieve_Flag_Comm == 1):
            Recieve_Flag_Comm = 0
            FLAG_Turn_ON_Payload = 1
            Flag_Signal_ADCS = 1

#Add while loop here to simulate time it takes to receive signal from Payload
            FLAG_Receive_PayLoad = 1                #Receive signal from PayLoad
            return(Turn_ON_Payload + Signal_ADCS + COMM_Periodic)

        elif(FLAG_Receive_PayLoad == 1):
            FLAG_Receive_PayLoad =0
            Flag_Signal_COMMS = 1

            Flag_Latch_Up = 0
            return(Signal_COMMS + COMM_Periodic)

        elif(Flag_Latch_Up == 1):
            return(Turn_OFFON_MCU)
        else:
            return(COMM_Periodic)

    return(COMM_Periodic)


def main():
    b=[]
    for t in range(5400):              #One Orbit
        b.append(CDHPower(t))
        print(b[t])

    CDH_Total_Power = sum(b)
    print(CDH_Total_Power)             #Total Power



main()
