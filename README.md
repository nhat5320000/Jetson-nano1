# Jetson Nano Setup Repository

This repository contains scripts and resources to set up a Jetson Nano for camera and database applications.

## Contents

- `setup_jetson.sh`: Shell script to install required packages and configure the system.
- `camera_script.py`: Python script for camera operations.
- `database_utils.py`: Python script for MySQL database interactions.
- `Images`: Diagrams and setup images.

## Usage

### 1. Download the Basic PyQT5 Interface

1. Clone this repository:

   ```bash
   git clone https://github.com/nhat5320000/Jetson-nano.git
   ```

2. Run the setup script:

   ```bash
   cd Jetson-nano
   chmod +x setup_jetson.sh
   sudo ./setup_jetson.sh
   ```

---

# Install by cmd

Follow these steps:

### 1. Install Required Dependencies

```bash
sudo apt-get install chromium-browser
sudo apt-get install python3-setuptools
sudo apt update
sudo apt install python3-pip
pip3 install imutils
#pip3 install nanocamera
git clone https://github.com/thehapyone/NanoCamera
cd NanoCamera
sudo python3 setup.py install
#pip3 install --user pyqt5
sudo apt-get install python3-pyqt5
sudo apt-get install pyqt5-dev-tools
sudo apt-get install qttools5-dev-tools
qtchooser -run-tool=designer -qt=5
#pyuic5 -x filename.ui -o filename.py
sudo apt-get install mysql-server
sudo mysql_secure_installation
Y-> pass:mysql 
sudo mysql -u root -p 
pass: mysql
#show database;

CREATE USER 'vqbg'@'localhost' IDENTIFIED BY 'vqbg123!';
GRANT ALL PRIVILEGES ON *.* TO 'vqbg'@'localhost';
exit;
sudo mysql -u vqbg -p
pass: vqbg123!
CREATE DATABASE CAMERA_PAPER;
exit;
# Bảng dữ liệu phần mềm sẽ tạo ra khi khỏi động SETTING_DATA_2
# USE CAMERA_PAPER;
# SELECT * FROM SETTING_DATA_2;

pip3 install mysql-connector
#sudo snap install pycharm-community --edge --classic Jetson orin

sudo apt install libcanberra-gtk-module libcanberra-gtk3-module
sudo /opt/nvidia/jetson-io/jetson-io.py
pip3 install pymodbus
sudo apt install v4l-utils
v4l2-ctl --list-devices
v4l2-ctl -d /dev/video0 --all
```
