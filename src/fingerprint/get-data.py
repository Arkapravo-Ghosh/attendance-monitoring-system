#!/usr/bin/env python
from pyfingerprint.pyfingerprint import PyFingerprint
import mariadb as connector
import os

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
    # Get all templates from sensor
    tableIndex = f.getTemplateIndex(0)
    tableIndex = tableIndex + f.getTemplateIndex(1)
    tableIndex = tableIndex + f.getTemplateIndex(2)
    tableIndex = tableIndex + f.getTemplateIndex(3)
    for i in range(0, len(tableIndex)):
        data = f"#{str(i)} {str(tableIndex[i])}"
        if "True" in data:
            try:
                # Search for class name and roll number in database
                query = f'SELECT class, roll, name FROM student_data WHERE position = "{str(i)}"'
                result = execute(query)
                if result:
                    print(
                        f"#{str(i)} is used by {result[0][0]} Roll {result[0][1]}, {result[0][2]}"
                    )
            except Exception as e:
                print("Operation failed!")
                print("Exception message: " + str(e))
                exit(1)

except Exception as e:
    print("Operation failed!")
    print("Exception message: " + str(e))
    exit(1)
