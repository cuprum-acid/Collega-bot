FROM python:3.10-slim

RUN pip install --no-cache-dir requests python-telegram-bot
RUN pip install --no-cache-dir python-telegram-bot[job-queue]

WORKDIR /app
COPY bot.py /app
COPY mem.py /app
COPY players_info.py /app
COPY res /app

CMD ["python", "bot.py"]
