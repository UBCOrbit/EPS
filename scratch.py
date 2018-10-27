import random

def scratch(maxTime,passes):
    file= open("random.txt","w")

    for s in range(0,passes):
        randTime = random.randint(0,maxTime-1)

        for i in range(0,maxTime):
            rand = random.uniform(0,9)

            if (i == randTime):
                time = 1
            else:
                time = 0

            file.write("%d %lf\n" %(time,rand))
    file.close()

scratch(5,3)
