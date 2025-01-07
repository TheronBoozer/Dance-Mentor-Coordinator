#!/bin/sh
# Toggle.sh
# navigate to home directory, then to this directory, then edit python script, then back home

sed -i 's/$1 = False/$1 = True' ~/DMC_Bot/flags.py || sed -i 's/$1 = True/$1 = False' ~/DMC_Bot/flags.py