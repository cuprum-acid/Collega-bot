# Run locally

1. Create `.env` file as in `.env.example`.

2. Run following commands:
```bash
poetry install
python bot.py
```

# Run in Docker🐳

1. Create `.env` file as in `.env.example`.

2. Run following commands:
```bash
docker build -t collega-image .
docker run --name collega-container --env-file .env collega-image
```

# Contributing

**🔄 Pull requests are welcome!**

Please, use gitmoji commit conventions.

Read about gitmoji: https://gitmoji.dev/