# Computational Social Science Reddit Bot

## Overview

This bot is designed increase engagement on the r/CompSocial. It's built using Python 3, MongoDB, and the PRAW package.

## Requirements

### Python Version

- Python 3.x

### Packages

- dotenv
- PRAW
- pymongo

To install the required packages, you can run:

```bash
pip install -r requirements.txt
```

OR install manually

```bash
pip install python-dotenv
pip install praw
pip install pymongo
```


## Usage

To run the bot, allowlist your IP address in the shared MongoDB (or create your own mongo instance) 

Then create a .env file with the auth string for mongo, the bot credentials, and subreddit name. Use the template in .env.template as a reference 

Now you can run the bot with 

```bash
python3 main.py
```

## Sending updates to production

So you've added a cool feature (and tested locally to make sure it actually works) and pushed it to the main branch on github.

Now you will need to log into the AWS EC2 server that runs the bot. You can open the terminal for the server in the browser, and run the `update.sh` script. This script pulls any new changes from github, kills the redditbot service and starts it again.

```bash
#change directory to the bot code
cd CSSpark_Bot
#run the update script
./update.sh
```



## Server setup

Right now the bot is running on an EC2 instance.

The bot is running in a systemd service. If you are starting from scratch on a new EC2 or other Ubuntu server you will need to make your `redditbot.service` file in `/etc/systemd/system/`

```bash
sudo vim /etc/systemd/system/redditbot.service
```

paste in the following configuration

```ini
[Unit]
Description=Reddit bot for comp social
After=network.target

[Service]
Type=simple
User=ubuntu
ExecStart=/usr/bin/python3 /home/ubuntu/CSSpark_Bot/main.py 
Restart=no

[Install]
WantedBy=multi-user.target
```

run

```bash
#enables start on boot so the bot will come back in the event the server randomly reboots
sudo systemctl enable redditbot.service 
sudo systemctl start redditbot.service
#check that the service is running
sudo systemctl status redditbot.service
```
