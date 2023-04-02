#!/bin/bash
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi
echo -n "Do you want to uninstall Attendance Monitoring System? (Y/n): "
read uninstall
if [ "$uninstall" != "Y" ] && [ "$uninstall" != "y" ] && [ "$uninstall" != "" ]; then
    exit
fi
rm -f /usr/bin/ams-server
rm -f /usr/bin/ams-attendance
rm -f /usr/bin/ams-delete
rm -f /usr/bin/ams-enroll
rm -f /usr/bin/ams-verify
rm -f /usr/bin/ams-get-data
echo -n "Do you want to remove the repository? (Y/n): "
read remove
if [ "$remove" == "Y" ] || [ "$remove" == "y" ] || [ "$remove" == "" ]; then
    rm -rf /opt/attendance-monitoring-system
fi

sed -i '/attendance-monitoring-system/d' /etc/profile
if [ -x "$(command -v zsh)" ]; then
    sed -i '/attendance-monitoring-system/d' /etc/zsh/zprofile
fi
echo -n "Do you want to remove the database? (y/N): "
read rmdb
if [ "$rmdb" == "Y" ] || [ "$rmdb" == "y" ]; then
    rm -rf /var/lib/mysql/attendance
fi

echo "Uninstalled successfully."
