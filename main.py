import logging
import time

import requests
import telegram
from decouple import config


class MyLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.tg_bot = tg_bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def get_reviews(token, timestamp):
    api_endpoint = "https://dvmn.org/api/long_polling/"
    headers = {
        "Authorization": f"Token {token}"
    }
    payload = {
        "timestamp": timestamp
    }
    response = requests.get(api_endpoint, headers=headers, timeout=90, params=payload)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    devman_token = config('DEVMAN_TOKEN')
    tg_bot_token = config('TELEGRAM_BOT_TOKEN')
    tg_admin_bot_token = config('TELEGRAM_ADMIN_BOT_TOKEN')
    chat_id = config('TG_CHAT_ID')
    admin_chat_id = config('TG_ADMIN_CHAT_ID')

    timestamp = None

    bot = telegram.Bot(tg_bot_token)
    admin_bot = telegram.Bot(tg_admin_bot_token)

    logger = logging.getLogger("tg_logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler(admin_bot, admin_chat_id))
    logger.info("Бот запущен")

    while True:
        try:
            reviews = get_reviews(devman_token, timestamp)
            if reviews["status"] == "timeout":
                timestamp = reviews["timestamp_to_request"]
            elif reviews["status"] == "found":
                timestamp = reviews["last_attempt_timestamp"]
                if reviews["new_attempts"][0]["is_negative"]:
                    result = "К сожалению, в работе нашлись ошибки"
                else:
                    result = "Преподавателю все понравилось, можно приступать к следующему уроку"
                lesson_title = reviews["new_attempts"][0]["lesson_title"]
                lesson_url = reviews["new_attempts"][0]["lesson_url"]
                message_to_customer = f"У вас проверили работу '[{lesson_title}]({lesson_url})'\n{result}"
                bot.send_message(chat_id=chat_id, text=message_to_customer, parse_mode="Markdown",
                                 disable_web_page_preview=True)
        except requests.exceptions.HTTPError:
            logger.info('Неверная ссылка')
        except requests.exceptions.ConnectionError:
            logger.info('Нет подключения к сети')
            time.sleep(90)
        except requests.exceptions.ReadTimeout:
            pass
