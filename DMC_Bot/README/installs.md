sudo pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip3 install --upgrade oauth2client
pip install --upgrade schedule
pip install --upgrade datetime
pip install --upgrade requests
sudo pip install --upgrade beautifulsoup4


## For Raspbian Lite
add the --break-system-packages flag to each install and use sudo
or, better yet
use a avirtual environment

## For Windows
pip install pywin32
    post install find the python Scripts folder (C:\users\user\AppData\Local\Programs\Python\Python312\Scripts) and run pywin32_postinstall


## commands used
from pc:
    cd C:\Users\thero\Documents\GitHub\Dance-Mentor-Coordinator
    scp -r ./* DMC@ballroom-dance.local:/home/DMC

from pi
    cd ~
    mkdir /home/$USER/DMC_Bot/.venv
    python -m venv --system-site-packages home/$USER/DMC_Bot/.venv
    source home/$USER/DMC_Bot/.venv/bin/activate
    python -m ensurepip --upgrade
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
    pip install --upgrade oauth2client
    pip install --upgrade schedule
    pip install --upgrade datetime
    pip install --upgrade requests
    pip install --upgrade beautifulsoup4

    cd ~
    chmod 755 DMC_Bot/Launchers/launcher.sh
    chmod 755 DMC_Bot/Launchers/Confirm.sh
    chmod 755 DMC_Bot/Launchers/Initiate.sh
    chmod 755 DMC_Bot/Launchers/Scrape.sh
    chmod 755 DMC_Bot/Launchers/Update.sh
    chmod 755 DMC_Bot/Launchers/Restart.sh
