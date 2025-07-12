import os
import schedule
import vk_api
import json
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import pytz
from datetime import datetime, timedelta
from dotenv import load_dotenv
import telebot
import random

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

time_zone = pytz.timezone(os.environ.get("TIME_ZONE"))
vk_bot_token=os.environ.get("VK_BOT_TOKEN")
tg_bot_token=os.environ.get("TG_BOT_TOKEN")

vk_bot_session = vk_api.VkApi(token=vk_bot_token)
vk_bot_api = vk_bot_session.get_api()

tg_bot = telebot.TeleBot(tg_bot_token, parse_mode="MARKDOWN")

def main():
    sequence() # Требуется для первого запуска без ожидания истечения времени выставленного в модуле schedule.
    schedule.every().minute.do(sequence)
    while True:
        schedule.run_pending()

def sequence():
    global timetables, phrases, current_date, current_weekday, current_time, duty_section
    current_date = datetime.now(time_zone)
    current_weekday = current_date.isoweekday()
    current_time = current_date.time().strftime("%H:%M")
    timetables = load_json('timetables.json')
    phrases = load_json('phrases.json')
    duty_section = timetables['sections'][(current_date.isocalendar().week) % len(timetables['sections'])]
    vacations = duty_section['vacations']
    on_vacation=False
    if len(vacations) > 0 :
        for vacation in vacations:
            if int(vacation['begin']) <= int(current_date.isocalendar().week) <= int(vacation['end']) :
                on_vacation=True
    if on_vacation is False:
        monday_notifications()
        duty_notification()

def load_json(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        _ = json.load(file)
    file.close()
    return _
    
def monday_notifications():
    if current_weekday == 1 :
        match current_time:
            case "09:00" :
                duty_section_icon = str(duty_section['icon'])
                duty_section_name = str(duty_section['name'])
                message = "На этой неделе дежурит секция:\n" \
                          "{0} {1}".format(
                    duty_section_icon,
                    duty_section_name
                )
                send_vk_message(int(timetables['main_vk_chat_id']),message)
                send_tg_message(int(timetables['main_tg_chat_id']),message)
            case "14:00" :
                previus_date = current_date - timedelta(days=7)
                if current_date.month != previus_date.month : # Первый понедельник месяца
                    icon = random.choice(phrases['club_fees']['icons'])
                    punch = random.choice(phrases['club_fees']['punches'])
                    message = "Напоминание о сборе клубных взносов. {0}\n" \
                              "\n" \
                              "👹 {1}".format(
                        icon,
                        punch
                    )
                    send_vk_message(int(timetables['main_vk_chat_id']),message)

def duty_notification():
    for workout in duty_section['workouts']:
        if current_weekday == int(workout['weekday']):
            if current_time == str(workout['begin']):
                icon = random.choice(phrases['duty_start']['icons'])
                message = "Дружественное напоминание о дежурстве {}".format(icon)
                send_vk_message(duty_section['chat_id'],message)
            elif current_time == str(workout['end']):
                gratitude = random.choice(phrases['duty_end']['gratitudes'])
                gratitude_icon = random.choice(phrases['duty_end']['gratitude_icons'])
                message = "Перед уходом, пожалуйста, убедитесь, что:\n" \
                          "- Снаряжение убрано по местам\n" \
                          "- Посуда помыта и убрана в шкаф\n" \
                          "- Мусорное ведро остаётся пустым\n" \
                          "\n" \
                          "{0} {1}".format(
                    gratitude,
                    gratitude_icon
                )
                send_vk_message(duty_section['chat_id'],message)

def send_vk_message(chat_id, message):
    vk_bot_session.method("messages.send", {"peer_id":chat_id, "message":message,"random_id":0})
    write_log('logfile.txt', "vk " +chat_id, message)

def send_tg_message(chat_id, message):
    tg_bot.send_message(chat_id, message)
    write_log('logfile.txt', "tg " + chat_id, message)

def write_log(filename, chat_info, message):
    try:
        with open(os.path.join(os.path.dirname(__file__), filename), 'a') as logfile:
            logfile.write("########################### " +
                          current_date.strftime("%Y/%m/%d %H:%M") + 
                          " ###########################" +
                          '\n' +
                          chat_info + 
                          '\n\n' +
                          message + 
                          '\n\n')
        logfile.close()
    except:
        print("Ошибка при попытке записи")

if __name__ == '__main__':
    main()
