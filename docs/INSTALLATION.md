# Install guide
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
<summary>Linux/macOS</summary>

```bash
pip3 install -r requirements.txt
```
</details>
<details>
<summary>Windows</summary>

```powershell
py -m pip install -r requirements.txt
```
</details>

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
#### Put the Newly Created SQL User's password in the text file at `/etc/ams/mysqlpasswd.txt`
> **NOTE:** If you are using Windows, you can put the password in the file at `C:\ams\mysqlpasswd.txt` instead.
<details>
<summary>Optional: Secure the password file in Linux</summary>

```bash
sudo groupadd ams
sudo usermod -aG ams $USER
sudo chown root:ams /etc/ams/mysqlpasswd.txt
sudo chmod 640 /etc/ams/mysqlpasswd.txt
newgrp ams
```
> **NOTE:** Re-login to apply the changes user-wide.
</details>

### Run the backend:
<details>
<summary>Linux/macOS</summary>

```bash
python3 ./src/server/backend.py -h
```
</details>
<details>
<summary>Windows</summary>

```powershell
py .\src\server\backend.py -h
```
</details>
