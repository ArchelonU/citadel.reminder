#!/bin/bash

project="citadel.reminder"
user=$(whoami)
directory="/opt/$project"

sudo mkdir $directory
sudo chown -R $user:$user $directory
cd $directory/../ && $(git clone https://github.com/ArchelonU/$project.git)

sudo apt update && sudo apt -y install pip python3-venv
python3 -m venv $directory/venv/
$directory/venv/bin/pip install --upgrade pip
$directory/venv/bin/pip install pytz schedule python-dotenv vk_api pyTelegramBotAPI

if [ ! -e $directory/.env ]; then
    cat > $directory/.env <<EOF
VK_BOT_TOKEN = "CHANGE_TO_REAL_VK_TOKEN"
TIME_ZONE = "Europe/Moscow"
TG_BOT_TOKEN = "CHANGE_TO_REAL_TG_TOKEN"
EOF
fi

if [ ! -e $directory/timetables.json ]; then
    cp $directory/examples/timetables.json $directory/timetables.json
fi

if [ ! -e $directory/phrases.json ]; then
    cp $directory/examples/phrases.json $directory/phrases.json
fi

sudo apt update && sudo apt -y install supervisor
sudo cp $directory/examples/supervisor.conf /etc/supervisor/conf.d/$project.conf
sudo supervisorctl reload
