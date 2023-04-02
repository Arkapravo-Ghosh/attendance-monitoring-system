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
    echo "Detected Debian Linux"
    if [ ! -x "$(command -v curl)" ]; then
        echo "Installing curl..."
        apt install -y curl
    fi
    if [ ! -x "$(command -v mysql)" ]; then
        echo -n "Do you want to install MariaDB? (Y/n): "
        read install
        if [ "$install" == "Y" ] || [ "$install" == "y" ] || [ "$install" == "" ]; then
            curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup | bash
            apt update
            apt install -y libmariadb-dev mariadb-server mariadb-client python3-dev python3-pip
        fi
    fi
elif [ -x "$(command -v pacman)" ]; then
    echo "Detected that you use Arch btw"
    if [ ! -x "$(command -v curl)" ]; then
        echo "Installing curl..."
        pacman -S --noconfirm curl
    fi
    if [ ! -x "$(command -v mysql)" ]; then
        echo -n "Do you want to install MariaDB? (Y/n): "
        read install
        if [ "$install" == "Y" ] || [ "$install" == "y" ] || [ "$install" == "" ]; then
            pacman -S --noconfirm mariadb python-pip
        fi
    fi
fi
echo -n "Do you want to install the required pip packages? (Y/n): "
read pipinstall
if [ "$pipinstall" == "Y" ] || [ "$pipinstall" == "y" ] || [ "$pipinstall" == "" ]; then
    echo "Installing the required pip packages..."
    pip3 install -r /opt/attendance-monitoring-system/requirements.txt
fi
echo -n "Do you want to auto setup MariaDB? (Y/n): "
read auto

if [ "$auto" == "Y" ] || [ "$auto" == "y" ] || [ "$auto" == "" ]; then
    echo "Enabling and Starting MariaDB..."
    systemctl enable --now mysql
    echo "Changing the root password of MariaDB..."
    mysql_secure_installation
    echo "Creating the database..."
    mysql -u root < /opt/attendance-monitoring-system/server/database.sql
    echo "Creating the user..."
    pass_var="Enter Password for SQL User: "
    while IFS= read -p "$pass_var" -r -s -n 1 letter
    do
        if [[ $letter == $'\0' ]]
        then
            break
        fi
        password="$password$letter"
        pass_var="*"
    done
    echo
    mysql -u root -e "CREATE USER 'attendance'@'%' IDENTIFIED BY '$password';"
    mysql -u root -e "GRANT ALL PRIVILEGES ON attendance.* TO 'attendance'@'%';"
    mysql -u root -e "FLUSH PRIVILEGES;"
fi

echo -n "Do you want to generate the config file? (Y/n): "
read generate
if [ "$generate" == "Y" ] || [ "$generate" == "y" ] || [ "$generate" == "" ]; then
    echo "Creating the config file..."
    mkdir /etc/ams
    if [ "$password" == "" ]; then
        pass_var="Enter Password for SQL User: "
        while IFS= read -p "$pass_var" -r -s -n 1 letter
        do
            if [[ $letter == $'\0' ]]
            then
                break
            fi
            password="$password$letter"
            pass_var="*"
        done
        echo
    fi
    echo -n "$password" > /etc/ams/mysqlpasswd.txt
fi
echo "Creating ams user..."
useradd -m ams
echo "Adding the user to the dialout group..."
usermod -aG dialout ams
echo "Adding service files..."
cp /opt/attendance-monitoring-system/server/ams-attendance.service /etc/systemd/system/ams-attendance.service
echo -n "Do you want to enable the ams service? (Y/n): "
read enableams
if [ "$enableams" == "Y" ] || [ "$enableams" == "y" ] || [ "$enableams" == "" ]; then
    echo "Enabling the service..."
    systemctl enable ams-attendance.service
fi
echo -n "Do you want to secure the config file? (Y/n): "
read secure
if [ "$secure" == "Y" ] || [ "$secure" == "y" ] || [ "$secure" == "" ]; then
    echo "Securing the config file..."
    echo "Creating the ams group..."
    groupadd ams
    echo "Adding ams user to the ams group..."
    usermod -aG ams ams
    echo "Adding current user to the ams group..."
    usermod -aG ams $SUDO_USER
    echo "Changes will take effect after a relogin."
    echo "Setting the permissions..."
    chown root:ams /etc/ams/mysqlpasswd.txt
    chmod 640 /etc/ams/mysqlpasswd.txt
fi

echo "Adding the scripts to the PATH variable..."
if [ -f "/etc/profile" ]; then
    if [ -z "$(grep "/opt/attendance-monitoring-system/src/server" /etc/profile)" ]; then
        echo "export PATH=\$PATH:/opt/attendance-monitoring-system/src/server:/opt/attendance-monitoring-system/src/fingerprint" >> /etc/profile
        if [ -x "$(command -v zsh)" ]; then
            if [ -z "$(grep "/opt/attendance-monitoring-system/src/server" /etc/zsh/zprofile)" ]; then
                echo "export PATH=\$PATH:/opt/attendance-monitoring-system/src/server:/opt/attendance-monitoring-system/src/fingerprint" >> /etc/zsh/zprofile
            fi
        fi
    fi
fi

echo -n "Do you want to reboot now? (Y/n): "
read reboot
if [ "$reboot" == "Y" ] || [ "$reboot" == "y" ] || [ "$reboot" == "" ]; then
    echo "Rebooting..."
    reboot
fi
echo "Installed."
