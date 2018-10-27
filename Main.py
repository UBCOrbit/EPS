#This is the main
#Created on Oct 10, 2018
#This is the main
import sys

def printToFile(Time, CDHPow, PayloadPow, COMMSPow, ADCSPow):
    global file
    if Time == 1:
        file = open("Output.txt","w")
        file.write("Time \t\t CDH \t Payload \t COMMS \t ADCS\n")

    file.write(" %3d  %6d %6d %6d  %6d \n" %(Time,CDHPow ,PayloadPow,COMMSPow, ADCSPow))
    #file.write(Time CDHPow Payload COMMSPow, ADCSPow)
printToFile(1,3,5,6,8)
printToFile(2,52,36,95,3)
