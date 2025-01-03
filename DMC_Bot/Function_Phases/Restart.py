import os

def reboot():
    os.system("shutdown -t 5 -r -f")

reboot()