#!/bin/bash
echo fetching from git
git pull
echo killing bot
sudo systemctl stop redditbot.service
echo starting bot
sudo systemctl start redditbot.service
echo printing status
sudo systemctl status redditbot.service