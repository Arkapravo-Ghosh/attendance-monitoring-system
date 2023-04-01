#!/usr/bin/env python
import os
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
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
    accuracyScore = result[1]

    if positionNumber == -1:
        print("No match found!")
        exit(0)
    else:
        print("Found template at position #" + str(positionNumber))
        if f.deleteTemplate(positionNumber) == True:
            print("Template deleted!")

except Exception as e:
    print("Operation failed!")
    print("Exception message: " + str(e))
    exit(1)

query = f"DELETE FROM student_data WHERE position = '{positionNumber}'"
print(query)
try:
    execute(query)
    print("Deleted from database")
except connector.Error as e:
    print(f"Error: {e}")
    exit(1)
