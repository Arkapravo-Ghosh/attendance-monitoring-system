#!/bin/python3
import mariadb as connector
import time
import sys
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
database = "attendance"

if "-h" not in sys.argv and "--help" not in sys.argv:
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
    args = sys.argv
    if "-h" in args or "--help" in args:
        print(
            f"""Usage: {args[0]} [OPTIONS] [ARGS]
Options:
    -h, --help\t\t\tShow this help message
    -d, --date\t\t\tDate of attendance (dd_mm_yyyy)
    -n, --student-name\t\tStudent name
    -r, --roll\t\t\tRoll number
    -c, --class\t\t\tClass
    -p, --period\t\tPeriod"""
        )
        exit(0)

    if "-d" not in args and "--date" not in sys.argv:
        date = get_date()
    else:
        if "-d" in args:
            date = args[args.index("-d") + 1]
        elif "--date" in args:
            date = args[args.index("--date") + 1]
    if "-n" in args or "--student-name" in args:
        if "-n" in args:
            name = args[args.index("-n") + 1]
        elif "--student-name" in args:
            name = args[args.index("--student-name") + 1]
    else:
        print("Error: Student name not specified")
        exit(1)
    if "-r" in args or "--roll" in args:
        if "-r" in args:
            roll = args[args.index("-r") + 1]
        elif "--roll" in args:
            roll = args[args.index("--roll") + 1]
    else:
        print("Error: Roll number not specified")
        exit(1)
    if "-c" in args or "--class" in args:
        if "-c" in args:
            class_ = args[args.index("-c") + 1]
        elif "--class" in args:
            class_ = args[args.index("--class") + 1]
    else:
        print("Error: Class not specified")
        exit(1)
    if "-p" in args or "--period" in args:
        if "-p" in args:
            period = args[args.index("-p") + 1]
        elif "--period" in args:
            period = args[args.index("--period") + 1]
    else:
        print("Error: Period not specified")
        exit(1)

    query = f"SELECT * FROM information_schema.tables WHERE table_name = '{date}'"
    if execute(query) == []:
        query = f"CREATE TABLE {date} (class VARCHAR(10) NOT NULL, roll INT NOT NULL, period INT NOT NULL, name VARCHAR(50) NOT NULL, PRIMARY KEY (class, roll, period))"
        execute(query)
    query = f"SELECT * FROM {date} WHERE class = '{class_}' AND roll = {roll} AND period = {period} AND name = '{name}'"
    exc = execute(query)
    if exc != []:
        print("Student already present")
    else:
        query = f"INSERT INTO {date} (class, roll, period, name) VALUES ('{class_}', {roll}, {period}, '{name}')"
        try:
            execute(query)
        except connector.IntegrityError:
            print("IntegrityError: Check the fields properly")
            exit(1)
        print("Student added to attendance")


if __name__ == "__main__":
    main()