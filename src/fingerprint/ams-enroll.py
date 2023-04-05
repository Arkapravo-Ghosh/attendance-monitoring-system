#!/bin/python3
import time
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2

try:
    import mariadb as connector
except ImportError:
    import mysql.connector as connector
import RPi.GPIO as GPIO

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

    if positionNumber >= 0:
        print("Template already exists at position #" + str(positionNumber))
        try:
            GPIO.cleanup()
        except RuntimeError:
            pass
        exit(0)
    try:
        GPIO.output(buzzer, GPIO.HIGH)
        time.sleep(wait)
        GPIO.output(buzzer, GPIO.LOW)
    except RuntimeError:
        pass
    print("Remove finger...")
    time.sleep(2)

    print("Waiting for same finger again...")

    while f.readImage() == False:
        pass
    try:
        GPIO.output(buzzer, GPIO.HIGH)
        time.sleep(wait)
        GPIO.output(buzzer, GPIO.LOW)
        GPIO.cleanup()
    except RuntimeError:
        pass

    f.convertImage(FINGERPRINT_CHARBUFFER2)

    if f.compareCharacteristics() == 0:
        raise Exception("Fingers do not match")

    f.createTemplate()

    positionNumber = f.storeTemplate()
    print("Finger enrolled successfully!")
    print("New template position #" + str(positionNumber))
    characterics = str(f.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)).encode(
        "utf-8"
    )
    print("SHA-2 hash of template: " + hashlib.sha256(characterics).hexdigest())

except Exception as e:
    print("Operation failed!")
    print("Exception message: " + str(e))
    try:
        GPIO.cleanup()
    except RuntimeError:
        pass
    exit(1)

if execute("SHOW TABLES LIKE 'student_data'") == []:
    execute(
        "CREATE TABLE student_data (position INT NOT NULL, name VARCHAR(50) NOT NULL, class VARCHAR(10) NOT NULL, roll INT NOT NULL, PRIMARY KEY (position, class, roll))"
    )

name = input("Enter name: ")
class_ = input("Enter class: ")
roll = input("Enter roll: ")
try:
    execute(
        f"INSERT INTO student_data VALUES ('{positionNumber}', '{name}', '{class_}', {roll})"
    )
except connector.IntegrityError:
    print("Error: Duplicate entry")
    try:
        GPIO.cleanup()
    except RuntimeError:
        pass
    exit(1)
print("Data added successfully")
