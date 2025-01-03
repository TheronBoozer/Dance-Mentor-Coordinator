# create virtual environment (venv)
cd ~
mkdir /home/$USER/DMC_Bot/.venv
python3 -m venv --system-site-packages home/$USER/DMC_Bot/.venv
source home/$USER/DMC_Bot/.venv/bin/activate

# use pip to install packages
python -m ensurepip --upgrade
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install --upgrade oauth2client
pip install --upgrade schedule
pip install --upgrade datetime
pip install --upgrade requests
pip install --upgrade beautifulsoup4

# make launchers executable
cd ~
chmod 755 home/$USER/DMC_Bot/Launchers/launcher.sh
chmod 755 home/$USER/DMC_Bot/Launchers/Confirm.sh
chmod 755 home/$USER/DMC_Bot/Launchers/Initiate.sh
chmod 755 home/$USER/DMC_Bot/Launchers/Scrape.sh
chmod 755 home/$USER/DMC_Bot/Launchers/Update.sh
chmod 755 home/$USER/DMC_Bot/Launchers/Restart.sh

# set cron variables
(crontab -l 2>/dev/null; echo "SHELL=/home/$USER/DMC_Bot/.venv") | crontab -                # set cron shell to venv
(crontab -l; echo "PATH=/home/$USER/DMC_Bot") | crontab -                                   # set cron path to DMC_Bot

# set cron tasks
(crontab -l; echo "0 0 * * 6 Launchers/Restart.sh >> /logs/restart.log") | crontab -        # restart at 00:00 Saturday
(crontab -l; echo "7 45 * * 6 Launchers/Scrape.sh >> /logs/scrape.log") | crontab -         # Scrape info at 07:45 Saturday
(crontab -l; echo "8 0 * * 6 Launchers/Initiate.sh >> /logs/initial.log") | crontab -       # Initialize at 08:00 Saturday
(crontab -l; echo "20 0 * * 7 Launchers/Confirm.sh >> /logs/confirm.log") | crontab -       # Confirm at 20:00 Sunday
(crontab -l; echo "20 15 * * 7 Launchers/Update.sh >> /logs/update.log") | crontab -        # Update at 20:15 Sunday