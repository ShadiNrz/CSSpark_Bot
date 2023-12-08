#!/bin/bash
git pull
sudo systemctl stop redditbot.service
sudo systemctl start redditbot.service