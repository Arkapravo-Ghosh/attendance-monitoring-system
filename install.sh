#!/bin/bash
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

if [ -d "/opt/attendance-monitoring-system" ]; then
    echo "Updating the repo..."
    cd /opt/attendance-monitoring-system
    git pull
else
    echo "Cloning the repo to /opt..."
    cd /opt
    git clone https://github.com/Arkapravo-Ghosh/attendance-monitoring-system.git
    git config pull.rebase false
fi

if [ -x "$(command -v apt)" ]; then
    echo "Installing MariaDB..."
    curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup | bash
    apt update
    apt install -y libmariadb-dev mariadb-server mariadb-client python3-dev python3-pip
fi

echo "Installing the required pip packages..."
pip3 install -r /opt/attendance-monitoring-system/requirements.txt
echo -n "Do you want to auto setup MariaDB? (Y/n): "
read auto

if [ "$auto" == "Y" ] || [ "$auto" == "y" ] || [ "$auto" == "" ]; then
    echo "Changing the root password of MariaDB..."
    mysql_secure_installation
    echo "Creating the database..."
    mysql -u root < /opt/attendance-monitoring-system/server/database.sql
    echo "Creating the user..."
    echo -n "Enter the password for the user: "
    read -s password
    echo
    mysql -u root -e "CREATE USER 'attendance'@'%' IDENTIFIED BY '$password';"
    mysql -u root -e "GRANT ALL PRIVILEGES ON attendance.* TO 'attendance'@'%';"
    mysql -u root -e "FLUSH PRIVILEGES;"
fi

echo -n "Has the password for the SQL user been changed? (Y/n): "
read changed
if [ "$changed" == "Y" ] || [ "$changed" == "y" ] || [ "$changed" == "" ]; then
    if [ "$password" == "" ]; then
        echo -n "Enter the password for the SQL user: "
        read -s password
        echo
    fi
fi

echo -n "Do you want to generate the config file? (Y/n): "
read generate
if [ "$generate" == "Y" ] || [ "$generate" == "y" ] || [ "$generate" == "" ]; then
    echo "Creating the config file..."
    mkdir /etc/ams
    echo "$password" > /etc/ams/mysqlpasswd.txt
fi

echo -n "Do you want to secure the config file? (Y/n): "
read secure
if [ "$secure" == "Y" ] || [ "$secure" == "y" ] || [ "$secure" == "" ]; then
    echo "Securing the config file..."
    echo "Creating the ams group..."
    groupadd ams
    echo "Adding the user to the ams group..."
    echo -n "Enter your username: "
    read username
    usermod -aG ams $username
    echo "Changes will take effect after a relogin."
    echo "Setting the permissions..."
    chown root:ams /etc/ams/mysqlpasswd.txt
    chmod 640 /etc/ams/mysqlpasswd.txt
fi

echo "Adding the scripts to the PATH variable..."
echo "export PATH=\$PATH:/opt/attendance-monitoring-system/src/server:/opt/attendance-monitoring-system/src/fingerprint" >> /etc/profile
if [ -x "$(command -v zsh)" ]; then
    echo "export PATH=\$PATH:/opt/attendance-monitoring-system/server:/opt/attendance-monitoring-system/fingerprint" >> /etc/zsh/zprofile
fi

echo -n "Do you want to reboot now? (Y/n): "
read reboot
if [ "$reboot" == "Y" ] || [ "$reboot" == "y" ] || [ "$reboot" == "" ]; then
    echo "Rebooting..."
    reboot
fi
echo "Installed."
