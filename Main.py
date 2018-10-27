#This is the main
#Created on Oct 10, 2018
#This is the main
import sys
from scratch import scratch
import SingleOrbit as Single_Orbit

def main():
    timeOfPass = 90
    NumOfPass = 5
    powers = []
    scratch(timeOfPass,NumOfPass) #Info of STK is obtained

    TakePhotoTime_Occurances = findOnFile(timeOfPass,NumOfPass)
    TakePhotoTime = TakePhotoTime_Occurances[0]
    Single_Orbit.SingleOrbitSimulation(TakePhotoTime)


#Finds the places where a photo should be taken
def findOnFile(Time,Num):
    occurances = []
    fileA = open("random.txt","r")
    for i in range(0,Time*Num):
        line = fileA.readline()

        if (line[0] == "1"):
            occurances.append(i+1)

    fileA.close()
    return occurances

main()
