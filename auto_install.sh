#!/bin/bash

project="citadel.reminder"
user=$(whoami)
directory="/opt/$project"

sudo mkdir $directory && sudo chown -R $user:$user $directory
cd $directory/../ && $(git clone https://github.com/ArchelonU/$project.git)

sudo apt update && sudo apt -y install pip python3-venv
python3 -m venv $directory/venv/
$directory/venv/bin/pip install --upgrade pip
$directory/venv/bin/pip install pytz schedule vk_api python-dotenv

cat > $directory/.env <<EOF
VK_BOT_TOKEN = "CHANGE_TO_REAL_TOKEN"
TIME_ZONE = "Europe/Moscow"
EOF

sudo apt update && sudo apt -y install supervisor
sudo cp $directory/supervisor.conf /etc/supervisor/conf.d/$project.conf
sudo supervisorctl reload