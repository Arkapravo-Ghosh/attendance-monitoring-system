#!/bin/python3
import time
import os
import http.server

try:
    import mariadb as connector
except ImportError:
    import mysql.connector as connector

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


def get_date():
    return time.strftime("%d_%m_%Y")


def main():
    print(
        """
Please select an option:
1. Manage Student Data
2. Manage Attendance Data
0. Exit
"""
    )
    choice_ams = input("Enter your choice: ")
    if choice_ams == "0":
        print("Exiting...")
        exit(0)
    elif choice_ams == "1":
        print("Manage Student Data")
        print(
            """
1. Add Student
2. Remove Student
3. Verify Student
4. List Students
0. Exit
"""
        )
        choice_s = input("Enter your choice: ")
        if choice_s == "1":
            os.system("sudo systemctl stop ams-attendance")
            os.system("ams-enroll.py")
            os.system("sudo systemctl start ams-attendance")


if __name__ == "__main__":
    print("Welcome to AMS Admin Console")
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Exiting...")
            exit(0)
        except Exception as e:
            print(f"Error: {e}")
            exit(1)
