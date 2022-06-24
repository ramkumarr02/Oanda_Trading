#!/bin/bash
sudo apt-get update
sudo apt install screen
yes | sudo apt install python3-pip
cd bt_3ema_trader
pip3 install -r requirements.txt
screen -S myscreen