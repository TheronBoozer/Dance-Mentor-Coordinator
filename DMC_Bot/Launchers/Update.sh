#!/bin/sh
# Update.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd /home/$USER/DMC_Bot
sudo /.venv/bin/python /Function_Phases/Update.py
cd /