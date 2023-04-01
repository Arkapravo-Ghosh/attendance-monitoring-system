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
