#!/usr/bin/env python
import time
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2


## Enrolls new finger


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

## Tries to enroll new finger
try:
    print("Waiting for finger...")

    ## Wait that finger is read
    while f.readImage() == False:
        pass

    ## Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(FINGERPRINT_CHARBUFFER1)

    ## Checks if finger is already enrolled
    result = f.searchTemplate()
    positionNumber = result[0]

    if positionNumber >= 0:
        print("Template already exists at position #" + str(positionNumber))
        exit(0)

    print("Remove finger...")
    time.sleep(2)

    print("Waiting for same finger again...")

    ## Wait that finger is read again
    while f.readImage() == False:
        pass

    ## Converts read image to characteristics and stores it in charbuffer 2
    f.convertImage(FINGERPRINT_CHARBUFFER2)

    ## Compares the charbuffers
    if f.compareCharacteristics() == 0:
        raise Exception("Fingers do not match")

    ## Creates a template
    f.createTemplate()

    ## Saves template at new position number
    positionNumber = f.storeTemplate()
    print("Finger enrolled successfully!")
    print("New template position #" + str(positionNumber))

except Exception as e:
    print("Operation failed!")
    print("Exception message: " + str(e))
    exit(1)
