# vk_auto_publisher

The program monitors the verification of your work from the [devman](https://dvmn.org/) site using
their [api](https://dvmn.org/api/docs/) and sends the results of lessons to you in
a [telegram](https://web.telegram.org/z/) chat.

## Environment

### Requirements

Python3(python 3.11 is recommended) should be already installed. Then use pip3 to install dependencies:

```bash
pip3 install -r requirements.txt
```

### Environment variables

- DEVMAN_TOKEN
- TELEGRAM_BOT_TOKEN
- TELEGRAM_ADMIN_BOT_TOKEN
- TG_CHAT_ID
- TG_ADMIN_CHAT_ID

1. Put `.env` file near `requirements.txt`.
2. `.env` contains text data without quotes.

For example, if you print `.env` content, you will see:

```bash
$ cat .env
DEVMAN_TOKEN=your_devman_api_token
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_ADMIN_BOT_TOKEN=your_admin_telegram_bot_token
TG_CHAT_ID=your_telegram_chat_id
TG_ADMIN_CHAT_ID=your_admin_telegram_chat_id
```

#### How to get

* Register on telegram service [telegram](https://web.telegram.org/z/). Default recipient for
  messages. [Contact @myidbot](https://telegram.me/myidbot)
  on Telegram to get and copy your `tg_chat_id`
* Telegram bot token. [Contact @BotFather](https://telegram.me/botfather) to obtain `telegram_bot_token` & `your_admin_telegram_bot_token`.
* Get your `your_admin_telegram_chat_id` & `your_devman_api_token` from [here](https://dvmn.org/api/docs/)
* `your_admin_telegram_bot_token` & `your_devman_api_token` are for your admin

## Run

Launch on Linux(Python 3) or Windows:

```bash
$(venv) python3 main.py
```