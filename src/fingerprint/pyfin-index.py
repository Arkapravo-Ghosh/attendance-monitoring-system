#!/usr/bin/env python
from pyfingerprint.pyfingerprint import PyFingerprint


## Shows the template index table


## Tries to initialize the sensor
try:
    f = PyFingerprint("/dev/ttyUSB0", 57600, 0xFFFFFFFF, 0x00000000)

    if f.verifyPassword() == False:
        raise ValueError("The given fingerprint sensor password is wrong!")

except Exception as e:
    print("The fingerprint sensor could not be initialized!")
    print("Exception message: " + str(e))
    exit(1)

## Gets some sensor information
print(
    "Currently used templates: "
    + str(f.getTemplateCount())
    + "/"
    + str(f.getStorageCapacity())
)

## Tries to show a template index table page
try:
    page = input("Please enter the index page (0, 1, 2, 3) you want to see: ")
    page = int(page)

    tableIndex = f.getTemplateIndex(page)

    for i in range(0, len(tableIndex)):
        print("Template at position #" + str(i) + " is used: " + str(tableIndex[i]))

except Exception as e:
    print("Operation failed!")
    print("Exception message: " + str(e))
    exit(1)
