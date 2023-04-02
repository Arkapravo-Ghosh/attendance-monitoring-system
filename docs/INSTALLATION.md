# Installation guide
## Backend
### Prerequisites:
- Python 3.6+
- MySQL 8.0+ or MariaDB 10.3+
- pip 19.0+
### Clone the repository:
```
git clone https://github.com/Arkapravo-Ghosh/attendance-monitoring-system.git
```
### Install dependencies:
<details>
<summary>Linux</summary>

```bash
git clone https://github.com/Arkapravo-Ghosh/attendance-monitoring-system.git
cd attendance-monitoring-system
sudo ./install.sh
```
</details>
<details>
<summary>Windows</summary>

```powershell
git clone https://github.com/Arkapravo-Ghosh/attendance-monitoring-system.git
cd attendance-monitoring-system
py -m pip install -r requirements.txt
```
### Create a database:
```sql
CREATE DATABASE attendance;
```
### Create a user:
```sql
CREATE USER 'attendance'@'localhost' IDENTIFIED BY 'password';
```
> **Note:** Replace `password` with your desired password.
#### Grant privileges:
```sql
GRANT ALL PRIVILEGES ON attendance.* TO 'attendance'@'localhost';
FLUSH PRIVILEGES;
```
</details>


#### Put the Newly Created SQL User's password in the text file at `/etc/ams/mysqlpasswd.txt`
> **NOTE:** If you are using Windows, you can put the password in the file at `C:\ams\mysqlpasswd.txt` instead.

### Run the backend (Linux):

```bash
backend.py -h
```

### Connect R307 Fingerprint Scanner to Raspberry Pi using UART to USB Converter:

<div align=center>
<img align=top height="300" src="images/R307-Fingerprint-Scanner-Pinout.png" />&nbsp;
<img align=top height="300" src="images/usb-to-uart-img.jpg" />
</div>
<br>

- Connect the 5V pin of the Fingerprint Scanner to 5V pin of the UART to USB Converter and the GND pin of the Fingerprint Scanner to GND pin of the UART to USB Converter.
- Connect the TXD pin of the Fingerprint Scanner to RXD pin of the UART to USB Converter and the RXD pin of the Fingerprint Scanner to TXD pin of the UART to USB Converter.
