#!/bin/bash
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi

rm -f /usr/bin/ams-server
rm -f /usr/bin/ams-attendance
rm -f /usr/bin/ams-delete
rm -f /usr/bin/ams-enroll
rm -f /usr/bin/ams-verify
rm -f /usr/bin/ams-get-data
rm -rf /opt/attendance-monitoring-system

sed -i '/attendance-monitoring-system/d' /etc/profile
source /etc/profile
if [ -x "$(command -v zsh)" ]; then
    sed -i '/attendance-monitoring-system/d' /etc/zsh/zprofile
    source /etc/zsh/zprofile
fi

echo "Uninstalled successfully."
