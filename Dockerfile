FROM python:3.9-slim

RUN pip install --no-cache-dir requests python-telegram-bot

WORKDIR /app
COPY bot.py /app

CMD ["python", "bot.py"]
