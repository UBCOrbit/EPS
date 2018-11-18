TAKE_PHOTO_TIME = [900,6300,11700]
PAYLOAD_BOOT_TIMES = []

for times in TAKE_PHOTO_TIME:
    boot_time = times - 3 - 5 -1
    PAYLOAD_BOOT_TIMES.append(boot_time)

for whaddup in range(0,100000):
    if(whaddup in PAYLOAD_BOOT_TIMES):
        PAYLOAD_BOOT = 1
        print("Hello")
