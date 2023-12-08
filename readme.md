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

Now you will need to log into the AWS EC2 server that runs the bot. You can open the terminal for the server in the browser (click on the EC2 instance in AWS, and then click "connect" on the top right), and run the `update.sh` script. This script pulls any new changes from github, kills the redditbot service and starts it again.

```bash
#change directory to the bot code
cd CSSpark_Bot
#run the update script
./update.sh
```



## Server setup

The following instructions are for setting up a brand new server to run the bot. See above for pushing updates to an already deployed server.

Start with a server running Ubuntu. The current production server is running 22.04, other versions will probably also work. 

Clone the git repository in the home directory 

```bash
git clone https://github.com/shanecranor/CSSpark_Bot.git
cd CSSpark_Bot
```

At this point you will need to install the dependencies listed at the top of this page. By default Ubuntu does not have pip so you will need to install it 

```bash
sudo apt update
sudo apt install python3-pip
pip install -r requirements.txt
```

In that folder, create a `.env` file with the database connection string and bot credentials following the template in `.env.template`.

It is probably a good idea at this point to make sure the bot code will run with

```bash
python3 main.py
```

Kill the bot with ctrl + c once you confirm it launches and functions with no errors. (don't forget to allowlist the server's IP in MongoDB)

Now make a systemd service. Create a file called `redditbot.service` in `/etc/systemd/system/`

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

run the following commands to get the reddit bot service running!

```bash
#enables start on boot so the bot will come back in the event the server randomly reboots
sudo systemctl enable redditbot.service 
sudo systemctl start redditbot.service
#check that the service is running
sudo systemctl status redditbot.service
```

you should have sucessfully deployed the bot to a server!
