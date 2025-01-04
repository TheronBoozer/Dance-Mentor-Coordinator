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
chmod 755 DMC_Bot/Launchers/launcher.sh
chmod 755 DMC_Bot/Launchers/Confirm.sh
chmod 755 DMC_Bot/Launchers/Initiate.sh
chmod 755 DMC_Bot/Launchers/Scrape.sh
chmod 755 DMC_Bot/Launchers/Update.sh
chmod 755 DMC_Bot/Launchers/Restart.sh

# set cron variables
(crontab -l 2>/dev/null; echo "SHELL=/home/$USER/DMC_Bot/.venv") | crontab -                # set cron shell to venv
(crontab -l; echo "PATH=/home/$USER/DMC_Bot\n") | crontab -                                   # set cron path to DMC_Bot

# set cron tasks
(crontab -l; echo "0 0 * * 6 Launchers/Restart.sh >> /logs/restart.log") | crontab -        # restart at 00:00 Saturday
(crontab -l; echo "45 7 * * 6 Launchers/Scrape.sh >> /logs/scrape.log") | crontab -         # Scrape info at 07:45 Saturday
(crontab -l; echo "0 8 * * 6 Launchers/Initiate.sh >> /logs/initial.log") | crontab -       # Initialize at 08:00 Saturday
(crontab -l; echo "0 20 * * 7 Launchers/Confirm.sh >> /logs/confirm.log") | crontab -       # Confirm at 20:00 Sunday
(crontab -l; echo "15 20 * * 7 Launchers/Update.sh >> /logs/update.log") | crontab -        # Update at 20:15 Sunday

# turn off LEDs
cd ~
sudo sh -c "echo '# Disable Power LED (Red)' >>/boot/firmware/config.txt"
sudo sh -c "echo 'dtparam=pwr_led_activelow=off\n' >>/boot/firmware/config.txt"                     # disable red power LED
sudo sh -c "echo '# Disable Activity LED (Green)' >>/boot/firmware/config.txt"
sudo sh -c "echo 'dtparam=act_led_trigger=none' >>/boot/firmware/config.txt"                        # disable green activity LED on triggers
sudo sh -c "echo 'dtparam=act_led_activelow=off\n' >>/boot/firmware/config.txt"                     # disable green activity LED on power
sudo sh -c "echo '# Disable LAN LEDs' >>/boot/firmware/config.txt"
sudo sh -c "echo 'dtparam=eth_led0=14' >>/boot/firmware/config.txt"                                 # disable LAN LED 0
sudo sh -c "echo 'dtparam=eth_led1=14\n' >>/boot/firmware/config.txt"                               # disable LAN LED 1


# restart
sudo reboot