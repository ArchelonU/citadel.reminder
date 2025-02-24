### Подготовка к работе
Для начала необходимо определиться с размещением кода. Его можно разместить в любую папку, например в **домашнюю папку пользователя** из под которого он будет запускаться, либо в какую-то общую папку, например **/opt/citadel.reminder**:  
`cd /opt && sudo git clone https://github.com/ArchelonU/citadel.reminder.git`  

При размещении кода в папке с чересчур высокими правами, **git** предупредит об этом. Можно попробовать сменить владельца, желательно указав специально созданного для этого пользователя:  
`sudo chown -R user:user /opt/citadel.reminder`

Если необходимость работы в папке с высокими правами сохраняется, то для дальнейшей работы с **git** потребуется выполнить команду, которая пометит у себя директорию как безопасную:  
`sudo git config --global --add safe.directory /opt/citadel.reminder`

Для запуска программы необходимо установить дополнительные библиотеки **python** (рекомендуется делать это в виртуальном окружении) и прописать токен бота в переменные окружения.  
Для этого, сначала необходимо установить программные пакеты `pip` и `python3-venv`:  
`sudo apt update && sudo apt -y install pip python3-venv`

Затем создать директорию виртуального окружения, например `/opt/citadel.reminder/venv/`:  
`sudo python3 -m venv /opt/citadel.reminder/venv/`

После чего можно проверить обновления для `pip` в виртуальном окружении:  
`sudo /opt/citadel.reminder/venv/bin/pip install --upgrade pip`

И уже в виртуальном окружении установить используемые пакеты `pytz`, `schedule`, `vk_api` и `python-dotenv`:  
`sudo /opt/citadel.reminder/venv/bin/pip install pytz schedule vk_api python-dotenv`

Для отправки сообщений, необходимо прописать актуальный токен бота в файле `.env` с переменными окружения:  
`sudo touch /opt/citadel.reminder/.env && echo "VK_BOT_TOKEN = \"token_example_1234567890\"" | sudo tee -a /opt/citadel.reminder/.env`

Там же можно поменять часовой пояс при необходимости:  
`echo "TIME_ZONE = \"Europe/Moscow\"" | sudo tee -a /opt/citadel.reminder/.env`

Запуск программы необходимо осуществлять интерпретатором из виртуального окружения с указанием расположения основного файла программы:  
`sudo /opt/citadel.reminder/venv/bin/python3 /opt/citadel.reminder/main.py`

---
Для упрощения ручного запуска, можно сделать алиас, вызывающий нужный интерпретатор с аргументом, содержащим полный путь до основного файла программы:  
`alias citadel.reminder.py="/opt/citadel.reminder/venv/bin/python3 /opt/citadel.reminder/main.py"`

Чтобы алиас работал для всех пользователей, данную строку можно поместить в `/etc/bash.bashrc` (для чего снова потребуются права суперпользователя), например, так:  
`sudo echo "alias citadel.reminder.py=\"/opt/citadel.reminder/venv/bin/python3 /opt/citadel.reminder/main.py\"" >> /etc/bash.bashrc`

После добавления строки, необходимо либо перезайти, либо перечитать файл `/etc/bash.bashrc`:  
`source /etc/bash.bashrc`

----
### Автоматизация запуска
Автоматизацию запуска можно сделать через создание `systemd` сервиса, либо с помощью `supervisor`, который помимо запуска может ещё и отслеживать состояние работы.

Для использования `supervisor` необходимо установить соответствующий пакет:  
`sudo apt update && sudo apt -y install supervisor`

Затем перенести файл конфигурации супервизора для приложения:  
`sudo cp /opt/citadel.reminder/supervisor.conf /etc/supervisor/conf.d/citadel.reminder.conf`

После этого можно перезагрузить супервизор для подхвата конфигурации:  
`sudo supervisorctl reload`