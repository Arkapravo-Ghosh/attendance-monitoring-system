#!/bin/python3
import os
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1

try:
    import mariadb as connector
except ImportError:
    import mysql.connector as connector
import RPi.GPIO as GPIO
import time

buzzer = 16
wait = 0.1
try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buzzer, GPIO.OUT)
except RuntimeError:
    pass

host = "localhost"
user = "attendance"
try:
    with open("/etc/ams/mysqlpasswd.txt", "r") as f:
        passwd = f.read()
except FileNotFoundError:
    print("Error: /etc/ams/mysqlpasswd.txt not found")
    try:
        GPIO.cleanup()
    except RuntimeError:
        pass
    exit(1)
passwd = passwd.strip()
database = "attendance"
try:
    cnx = connector.connect(
        host=host, user=user, passwd=passwd, database=database, autocommit=True
    )
except connector.OperationalError:
    print("Error connecting to Database")
    try:
        GPIO.cleanup()
    except RuntimeError:
        pass
    exit(1)

try:
    cur = cnx.cursor()
except NameError:
    pass


def execute(query):
    cur.execute(query)
    try:
        return cur.fetchall()
    except connector.ProgrammingError:
        return []


try:
    f = PyFingerprint("/dev/ttyUSB0", 57600, 0xFFFFFFFF, 0x00000000)

    if f.verifyPassword() == False:
        raise ValueError("The given fingerprint sensor password is wrong!")

except Exception as e:
    print("The fingerprint sensor could not be initialized!")
    print("Exception message: " + str(e))
    try:
        GPIO.cleanup()
    except RuntimeError:
        pass
    exit(1)

print(
    "Currently used templates: "
    + str(f.getTemplateCount())
    + "/"
    + str(f.getStorageCapacity())
)

try:
    print("Waiting for finger...")

    while f.readImage() == False:
        pass

    f.convertImage(FINGERPRINT_CHARBUFFER1)

    result = f.searchTemplate()

    positionNumber = result[0]
    accuracyScore = result[1]

    if positionNumber == -1:
        print("No match found!")
        try:
            GPIO.cleanup()
        except RuntimeError:
            pass
        exit(0)
    try:
        GPIO.output(buzzer, GPIO.HIGH)
        time.sleep(wait)
        GPIO.output(buzzer, GPIO.LOW)
        GPIO.cleanup()
    except RuntimeError:
        pass

    f.loadTemplate(positionNumber, FINGERPRINT_CHARBUFFER1)

except Exception as e:
    print("Operation failed!")
    print("Exception message: " + str(e))
    try:
        GPIO.cleanup()
    except RuntimeError:
        pass
    exit(1)

query = f"SELECT name, class, roll FROM student_data WHERE position = {positionNumber}"
try:
    result = execute(query)
except connector.ProgrammingError:
    print("Error executing query")
    try:
        GPIO.cleanup()
    except RuntimeError:
        pass
    exit(1)

name = result[0][0]
class_ = result[0][1]
roll = result[0][2]
while True:
    try:
        period = int(input("Enter period: "))
        break
    except ValueError:
        print("Invalid period")
backend = "ams-backend.py"
try:
    os.system(f'{backend} -n "{name}" -c {class_} -r {roll} -p {period}')
except FileNotFoundError:
    print(f"Error: {backend} not found")
    try:
        GPIO.cleanup()
    except RuntimeError:
        pass
    exit(1)
