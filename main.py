from decouple import config
import requests
import json


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
    reviews = response.json()
    return reviews


if __name__ == "__main__":
    devman_token = config('DEVMAN_TOKEN')
    timestamp = None
    while True:
        try:
            reviews = get_reviews(devman_token, timestamp)
            json_formatted_str = json.dumps(reviews, indent=2)
            print(json_formatted_str)
            if reviews["status"] == "found":
                timestamp = reviews["last_attempt_timestamp"]
            else:
                timestamp = reviews["timestamp_to_request"]
        except requests.exceptions.HTTPError:
            print('Неверная ссылка')
        except requests.exceptions.ReadTimeout:
            print('Сервис не ответил по каким то причинам, пробуем послать еще один запрос')
        except requests.exceptions.ConnectionError:
            print('Нет подключения к сети')
