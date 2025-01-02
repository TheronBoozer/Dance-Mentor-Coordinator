cd ~
mkdir /home/$USER/DMC_Bot/.venv
python3 -m venv --system-site-packages home/$USER/DMC_Bot/.venv
source home/$USER/DMC_Bot/.venv/bin/activate
python -m ensurepip --upgrade
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install --upgrade oauth2client
pip install --upgrade schedule
pip install --upgrade datetime
pip install --upgrade requests
pip install --upgrade beautifulsoup4

cd ~
chmod 755 home/$USER/DMC_Bot/launcher.sh
(crontab -l 2>/dev/null; echo "@reboot sh /home/$USER/DMC_Bot/launcher.sh >/home/$USER/DMC_Bot/logs/cronlog 2>&1") | crontab -