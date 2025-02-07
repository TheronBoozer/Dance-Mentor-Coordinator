# create virtual environment (venv)
cd ~
mkdir ~/.venv
python -m venv --system-site-packages ~/.venv
source ~/.venv/bin/activate

# use pip to install packages
python -m ensurepip --upgrade
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install --upgrade oauth2client
pip install --upgrade schedule
pip install --upgrade datetime
pip install --upgrade requests
pip install --upgrade beautifulsoup4

# deactivate venv
deactivate

# make launchers executable
cd ~
chmod 755 Bash_Scripts/Launchers/Schedule.sh
chmod 755 Bash_Scripts/Launchers/Confirm.sh
chmod 755 Bash_Scripts/Launchers/Initiate.sh
chmod 755 Bash_Scripts/Launchers/Scrape.sh
chmod 755 Bash_Scripts/Launchers/Update.sh
chmod 755 Bash_Scripts/Launchers/Restart.sh
chmod 755 Bash_Scripts/Launchers/Authenticate.sh
chmod 755 Bash_Scripts/Launchers/Toggle.sh

# set cron tasks
(crontab -l; echo "0 20 * * 5 sh ~/Bash_Scripts/Launchers/Test.sh >> ~/Bash_Scripts/logs/test.log 2>&1") | crontab -             # test at 20:00 Friday
(crontab -l; echo "0 0 * * 6 sh ~/Bash_Scripts/Launchers/Restart.sh >> ~/Bash_Scripts/logs/restart.log 2>&1") | crontab -        # restart at 00:00 Saturday
(crontab -l; echo "45 7 * * 6 sh ~/Bash_Scripts/Launchers/Scrape.sh >> ~/Bash_Scripts/logs/scrape.log 2>&1") | crontab -         # Scrape info at 07:45 Saturday
(crontab -l; echo "0 8 * * 6 sh ~/Bash_Scripts/Launchers/Initiate.sh >> ~/Bash_Scripts/logs/initial.log 2>&1") | crontab -       # Initialize at 08:00 Saturday
(crontab -l; echo "0 20 * * 7 sh ~/Bash_Scripts/Launchers/Confirm.sh >> ~/Bash_Scripts/logs/confirm.log 2>&1") | crontab -       # Confirm at 20:00 Sunday
(crontab -l; echo "15 20 * * 7 sh ~/Bash_Scripts/Launchers/Update.sh >> ~/Bash_Scripts/logs/update.log 2>&1") | crontab -        # Update at 20:15 Sunday

# turn off LEDs
cd ~
sudo sh -c "echo '# Disable Activity LED (Green)' >>/boot/firmware/config.txt"
sudo sh -c "echo 'dtparam=act_led_trigger=none' >>/boot/firmware/config.txt"                        # disable green activity LED on triggers
sudo sh -c "echo 'dtparam=act_led_activelow=on\n' >>/boot/firmware/config.txt"                     # disable green activity LED on power

# restart cron
service cron restart

# restart
echo 'Reboot? (y/n)' && read x && [[ "$x" == "y" ]] && sudo reboot