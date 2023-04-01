#!/bin/python3
import time
import os
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2
import mariadb as connector

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

    if positionNumber >= 0:
        print("Template already exists at position #" + str(positionNumber))
        exit(0)

    print("Remove finger...")
    time.sleep(2)

    print("Waiting for same finger again...")

    while f.readImage() == False:
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
    exit(1)
print("Data added successfully")
