FROM python:3.11.5-slim-bookworm

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . /app

COPY bot.py /app
COPY mem.py /app
COPY players_info.py /app
COPY res /app

# Set the entrypoint command to run your application
CMD ["python", "bot.py"]