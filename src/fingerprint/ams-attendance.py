#!/bin/python3
import os
import time
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1

try:
    import mariadb as connector
except ImportError:
    import mysql.connector as connector
import RPi.GPIO as GPIO

buzzer = 16
wait = 0.1
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buzzer, GPIO.OUT)

host = "localhost"
user = "attendance"
if os.name == "nt":
    try:
        with open(r"C:\ams\mysqlpasswd.txt", "r") as f:
            passwd = f.read()
    except FileNotFoundError:
        print(r"Error: C:\ams\mysqlpasswd.txt not found")
        exit(1)
elif os.name == "posix":
    try:
        with open("/etc/ams/mysqlpasswd.txt", "r") as f:
            passwd = f.read()
    except FileNotFoundError:
        print("Error: /etc/ams/mysqlpasswd.txt not found")
        exit(1)
passwd = passwd.strip()
database = "attendance"
try:
    cnx = connector.connect(
        host=host, user=user, passwd=passwd, database=database, autocommit=True
    )
except connector.OperationalError:
    print("Error connecting to Database")
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
        exit(0)

    GPIO.output(buzzer, GPIO.HIGH)
    time.sleep(wait)
    GPIO.output(buzzer, GPIO.LOW)
    GPIO.cleanup()

    f.loadTemplate(positionNumber, FINGERPRINT_CHARBUFFER1)

except Exception as e:
    print("Operation failed!")
    print("Exception message: " + str(e))
    exit(1)

query = f"SELECT name, class, roll FROM student_data WHERE position = {positionNumber}"
try:
    result = execute(query)
except connector.ProgrammingError:
    print("Error executing query")
    exit(1)

name = result[0][0]
class_ = result[0][1]
roll = result[0][2]

now = time.localtime()
hour = now.tm_hour
minute = now.tm_min

period = 0
if hour == 9:
    if minute >= 30:
        period = 1
elif hour == 10:
    if minute <= 25:
        period = 1
    elif minute >= 30:
        period = 2
elif hour == 11:
    if minute <= 25:
        period = 2
    elif minute >= 30:
        period = 3
elif hour == 12:
    if minute <= 25:
        period = 3
elif hour == 13:
    if minute >= 20:
        period = 4
elif hour == 14:
    if minute <= 15:
        period = 4
    elif minute >= 20:
        period = 5
elif hour == 15:
    if minute <= 15:
        period = 5
    elif minute >= 20:
        period = 6
elif hour == 16:
    if minute <= 15:
        period = 6

backend = "/opt/attendance-monitoring-system/src/server/ams-backend.py"
try:
    os.system(f'{backend} -n "{name}" -c {class_} -r {roll} -p {period}')
except FileNotFoundError:
    print(f"Error: {backend} not found")
    exit(1)
