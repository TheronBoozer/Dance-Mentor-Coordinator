# Dance Mentor Automatic Coordination (DMAC)
DMAC is an automated scheduling system designed for the WPI Ballroom Dance Team. The system employs object oriented programming in Python to schedule individual dance lessons between mentors and mentees. In brief the system takes Google Form session request responses and creates a list of possible times for each mentor. These times are listed in a new Google Form that the each mentor completes to accept or deny the session requests. Once all mentor responses are in, emails are sent out to the mentors and mentees with session details.
## Table of Contents
1. [Getting Started](#Getting-Started)
	- [Installation](#Installation)
	- [Setup](#Setup)
2. [How to Use](#How-to-Use)
	- [Making a Session Request](#Making-a-Session-Request)
	- [Adding a Mentor](#Adding-a-Mentor)
	- Adding a Location
	- Upkeep
	- Example
3. How It Works
	- Phases
		- Reboot
		- Scrape
		- Initiate
		- Confirm
		- Update
	- Objects
		- Google Drive
			- Google Form
			- Google Sheet
		- Schedules
			- When2Meet
			- 25Live
		- Timekeeping
			- Hourly Time
			- Quarter Hour
			- Hour
			- Day
		- Location
		- Mentor
		- Session Request
	- Use on a Raspberry Pi
		- Bash Scripts
			- Launchers
			- Install
			- Set
4. Debugging
	- Debug Flag
	- Cron Logs


# Getting Started
Setting up the DMAC system requires a simple installation and some setup. If you know what you're doing it should take 10 minutes given install times. And if you don't, I'll try to provide enough information for you too.

## Installation
DMAC is intended to be run from a Raspberry Pi through cron jobs. The following explains how to install it directly to a Raspberry Pi Zero 2 W, all other installation processes may be different.

### Flash Raspberry Pi OS Lite (32-bit)
This step can be done many ways, but it is recommended to use the [Raspberry Pi imager](https://www.raspberrypi.com/software/). 

With the imager installed and an SD card inserted into your computer, select Raspberry Pi Zero 2 W as your Raspberry Pi Device and Raspberry Pi OS Lite (32-bit) as your Operating System. 

<p align=center>
	<img src="https://github.com/TheronBoozer/Dance-Mentor-Coordinator/blob/main/Images/imaher.png?raw=true" alt="Installer Image" width=50%>
</p>

Now is a good time to change username and password as well as setting up the Wi-Fi when prompted.

<p align=center>
<img src="https://github.com/TheronBoozer/Dance-Mentor-Coordinator/blob/main/Images/pi%20settings.png?raw=true" alt="Settings Image" width=50%>
</p>

Once imaged, the SD card can be inserted back into the pi. It is a good idea to boot it up and check SSH connection.

### Transfer Files
I will share two ways to do this, [git](#Git) and [SCP (Secure Copy Protocol)](#scp). Even using git, you will need to add a few files containing authentication information, and while you can copy it over later through SCP separately, I find using SCP from the start is easier. 

#### Git
SSH into the Raspberry Pi.
Assuming you're on the same network use:

    ssh [user]@[hostname].local

Then clone the repository:

    git clone https://github.com/TheronBoozer/Dance-Mentor-Coordinator.git

#### SCP
Download the code onto your local machine. From there, recursively SCP the files onto the local Raspberry Pi:

	cd [path-to-code]
	scp -r ./* [user]@[hostname].local:~/

## Setup
After installing the code onto the Raspberry Pi, a bash script can be run to set up the crontab, virtual environment, dependencies, and turn off the LED.
To do so, run:

	source ~/Bash_Scripts/install.sh

You will need to enter your password to edit the crontab and then click y to reboot. This will set up everything needed for the scripts to run aside from the secrets that are needed.

### Add the secrets files
Two secret files are needed -- smtp_secrets.json and service_oauth.json. Transferring them via SCP will be easiest, but writing hem with nano will be covered. 

#### smtp secrets
The SMTP secrets file will contain login information to the email account being used. The JSON will look as follows for an outlook email:

	{
		"server" : "smtp-mail.oulook.com",
		"port" : 587,
		"username" : "email@example.com"
		"password" : "[PASSWORD]"
	}

Replace the email and [PASSWORD] with your email and password. This will only work if two factor authentication is NOT enabled for your email or if [PASSWORD] is an app password. For a gmail with the same email address and password the server would simply be switched to `smtp.gmail.com`.

This file can either be made in any text editor and then transferred through `scp PATH [user]@[hostname].local:~/Saved_Information/Ignored/` from your local computer or `nano ~/Saved_Information/Ignored/smtp_secrets.json` and typing the above through SSH into the pi.

#### service oauth
The service oauth is where things get tricky. And because I couldn't find any simple and thorough instructions to link, I get to write even more. If you already have service account credentials, feel free to skip to the section on transferring the credentials.

##### Creating a Google Cloud Project
The first step in creating a service account is to navigate to [google cloud](https://cloud.google.com/) and create a project by selecting "select a project" and then New Project.

<p align=center>
<img src="https://github.com/TheronBoozer/Dance-Mentor-Coordinator/blob/main/Images/New_Cloud_Project.png?raw=true" alt="New Account Image" width=75%>
</p>

Name your project whatever makes sense for you. Navigate to the *APIs* panel and add the Google Sheets and Google Forms API. To add an API, just find it and select it, then choose enable.

<p align=center>
<img src="https://github.com/TheronBoozer/Dance-Mentor-Coordinator/blob/main/Images/API_Screen.png?raw=true" alt="New Account Image" width=75%>
</p>

##### Creating a Service Account
Once those are enabled we need to create the service account needs to be made. Navigate to *Credentials*, then select [*Credentials in APIs & Services*](https://console.cloud.google.com/apis/credentials?) or click the link here. 

<p align=center>
<img src="https://github.com/TheronBoozer/Dance-Mentor-Coordinator/blob/main/Images/New_Service_Account.png?raw=true" alt="New Account Image" width=75%>
</p>

Give your service account a name, ID - they are typically the same - and a short description. Then grant the *Editor* role to your service account. Grant any users access if you'd like, but this is optional for this project. 

Once made navigate to the service account to *KEYS* and create a new key. This will download a json file to your laptop. Keep this json for the [Adding the Oauth Secrets](Adding-the-Oauth-Secrets) section.

##### Adding the Oauth Secrets
Take your json key from earlier and, like earlier, we will push through scp to the raspberry pi. Rename your json key to *service_oauth.json* and push it to the *Ignored* folder.

	cd [PATH_TO_KEY]
	scp ./service_oauth.json [USER]@[HOSTNAME].local:Saved_Information/Ignored/

##### Provide Access Permissions
The final step for oauth is to share whatever files the service account needs to access. This is as simple as sharing your google drive files with any other google email, just hit share and paste in your service accounts email which should look like: [NAME]@[PROJECT].iam.gserviceaccount.com.

For the DMAC system there is one sheet and one form that needs access. The Mentor Session Log sheet and the Dance Mentor Session Confirmation form. A folder can also just be shared.


# How to Use
DMAC runs weekly scripts to take user inputs and make pairings based on scheduling and preferences. Use requires keeping an updated list of Mentors and Locations, and taking weekly session requests.

## Making a Session Request
Making a session request is as simple as filling out the session request Google form. The session request form requires the following inputs:
 - Names of participants
 - Emails of participants
 - Phone numbers of participants
 - A [When2Meet](when2meet.com) of the participants availability
 - The theme of the lesson
 - The level of the dancing
 - Roles of dancers
 - The dance styles
 - The dances
 - A description of the lesson focus
 - Preferred mentors
 - If another mentor may shadow the lesson

These inputs get taken into consideration when pairing the mentees with a mentor. The automation system considers the schedule and the preferred mentors; the rest of the information is given to the mentors to self evaluate their ability to teach the lesson where they then provide a self evaluation from 1-5 as to how capable they would be to teach the lesson.

## Adding a Mentor



