import json

import requests
import telegram
from decouple import config


def send_tg_message(token, chat_id, lesson_title, result, lesson_url):
    bot = telegram.Bot(token)
    message_to_customer = f"У вас проверили работу '[{lesson_title}]({lesson_url})'\n{result}"
    bot.send_message(chat_id=chat_id, text=message_to_customer, parse_mode="Markdown", disable_web_page_preview=True)


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
    chat_id = config('TG_CHAT_ID')
    timestamp = None
    while True:
        try:
            reviews = get_reviews(devman_token, timestamp)
            json_formatted_str = json.dumps(reviews, indent=2)
            if reviews["status"] == "found":
                timestamp = reviews["last_attempt_timestamp"]
            else:
                timestamp = reviews["timestamp_to_request"]
            if reviews["new_attempts"][0]["is_negative"]:
                result = "К сожалению, в работе нашлись ошибки"
            else:
                result = "Преподавателю все понравилось, можно приступать к следующему уроку"
            lesson_title = reviews["new_attempts"][0]["lesson_title"]
            lesson_url = reviews["new_attempts"][0]["lesson_url"]
            send_tg_message(tg_bot_token, chat_id, lesson_title, result, lesson_url)
        except requests.exceptions.HTTPError:
            print('Неверная ссылка')
        except requests.exceptions.ReadTimeout:
            print('Сервис не ответил по каким то причинам, пробуем послать еще один запрос')
        except requests.exceptions.ConnectionError:
            print('Нет подключения к сети')
