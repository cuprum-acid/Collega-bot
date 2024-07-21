import requests
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, ApplicationBuilder, JobQueue

from mem import get_mem

TELEGRAM_BOT_TOKEN = ''
SERVER_URL = "https://api.mcsrvstat.us/3/d11.gamely.pro:20187"
REQUEST_INTERVAL = 240
online_players = []


def get_players() -> (list[str], None):
    response = requests.get(SERVER_URL)
    data = response.json()
    if 'players' in data and 'online' in data['players']:
        online_players_count = data['players']['online']
        if online_players_count > 0 and 'list' in data['players']:
            return [player['name'] for player in data['players']['list']]
        else:
            return []
    else:
        return None


async def check_new_players(context: CallbackContext) -> None:
    global online_players
    current_players = get_players()
    if current_players is None:
        return
    joined_players = set(current_players) - set(online_players)
    quited_players = set(online_players) - set(current_players)
    online_players = current_players
    if joined_players or quited_players:
        reply = (f'{"На сервер зашли игроки: " + ", ".join(joined_players) + ". " if joined_players else ""}'
                 f'{"С сервера вышли: " + ", ".join(quited_players) if quited_players else ""}')
        await context.bot.send_message(context.job.chat_id, reply)


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        'Привет! Используй команду /players, чтобы узнать кто сейчас на сервере Minecraft. '
        'Запусти слежку за сервером командой /monitor или останови ее с помощью /monitor_stop '
        'А если хочешь получить мем-предсказание на день, введи /mem_taro'
    )


async def players(update: Update, context: CallbackContext) -> None:
    global online_players
    try:
        online_players = get_players()
        if online_players is None:
            reply = 'Не удалось получить информацию о игроках.'
        elif online_players:
            reply = f'В данный момент на сервере находятся игроки: {", ".join(online_players)}'
        else:
            reply = 'На сервере в данный момент нет игроков.'
    except Exception as e:
        reply = f"Произошла ошибка при запросе к серверу: {e}"
    await update.message.reply_text(reply)


async def monitor(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    context.job_queue.run_repeating(check_new_players, interval=REQUEST_INTERVAL, chat_id=chat_id)
    await update.message.reply_text(
        'Коллеги! Просьба не опаздывать на пары! '
        'Теперь я слежу за всеми входящими и выходящими в аудиторию.'
    )


async def monitor_stop(update: Update, context: CallbackContext) -> None:
    await context.application.job_queue.stop()
    await update.message.reply_text('Свободная посещаемость! я не слежу за вами.')


async def mem_taro(update: Update, context: CallbackContext) -> None:
    await get_mem(update, context)


def main() -> None:
    application = ApplicationBuilder().job_queue(JobQueue()).token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("monitor", monitor))
    application.add_handler(CommandHandler("monitor_stop", monitor_stop))
    application.add_handler(CommandHandler("players", players))
    application.add_handler(CommandHandler("mem_taro", mem_taro))
    application.run_polling()


if __name__ == '__main__':
    main()
