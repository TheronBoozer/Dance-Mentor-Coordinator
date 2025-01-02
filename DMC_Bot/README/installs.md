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