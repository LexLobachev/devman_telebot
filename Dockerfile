FROM python:3.11

COPY requirements.txt /devman_notificator/requirements.txt

WORKDIR /devman_notificator

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /devman_notificator

CMD ["python", "main.py"]