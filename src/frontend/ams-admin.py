#!/bin/python3
import time
import os

try:
    import mariadb as connector
except ImportError:
    import mysql.connector as connector
no_of_periods = 6
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


def get_attendance_data(date):
    try:
        data = execute(f"SELECT * FROM {date}")
    except connector.ProgrammingError:
        print("Error: Table does not exist")
        exit(1)
    return data


def get_student_data():
    data = execute("SELECT * FROM student_data")
    return data


def get_absent_students(date):
    attendance_data = get_attendance_data(date)
    student_data = get_student_data()
    absent_data = []
    for row in student_data:
        flag = 0
        for row_a in attendance_data:
            if row[2] == row_a[0] and row[3] == row_a[1]:
                flag = 1
                break
        if flag == 0:
            absent_data.append(row)
    return absent_data

def get_absent_students_class(date, class_):
    attendance_data = get_attendance_data(date)
    student_data = get_student_data()
    absent_data = []
    for row in student_data:
        flag = 0
        for row_a in attendance_data:
            if row[2] == row_a[0] and row[3] == row_a[1]:
                flag = 1
                break
        if flag == 0 and row[2] == class_:
            absent_data.append(row)
    return absent_data

def get_present_students(date):
    attendance_data = get_attendance_data(date)
    student_data = get_student_data()
    present_data = []
    for row in student_data:
        flag = 0
        for row_a in attendance_data:
            if row[2] == row_a[0] and row[3] == row_a[1]:
                flag = 1
                break
        if flag == 1:
            present_data.append(row)
    return present_data

def get_present_students_class(date, class_):
    attendance_data = get_attendance_data(date)
    student_data = get_student_data()
    present_data = []
    for row in student_data:
        flag = 0
        for row_a in attendance_data:
            if row[2] == row_a[0] and row[3] == row_a[1]:
                flag = 1
                break
        if flag == 1 and row[2] == class_:
            present_data.append(row)
    return present_data

def get_bunkers(date):
    attendance_data = get_attendance_data(date)
    student_data = get_student_data()
    bunkers = []
    for row in student_data:
        count = 0
        period = []
        period_bunked = []
        for row_a in attendance_data:
            if row[2] == row_a[0] and row[3] == row_a[1]:
                count += 1
                period.append(row_a[2])
        if count == 6:
            pass
        elif count < 6 and count > 0:
            for prd in range(1, no_of_periods + 1):
                if prd not in period:
                    period_bunked.append(prd)
            bunkers.append([row[2], row[3], row[1], period_bunked])
    return bunkers

