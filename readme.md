# Подготовка к работе
Для начала работы достаточно запустить скрипт автоматической установки, который можно скачать из репозитория в виде raw-файла:  
`wget https://raw.githubusercontent.com/ArchelonU/citadel.reminder/refs/heads/master/auto_install.sh`

По умолчанию, в качестве рабочей директории программы задан путь **/opt/citadel.reminder**, а в качестве владельца будет указан тот пользователь, из под которого будет выполняться установка. Для успешного отрабатывания скрипта, пользователю потребуются права **root**. При желании перед запуском можно отредактировать переменные с помощью любого тексового редактора. Либо если нет в этом необходимости, просто выполнить скрипт:  
`/bin/bash ./auto_install.sh`

Если изменения директории и пользователя делать не планируется, установку можно сделать одной командой:  
`wget https://raw.githubusercontent.com/ArchelonU/citadel.reminder/refs/heads/master/auto_install.sh | bash`

После чего не забудьте прописать актуальные токены для VK и Telegram в файле **.env**, сделать это можно с помощью любого текстового редактора. Затем проставить соответствующие идентификаторы чатов в файле **timetables.json**, а также, при необходимости, поправить расписание секций (cоблюдая формат данных *json*).

---
### Ручная установка
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

И уже в виртуальном окружении установить используемые пакеты `pytz`, `schedule`, `python-dotenv`, `vk_api` и `pyTelegramBotAPI`:  
`sudo /opt/citadel.reminder/venv/bin/pip install pytz schedule python-dotenv vk_api pyTelegramBotAPI`

Для отправки сообщений в VK, необходимо прописать актуальный токен бота в файле `.env` с переменными окружения:  
`sudo touch /opt/citadel.reminder/.env && echo "VK_BOT_TOKEN = \"VK_token_example_1234567890\"" | sudo tee -a /opt/citadel.reminder/.env`

Там же можно поменять часовой пояс при необходимости:  
`echo "TIME_ZONE = \"Europe/Moscow\"" | sudo tee -a /opt/citadel.reminder/.env`

Для отправки сообщений в Telegram:  
`echo "TG_BOT_TOKEN = \"TG_token_example_1234567890\"" | sudo tee -a /opt/citadel.reminder/.env`

Теперь необходимо создать файл с расписанием занятий и идентификаторами чатов. Пример можно найти в директории `/opt/citadel.reminder/examples/timetables.json`, оттуда же его можно и скопировать:  
`sudo cp /opt/citadel.reminder/examples/timetables.json /opt/citadel.reminder/timetables.json`

В нём необходимо проставить соответствующий порядок секций, время их занятий и идентификаторы чатов секций, в которые будут приходить оповещения. Сделать это можно любым файловым редактором:  
`sudo nano /opt/citadel.reminder/timetables.json` или `sudo vim /opt/citadel.reminder/timetables.json`

Запуск программы необходимо осуществлять интерпретатором из виртуального окружения с указанием расположения основного файла программы:  
`sudo /opt/citadel.reminder/venv/bin/python3 /opt/citadel.reminder/main.py`

**Дополнительная информация**  
Для упрощения ручного запуска можно сделать алиас, вызывающий нужный интерпретатор с аргументом, содержащим полный путь до основного файла программы:  
`alias citadel.reminder.py="/opt/citadel.reminder/venv/bin/python3 /opt/citadel.reminder/main.py"`

Чтобы алиас работал для всех пользователей, данную строку можно поместить в `/etc/bash.bashrc` (для чего снова потребуются права суперпользователя), например, так:  
`sudo echo "alias citadel.reminder.py=\"/opt/citadel.reminder/venv/bin/python3 /opt/citadel.reminder/main.py\"" >> /etc/bash.bashrc`

После добавления строки, необходимо либо перезайти, либо перечитать файл `~/.bashrc` или `/etc/bash.bashrc`, в зависимости от того, куда был прописан алиас:  
`source ~/.bashrc` или `source /etc/bash.bashrc`

---
### Автоматизация запуска
Автоматизацию запуска можно сделать через создание `systemd` сервиса, либо с помощью `supervisor`, который помимо запуска может ещё и отслеживать состояние работы.

Для использования `supervisor` необходимо установить соответствующий пакет:  
`sudo apt update && sudo apt -y install supervisor`

Затем перенести файл конфигурации супервизора для приложения:  
`sudo cp /opt/citadel.reminder/supervisor.conf /etc/supervisor/conf.d/citadel.reminder.conf`

После этого можно перезагрузить супервизор для подхвата конфигурации:  
`sudo supervisorctl reload`