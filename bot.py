import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, ApplicationBuilder


TELEGRAM_BOT_TOKEN = ''
SERVER_URL = "https://api.mcsrvstat.us/3/d11.gamely.pro:20187"

def get_players():
    try:
        response = requests.get(SERVER_URL)
        data = response.json()
        
        if 'players' in data and 'online' in data['players']:
            online_players = data['players']['online']
            if online_players > 0 and 'list' in data['players']:
                players = data['players']['list']
                return f"В данный момент на сервере находятся игроки: {', '.join(players)}"
            else:
                return "На сервере в данный момент нет игроков."
        else:
            return "Не удалось получить информацию о игроках."
    except Exception as e:
        return f"Произошла ошибка при запросе к серверу: {e}"

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Используй команду /players, чтобы узнать кто сейчас на сервере Minecraft.')

async def players(update: Update, context: CallbackContext) -> None:
    players_info = get_players()
    await update.message.reply_text(players_info)

def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("players", players))

    application.run_polling()

if __name__ == '__main__':
    main()
