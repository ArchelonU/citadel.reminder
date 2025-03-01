import os
import schedule
import vk_api
import json
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import pytz
from datetime import datetime, timedelta
from dotenv import load_dotenv
import telebot

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
    global current_date, current_weekday, current_time, duty_section
    current_date = datetime.now(time_zone)
    current_weekday = current_date.isoweekday()
    current_time = current_date.time().strftime("%H:%M")
    load_timetables()
    duty_section = timetables['sections'][(current_date.isocalendar().week) % len(timetables['sections'])]
    monday_notifications()
    duty_notification()

def load_timetables():
    global timetables
    with open(os.path.join(os.path.dirname(__file__), 'timetables.json')) as file:
        timetables = json.load(file)
    file.close()
    
def monday_notifications():
    if current_weekday == 1 :
        match current_time:
            case "09:00" :
                message = "На этой неделе дежурит секция:\n" + str(duty_section['icon']) + " " + str(duty_section['name'])
                send_vk_message(int(timetables['main_vk_chat_id']),message)
                send_tg_message(int(timetables['main_tg_chat_id']),message)
            case "14:00" :
                previus_date = current_date - timedelta(days=7)
                if current_date.month != previus_date.month : # Первый понедельник месяца
                    for section in timetables['sections']:
                        message = "Напоминание о сдаче взносов. 💰\n\n👹 Казна сама себя не наполнит!"
                        send_vk_message(section['chat_id'],message)

def duty_notification():
    for workout in duty_section['workouts']:
        workout_weekday = int(workout['weekday'])
        if current_weekday == workout_weekday:
            workout_start = str(workout['start'])
            workout_end = str(workout['end'])
            if current_time == workout_start:
                message = "Дружественное напоминание о дежурстве 🙌"
                send_vk_message(duty_section['chat_id'],message)
            if current_time == workout_end:
                message = "Перед уходом, пожалуйста, убедитесь, что:\n" \
                            "- Снаряжение убрано по местам\n" \
                            "- Посуда помыта и убрана в шкаф\n" \
                            "- Мусорное ведро остаётся пустым\n" \
                            "\n" \
                            "Благодарим за вклад в общее дело! 🤝"
                send_vk_message(duty_section['chat_id'],message)

def send_vk_message(chat_id, message):
    vk_bot_session.method("messages.send", {"peer_id":chat_id, "message":message,"random_id":0})

def send_tg_message(chat_id, message):
    tg_bot.send_message(chat_id, message)

if __name__ == '__main__':
    main()
