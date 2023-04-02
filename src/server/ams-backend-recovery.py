#!/bin/python3
import subprocess


def main():
    ams_attendance = subprocess.run(
        ["systemctl", "is-failed", "ams-attendance.service"], stdout=subprocess.PIPE
    )
    ams_attendance = ams_attendance.stdout.decode("utf-8").strip()
    if ams_attendance == "failed":
        subprocess.run(["systemctl", "daemon-reload"])
        subprocess.run(["systemctl", "restart", "ams-attendance.service"])


if __name__ == "__main__":
    main()
