FROM ubuntu

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_ROOT_USER_ACTION=ignore

# Установим директорию для работы

WORKDIR /Pallit_Discord_Bot

ENV R_TELEGRAM_BOT_botname ТОКЕН_ВАШЕГО_БОТА

COPY ./requirements.txt ./

RUN apt-get update && \
    apt install python3.10 -y && \
    apt install python3.10-dev -y &&  \
    apt install python3-pip -y && \
    apt install python3.10-venv -y &&  \
    apt-get -y install ffmpeg && \
    apt-get -y install libopus-dev &&  apt-get install libopus0

# Устанавливаем зависимости и gunicorn
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

# Копируем файлы и билд
COPY ./ ./

RUN chmod -R 777 ./

CMD python3 init.py