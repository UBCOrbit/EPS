import csv
list = []
with open('Solar_Panel_Power.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        list.append(float(row['Power (W)']))

power_generated=(list[5401*6:])

print(sum(power_generated))