def main():
    print(
        """
Please select an option:
1. Manage Student Data
2. Manage Attendance System
3. Manage Attendance Data
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
4. Check Attendance Session Health
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
            os.system("sudo systemctl status ams-attendance")
        else:
            print("Invalid Choice")
    elif choice_ams == "3":
        print("Manage Attendance Data")
        print(
            """
1. Get Attendance Data
2. Get Absent Students Data
3. Get Absent Students Data for a Class
4. Get Bunkers List
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
            print(
                """
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
                date = get_date()
                query = f"SELECT * FROM {date}"
                try:
                    attendance_data = execute(query)
                except connector.ProgrammingError:
                    print("No attendance data found")
                    exit(0)
                with open(f"attendance_{date}.csv", "w") as f:
                    f.write("Class, Roll, Period, Name\n")
                    for row in attendance_data:
                        f.write(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}\n")
                print(f"Attendance data saved to attendance_{date}.csv")
            elif choice_d == "2":
                while True:
                    date = input("Enter date in dd_mm_yyyy format: ")
                    flag = 0
                    for i in date.split("_"):
                        if not i.isdigit():
                            print("Invalid date")
                            flag = 1
                            break
                    if flag == 0:
                        break
                query = f"SELECT * FROM {date}"
                try:
                    attendance_data = execute(query)
                except connector.ProgrammingError:
                    print("No attendance data found")
                    exit(0)
                with open(f"attendance_{date}.csv", "w") as f:
                    f.write("Class, Roll, Period, Name\n")
                    for row in attendance_data:
                        f.write(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}\n")
                print(f"Attendance data saved to attendance_{date}.csv")
            else:
                print("Invalid Choice")

        elif choice_a == "2":
            print(
                """
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
                date = get_date()
                absent_data = get_absent_students(date)
                with open(f"absent_{date}.csv", "w") as f:
                    f.write("Class, Roll, Name\n")
                    for row in absent_data:
                        f.write(f"{row[2]}, {row[3]}, {row[1]}\n")
                print(f"Absent data saved to absent_{date}.csv")
            elif choice_d == "2":
                while True:
                    date = input("Enter date in dd_mm_yyyy format: ")
                    flag = 0
                    for i in date.split("_"):
                        if not i.isdigit():
                            print("Invalid date")
                            flag = 1
                            break
                    if flag == 0:
                        break
                absent_data = get_absent_students(date)
                with open(f"absent_{date}.csv", "w") as f:
                    f.write("Class, Roll, Name\n")
                    for row in absent_data:
                        f.write(f"{row[2]}, {row[3]}, {row[1]}\n")
                print(f"Absent data saved to absent_{date}.csv")
            else:
                print("Invalid Choice")
        elif choice_a == "3":
            print(
                """
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
                date = get_date()
                class_ = input("Enter class: ")
                attendance_data = get_absent_students_class(date, class_)
                with open(f"absent_{date}_{class_}.csv", "w") as f:
                    f.write("Roll, Name\n")
                    for row in attendance_data:
                        f.write(f"{row[0]}, {row[1]}\n")
                print(f"Absent students data for class {class_} saved to absent_{date}_{class_}.csv")
            elif choice_d == "2":
                while True:
                    date = input("Enter date in dd_mm_yyyy format: ")
                    flag = 0
                    for i in date.split("_"):
                        if not i.isdigit():
                            print("Invalid date")
                            flag = 1
                            break
                    if flag == 0:
                        break
                class_ = input("Enter class: ")
                attendance_data = get_absent_students_class(date, class_)
                with open(f"absent_{date}_{class_}.csv", "w") as f:
                    f.write("Roll, Name\n")
                    for row in attendance_data:
                        f.write(f"{row[0]}, {row[1]}\n")
                print(f"Absent students data for class {class_} saved to absent_{date}_{class_}.csv")
            else:
                print("Invalid Choice")
        elif choice_a == "4":
            print(
                """
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
                date = get_date()
                bunkers = get_bunkers(date)
                # Example bunkers list with one row: [['1E', 23, 'Arkapravo Ghosh', [1, 2, 3]]]
                with open(f"bunkers_{date}.csv", "w") as f:
                    f.write("Class, Roll, Name, Periods\n")
                    for row in bunkers:
                        pr = ""
                        for i in row[3]:
                            if i == row[3][-1]:
                                pr += f"{i}"
                            else:
                                pr += f"{i} "
                        f.write(f"{row[0]}, {row[1]}, {row[2]}, {pr}\n")
                print(f"Bunkers data saved to bunkers_{date}.csv")
            elif choice_d == "2":
                while True:
                    date = input("Enter date in dd_mm_yyyy format: ")
                    flag = 0
                    for i in date.split("_"):
                        if not i.isdigit():
                            print("Invalid date")
                            flag = 1
                            break
                    if flag == 0:
                        break
                bunkers = get_bunkers(date)
                with open(f"bunkers_{date}.csv", "w") as f:
                    f.write("Class, Roll, Name, Periods\n")
                    for row in bunkers:
                        pr = ""
                        for i in row[3]:
                            if i == row[3][-1]:
                                pr += f"{i}"
                            else:
                                pr += f"{i} "
                        f.write(f"{row[0]}, {row[1]}, {row[2]}, {pr}\n")
                print(f"Bunkers data saved to bunkers_{date}.csv")
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
