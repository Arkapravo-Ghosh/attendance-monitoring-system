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

Press Enter to go back
"""
        )
        choice_s = input("Enter your choice: ")
        if choice_s == "":
            pass
        elif choice_s == "0":
            print("Exiting...")
            exit(0)
        elif choice_s == "1":
            os.system("sudo systemctl stop ams-attendance")
            time.sleep(1)
            os.system("ams-enroll.py")
            time.sleep(1)
            os.system("sudo systemctl start ams-attendance")
        elif choice_s == "2":
            os.system("sudo systemctl stop ams-attendance")
            time.sleep(1)
            os.system("ams-delete.py")
            time.sleep(1)
            os.system("sudo systemctl start ams-attendance")
        elif choice_s == "3":
            os.system("sudo systemctl stop ams-attendance")
            time.sleep(1)
            os.system("ams-verify.py")
            time.sleep(1)
            os.system("sudo systemctl start ams-attendance")
        elif choice_s == "4":
            os.system("sudo systemctl stop ams-attendance")
            time.sleep(1)
            os.system("ams-get-data.py")
            time.sleep(1)
            os.system("sudo systemctl start ams-attendance")
        else:
            print("Invalid Choice")
    elif choice_ams == "2":
        print("Manage Attendance Data")
        print(
            """
1. Start Attendance Session
2. Stop Attendance Session
3. Restart Attendance Session
4. View Attendance Data
0. Exit

Press Enter to go back
"""
        )
        choice_a = input("Enter your choice: ")
        if choice_a == "":
            pass
        elif choice_a == "0":
            print("Exiting...")
            exit(0)
        elif choice_a == "1":
            os.system("sudo systemctl start ams-attendance")
        elif choice_a == "2":
            os.system("sudo systemctl stop ams-attendance")
        elif choice_a == "3":
            os.system("sudo systemctl restart ams-attendance")
        elif choice_a == "4":
            # Ask if the user wants today's date or different date
            print(
                """
Please select an option:
1. Today's Date
2. Different Date
0. Exit

Press Enter to go back
"""
            )
            choice_d = input("Enter your choice: ")
            if choice_d == "":
                pass
            elif choice_d == "0":
                print("Exiting...")
                exit(0)
            elif choice_d == "1":
                # Get today's date
                date = get_date()
                # Get attendance data
                query = f"SELECT * FROM {date}"
                try:
                    attendance_data = execute(query)
                except connector.ProgrammingError:
                    print("No attendance data found")
                    exit(0)
                # Print attendance data to csv file
                with open(f"attendance_{date}.csv", "w") as f:
                    f.write("Class, Roll, Period, Name\n")
                    for row in attendance_data:
                        f.write(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}\n")
                # Start http server to serve csv file
                os.chdir(os.getcwd())
                httpd = http.server.HTTPServer(
                    ("", 8723), http.server.SimpleHTTPRequestHandler
                )
                # Get IP address using ifconfig
                ip = os.popen("ifconfig").read().split("inet ")[1].split(" ")[0]
                print(
                    f"Serving attendance data at http://{ip}:8000/attendance_{date}.csv"
                )
                k = input("Press Enter to stop serving")
                httpd.shutdown()
                os.remove(f"attendance_{date}.csv")
            elif choice_d == "2":
                # Ask for date
                date = input("Enter date in dd_mm_yyyy format: ")
                # Get attendance data
                query = f"SELECT * FROM {date}"
                try:
                    attendance_data = execute(query)
                except connector.ProgrammingError:
                    print("No attendance data found")
                    exit(0)
                # Print attendance data to csv file
                with open(f"attendance_{date}.csv", "w") as f:
                    f.write("Class, Roll, Period, Name\n")
                    for row in attendance_data:
                        f.write(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}\n")
                # Start http server to serve csv file
                os.chdir(os.getcwd())
                httpd = http.server.HTTPServer(
                    ("", 8723), http.server.SimpleHTTPRequestHandler
                )
                # Get IP address using ifconfig
                ip = os.popen("ifconfig").read().split("inet ")[1].split(" ")[0]
                print(
                    f"Serving attendance data at http://{ip}:8000/attendance_{date}.csv"
                )
                k = input("Press Enter to stop serving")
                httpd.shutdown()
                os.remove(f"attendance_{date}.csv")
        else:
            print("Invalid Choice")


if __name__ == "__main__":
    print("Welcome to AMS Admin Console")
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("\nExiting...")
            exit(0)
        except Exception as e:
            print(f"Error: {e}")
            exit(1)
