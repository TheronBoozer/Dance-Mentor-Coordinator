# create virtual environment (venv)
cd ~
mkdir ~/DMC_Bot/.venv
python -m venv --system-site-packages ~/DMC_Bot/.venv
source ~/DMC_Bot/.venv/bin/activate

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
chmod 755 DMC_Bot/Bash_Scripts/Launchers/Schedule.sh
chmod 755 DMC_Bot/Bash_Scripts/Launchers/Confirm.sh
chmod 755 DMC_Bot/Bash_Scripts/Launchers/Initiate.sh
chmod 755 DMC_Bot/Bash_Scripts/Launchers/Scrape.sh
chmod 755 DMC_Bot/Bash_Scripts/Launchers/Update.sh
chmod 755 DMC_Bot/Bash_Scripts/Launchers/Restart.sh
chmod 755 DMC_Bot/Bash_Scripts/Launchers/Authenticate.sh
chmod 755 DMC_Bot/Bash_Scripts/Launchers/Toggle.sh

# set cron tasks
(crontab -l; echo "0 0 * * 6 sh ~/DMC_Bot/Bash_Scripts/Launchers/Restart.sh >> ~/DMC_Bot/Bash_Scripts/logs/restart.log") | crontab -        # restart at 00:00 Saturday
(crontab -l; echo "45 7 * * 6 sh ~/DMC_Bot/Bash_Scripts/Launchers/Scrape.sh >> ~/DMC_Bot/Bash_Scripts/logs/scrape.log") | crontab -         # Scrape info at 07:45 Saturday
(crontab -l; echo "0 8 * * 6 sh ~/DMC_Bot/Bash_Scripts/Launchers/Initiate.sh >> ~/DMC_Bot/Bash_Scripts/logs/initial.log") | crontab -       # Initialize at 08:00 Saturday
(crontab -l; echo "0 20 * * 7 sh ~/DMC_Bot/Bash_Scripts/Launchers/Confirm.sh >> ~/DMC_Bot/Bash_Scripts/logs/confirm.log") | crontab -       # Confirm at 20:00 Sunday
(crontab -l; echo "15 20 * * 7 sh ~/DMC_Bot/Bash_Scripts/Launchers/Update.sh >> ~/DMC_Bot/Bash_Scripts/logs/update.log") | crontab -        # Update at 20:15 Sunday

# turn off LEDs
cd ~
sudo sh -c "echo '# Disable Activity LED (Green)' >>/boot/firmware/config.txt"
sudo sh -c "echo 'dtparam=act_led_trigger=none' >>/boot/firmware/config.txt"                        # disable green activity LED on triggers
sudo sh -c "echo 'dtparam=act_led_activelow=on\n' >>/boot/firmware/config.txt"                     # disable green activity LED on power

# restart cron
service cron restart