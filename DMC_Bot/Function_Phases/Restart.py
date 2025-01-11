import os

def reboot():
    if os.name == 'nt':
        os.system("shutdown -t 5 -r -f")
    else:
        os.system("reboot")